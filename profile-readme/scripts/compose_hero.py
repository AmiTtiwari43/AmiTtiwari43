#!/usr/bin/env python3
"""
compose_hero.py — stitches the ASCII portrait rows + stats.json into one
self-contained hero.svg: portrait on top, big total + active-days/best-week
stat blocks below, a hand-drawn sparkline, and a link row underneath.
Everything shares one canvas, one background, one embedded font subset.

Usage:
  python3 compose_hero.py assets/portrait.rows.json stats.json links.json assets/hero.svg
"""
import sys
import json
import base64

CHAR_W_EM = 0.600
FONT_SIZE = 12.9
ROW_H = 15.0
FG = "#e8e2d4"
DIM = "#8a8578"
ACCENT = "#c9a24b"   # warm gold accent
BG = "#0a0a0c"        # near-black


def load_font_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("ascii")
    except FileNotFoundError:
        return None


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def sparkline_path(values, x0, y0, w, h):
    if not values:
        return "", 0, 0
    n = len(values)
    step = w / max(n - 1, 1)
    pts = [(x0 + i * step, y0 + h - v * h) for i, v in enumerate(values)]
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return d, pts[-1][0], pts[-1][1]


def main():
    rows_path, stats_path, links_path, out_path = sys.argv[1:5]
    rows = json.load(open(rows_path))
    stats = json.load(open(stats_path))
    links = json.load(open(links_path))
    font_b64 = load_font_b64("fonts/labels.woff2") or load_font_b64("fonts/ramp.woff2")

    cols = max(len(r) for r in rows)
    char_w = CHAR_W_EM * FONT_SIZE
    portrait_w = cols * char_w
    portrait_h = len(rows) * ROW_H

    pad = 28
    width = round(portrait_w + pad * 2)
    stats_h = 190
    height = round(portrait_h + stats_h + pad * 2)

    svg = []
    svg.append(f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" font-size="{FONT_SIZE}">')
    if font_b64:
        svg.append(f"""<style>
      @font-face {{ font-family:'ramp'; src:url(data:font/woff2;base64,{font_b64}) format('woff2'); }}
      text {{ font-family:'ramp', 'JetBrains Mono', monospace; }}
      .big {{ font-size: 44px; font-weight: 700; fill: {FG}; }}
      .lbl {{ font-size: 12px; fill: {DIM}; letter-spacing: 0.02em; }}
      .stat {{ font-size: 22px; font-weight: 700; fill: {FG}; }}
      .link {{ font-size: 12px; fill: {ACCENT}; }}
      .sep {{ font-size: 12px; fill: {DIM}; }}
    </style>""")
    svg.append(f'<rect width="{width}" height="{height}" fill="{BG}"/>')

    # ---- portrait rows, typed in row by row ----
    for i, row in enumerate(rows):
        y = pad + (i + 1) * ROW_H - 3
        text_w = len(row) * char_w
        cid = f"pc{i}"
        begin = round(i * 0.055, 3)
        svg.append(f'''<clipPath id="{cid}"><rect x="{pad}" y="{y - FONT_SIZE}" width="0" height="{ROW_H}">
<animate attributeName="width" from="0" to="{text_w}" dur="0.4s" begin="{begin}s" fill="freeze" calcMode="spline" keySplines="0.2 0 0.2 1"/>
</rect></clipPath>
<text x="{pad}" y="{y}" fill="{FG}" clip-path="url(#{cid})" xml:space="preserve">{esc(row)}</text>''')

    portrait_end = round(len(rows) * 0.055 + 0.5, 2)
    stats_y0 = pad + portrait_h + 34

    # ---- big total, typed with a wipe ----
    total_str = f"{stats['total_contributions']:,}"
    big_w = len(total_str) * 27
    svg.append(f'''<clipPath id="bigwipe"><rect x="{pad}" y="{stats_y0 - 44}" width="0" height="54">
<animate attributeName="width" from="0" to="{big_w}" dur="0.5s" begin="{portrait_end}s" fill="freeze"/>
</rect></clipPath>
<text x="{pad}" y="{stats_y0}" class="big" clip-path="url(#bigwipe)">{total_str}</text>
<text x="{pad}" y="{stats_y0 + 20}" class="lbl" opacity="0">contributions in the last year
<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{portrait_end + 0.3}s" fill="freeze"/>
</text>''')

    # ---- active days / best week, right-aligned ----
    right_x = width - pad
    ry0 = stats_y0 - 44
    svg.append(f'''<text x="{right_x}" y="{ry0 + 20}" text-anchor="end" class="stat" opacity="0">{stats['active_days']}
<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{portrait_end + 0.15}s" fill="freeze"/></text>
<text x="{right_x}" y="{ry0 + 36}" text-anchor="end" class="lbl" opacity="0">active days
<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{portrait_end + 0.15}s" fill="freeze"/></text>
<text x="{right_x}" y="{ry0 + 62}" text-anchor="end" class="stat" opacity="0">{stats['best_week']}
<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{portrait_end + 0.3}s" fill="freeze"/></text>
<text x="{right_x}" y="{ry0 + 78}" text-anchor="end" class="lbl" opacity="0">best week
<animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="{portrait_end + 0.3}s" fill="freeze"/></text>''')

    # ---- sparkline, drawn in with stroke-dashoffset ----
    spark_y0 = stats_y0 + 48
    spark_h = 46
    d, _, _ = sparkline_path(stats["sparkline"], pad, spark_y0, width - pad * 2, spark_h)
    svg.append(f'''<path d="{d}" fill="none" stroke="{FG}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"
  pathLength="1000" stroke-dasharray="1000" stroke-dashoffset="1000">
<animate attributeName="stroke-dashoffset" from="1000" to="0" dur="0.9s" begin="{portrait_end + 0.5}s" fill="freeze" calcMode="spline" keySplines="0.2 0 0.2 1"/>
</path>''')

    # ---- link row ----
    link_y = height - 16
    link_str = "  ·  ".join(links)
    svg.append(f'''<text x="{width/2}" y="{link_y}" text-anchor="middle" class="link" opacity="0">{esc(link_str)}
<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{portrait_end + 1.2}s" fill="freeze"/></text>''')

    svg.append("</svg>")

    with open(out_path, "w") as f:
        f.write("".join(svg))
    print(f"wrote {out_path} ({width}x{height})")


if __name__ == "__main__":
    main()
