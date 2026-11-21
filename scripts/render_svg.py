#!/usr/bin/env python3
"""Render figure SVGs to PNG through headless Chrome, the way a browser shows them.

Matplotlib's own PNG preview (FIG_PREVIEW) and pymupdf do not draw these SVGs as a browser
does (pymupdf drops dashes and clipping), so judge a figure from this render. Run from the
book folder:

    python3 -B scripts/render_svg.py notes/chapter-1/figures/p13-*.svg --out <folder>
    python3 -B scripts/render_svg.py <svg> ... --out <folder> --scale 2 --gray

Each SVG is shown at its own size (1 pt = 4/3 CSS px) on a white page and captured at
`--scale` device pixels per CSS pixel (default 2, a high-density screen). With --gray a
grayscale copy, <name>-gray.png, is written beside it (needs Pillow), to check that the
figure still reads without color (FIGURE_STANDARD.md, point 16).

Chrome is taken from the CHROME environment variable, or the usual macOS and Linux paths.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
]


def chrome():
    """Path of a Chrome or Chromium executable, or SystemExit."""
    env = os.environ.get("CHROME")
    for c in ([env] if env else []) + CANDIDATES:
        if c and (Path(c).exists() or shutil.which(c)):
            return c
    raise SystemExit("render_svg: no Chrome found; set CHROME to its path")


def svg_size_px(path):
    """Width and height of the SVG in CSS px (from its width and height in pt)."""
    head = Path(path).read_text(encoding="utf-8")[:2000]
    m = re.search(r'<svg[^>]*\bwidth="([\d.]+)(pt|px)?"[^>]*\bheight="([\d.]+)(pt|px)?"', head)
    if not m:
        raise SystemExit(f"render_svg: no width and height in {path}")
    k = 4.0 / 3.0 if (m.group(2) or "px") == "pt" else 1.0
    return int(round(float(m.group(1)) * k)), int(round(float(m.group(3)) * k))


def render(svg, out_dir, scale=2.0, gray=False, exe=None):
    """Render one SVG; return the PNG path (and write <name>-gray.png when gray=True)."""
    svg = Path(svg).resolve()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    w, h = svg_size_px(svg)
    png = (out_dir / f"{svg.stem}.png").resolve()
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "page.html"
        page.write_text("<!doctype html><html><head><meta charset='utf-8'><style>html,body{margin:0;padding:0;"
                        f"background:#fff}}img{{display:block}}</style></head><body><img src='{svg.as_uri()}' "
                        f"width='{w}' height='{h}' alt=''></body></html>", encoding="utf-8")
        cmd = [exe or chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
               f"--user-data-dir={tmp}/profile", f"--force-device-scale-factor={scale:g}",
               f"--window-size={w},{h}", f"--screenshot={png}", "--allow-file-access-from-files", page.as_uri()]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    if gray:
        from PIL import Image
        Image.open(png).convert("L").save(out_dir / f"{svg.stem}-gray.png")
    return png


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("svgs", nargs="+")
    ap.add_argument("--out", required=True, help="folder for the PNG files")
    ap.add_argument("--scale", type=float, default=2.0, help="device pixels per CSS pixel (default 2)")
    ap.add_argument("--gray", action="store_true", help="also write a grayscale copy")
    a = ap.parse_args(argv)
    exe = chrome()
    for s in a.svgs:
        print("rendered", render(s, a.out, a.scale, a.gray, exe))


if __name__ == "__main__":
    main(sys.argv[1:])
