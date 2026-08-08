#!/usr/bin/env python3
"""
generate_portrait.py — photo -> animated ASCII portrait SVG.

Pipeline (see README-notes for why each stage exists):
  1. rembg cutout        -> forces background to white
  2. bilateral filter    -> smooths skin, keeps edges
  3. CLAHE (clip ~3.0)   -> local contrast per tile
  4. darkening curve      (v/255)^1.7  -> keeps detail out of flat mid-tones
  5. map to ASCII ramp   -> ' .`:-=+*cs#%@' (leading space clears bg to nothing)
  6. build SVG rows, each in a clipPath wiped in with SMIL, staggered top->bottom

Usage:
  python3 generate_portrait.py <input.jpg> <output.svg> [--cols 90]

Requires: pillow numpy opencv-python-headless rembg onnxruntime
"""
import sys
import argparse
import base64
import numpy as np
from PIL import Image
import cv2

RAMP = " .`:-=+*cs#%@"          # dark->light is index 0->end; space = background
CHAR_W_EM = 0.600                 # advance width baked into the grid (JetBrains/Liberation/DejaVu/Noto mono)
FONT_SIZE = 12.9
ROW_H = 15.0                      # px per row


def load_font_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("ascii")
    except FileNotFoundError:
        return None


def cutout_on_white(im: Image.Image) -> Image.Image:
    from rembg import remove
    out = remove(im)  # RGBA, subject isolated
    # binarize + median-blur the alpha mask to kill soft fringes / stray background bleed
    alpha = np.array(out.split()[3])
    alpha_bin = (alpha > 140).astype(np.uint8) * 255
    alpha_bin = cv2.medianBlur(alpha_bin, 5)
    mask = Image.fromarray(alpha_bin)
    bg = Image.new("RGB", out.size, (255, 255, 255))
    bg.paste(out, mask=mask)
    return bg


def process_to_gray(im: Image.Image) -> np.ndarray:
    arr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)
    clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    # darkening curve: (v/255)^1.7 * 255 — keeps detail out of flat mid-tones
    curved = ((gray.astype(np.float64) / 255.0) ** 1.55 * 255.0).astype(np.uint8)
    return curved


def to_ascii_rows(gray: np.ndarray, cols: int = 90) -> list[str]:
    h, w = gray.shape
    rows = max(1, round(cols * (h / w) * 0.48))  # mono chars are ~2x taller than wide
    small = cv2.resize(gray, (cols, rows), interpolation=cv2.INTER_AREA)
    n = len(RAMP) - 1
    lines = []
    for r in range(rows):
        line = []
        for c in range(cols):
            v = small[r, c] / 255.0          # 0 = dark, 1 = bright/background
            idx = round((1.0 - v) * n)        # bright -> low idx (space); dark -> high idx (@)
            line.append(RAMP[idx])
        lines.append("".join(line))
    return lines


def rows_to_svg(rows: list[str], font_b64: str | None, fg="#e8e2d4", bg="#0a0a0c") -> str:
    cols = max(len(r) for r in rows)
    char_w = CHAR_W_EM * FONT_SIZE
    width = round(cols * char_w) + 20
    height = round(len(rows) * ROW_H) + 20

    font_face = ""
    if font_b64:
        font_face = f"""
    <style>
      @font-face {{
        font-family: 'ramp';
        src: url(data:font/woff2;base64,{font_b64}) format('woff2');
      }}
      text {{ font-family: 'ramp', monospace; }}
    </style>"""

    parts = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" font-size="{FONT_SIZE}">']
    parts.append(font_face)
    parts.append(f'<rect width="{width}" height="{height}" fill="{bg}"/>')

    for i, row in enumerate(rows):
        y = 20 + i * ROW_H
        text_w = len(row) * char_w
        clip_id = f"clip{i}"
        begin = round(i * 0.09, 2)
        # escape XML special chars
        esc = row.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        parts.append(f'''
  <clipPath id="{clip_id}">
    <rect x="10" y="{y - FONT_SIZE}" width="0" height="{ROW_H}">
      <animate attributeName="width" from="0" to="{text_w}" dur="0.5s"
               begin="{begin}s" fill="freeze" calcMode="spline" keySplines="0.2 0 0.2 1"/>
    </rect>
  </clipPath>
  <text x="10" y="{y}" fill="{fg}" clip-path="url(#{clip_id})" xml:space="preserve">{esc}</text>''')

    parts.append("</svg>")
    return "".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--cols", type=int, default=90)
    ap.add_argument("--font", default="fonts/ramp.woff2")
    ap.add_argument("--no-cutout", action="store_true", help="skip rembg (input already isolated/plain bg)")
    args = ap.parse_args()

    im = Image.open(args.input).convert("RGB")
    im = im if args.no_cutout else cutout_on_white(im)
    gray = process_to_gray(im)
    rows = to_ascii_rows(gray, cols=args.cols)
    font_b64 = load_font_b64(args.font)
    svg = rows_to_svg(rows, font_b64)

    with open(args.output, "w") as f:
        f.write(svg)

    # also dump the raw character grid so compose_hero.py can build a combined card
    import json
    rows_path = args.output.rsplit(".", 1)[0] + ".rows.json"
    with open(rows_path, "w") as f:
        json.dump(rows, f)

    print(f"wrote {args.output}  ({len(rows)} rows x {args.cols} cols, font embedded: {font_b64 is not None})")


if __name__ == "__main__":
    main()
