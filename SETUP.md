# Setting this up in AmiTtiwari43/AmiTtiwari43

Everything here is already generated once, using your actual photo — you can
commit it as-is and it'll work immediately. The workflow just keeps the
numbers current after that.

## 1. Drop these files into your profile repo

```
AmiTtiwari43/
├── README.md
├── assets/
│   ├── hero.svg            ← already built, from your photo + sample stats
│   ├── portrait.rows.json  ← the character grid (needed by compose_hero.py)
│   ├── links.json
│   └── stats.sample.json
├── fonts/
│   ├── ramp.woff2           (1.3 KB — 13 portrait characters)
│   ├── labels.woff2         (3.4 KB — stat numbers/labels)
│   └── OFL.txt               (JetBrains Mono license — keep this alongside the fonts)
├── scripts/
│   ├── generate_portrait.py  (run manually, only when you change your photo)
│   ├── generate_stats.py     (run nightly by the workflow)
│   └── compose_hero.py       (run nightly by the workflow)
└── .github/workflows/refresh-profile.yml
```

## 2. Get real numbers instead of the sample stats

The workflow uses GitHub's built-in `GITHUB_TOKEN` — **no secret to create,
no personal access token needed.** The moment the workflow runs once
(automatically at 05:17 UTC nightly, or trigger it manually from the Actions
tab with "Run workflow"), `assets/hero.svg` gets rewritten with your real
contribution count, active days, best week, and sparkline, and committed
back by `github-actions[bot]`.

## 3. If you ever want to swap the photo

```bash
pip install pillow numpy opencv-python-headless rembg onnxruntime --break-system-packages
python3 scripts/generate_portrait.py your_new_photo.jpg assets/portrait.svg --cols 90 --font fonts/ramp.woff2
python3 scripts/compose_hero.py assets/portrait.rows.json assets/stats.sample.json assets/links.json assets/hero.svg
```
Commit the regenerated `assets/hero.svg` and `assets/portrait.rows.json`.

## 4. A couple of things worth knowing

- **First load may look stale.** GitHub caches profile READMEs briefly —
  if the hero doesn't show up after pushing, open the README once through
  the web UI to force a refresh.
- **`assets/stats.sample.json` is only a fallback reference** — the real
  file the workflow writes is `assets/stats.json`, gitignored-or-not, your
  call. The hero always reflects whatever `stats.json` said on the last run.
- **Your current photo has sunglasses on**, so the eyes render as a flat
  dark shape rather than resolving detail — everything else (jaw, hair,
  cheekbones) came through fine. If you want the eyes to show, send a photo
  without them and re-run step 3 — no other changes needed.
