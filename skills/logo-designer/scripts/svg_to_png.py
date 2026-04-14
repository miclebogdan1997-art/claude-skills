#!/usr/bin/env python3
"""
Rasterize logo SVG variants to PNGs at multiple sizes.

Usage:
    python svg_to_png.py <input-svg-dir> <output-png-dir>

For each SVG in the input directory, generates PNGs at standard sizes
appropriate for that variant (icon gets favicon/app-icon sizes;
primary/horizontal get web/print sizes).

Tries cairosvg first, then Playwright/Chromium as a fallback. Install
either with:
    pip install cairosvg --break-system-packages
    pip install playwright --break-system-packages && playwright install chromium
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Default export sizes (width in pixels). For icon variants we emit small
# sizes useful for favicons/app icons. For other variants we emit sizes
# useful for web/print.
ICON_SIZES = [16, 32, 48, 64, 128, 256, 512, 1024]
LOCKUP_SIZES = [256, 512, 1024, 2048]


def is_icon_variant(name: str) -> bool:
    return "icon" in name.lower()


def try_cairosvg(svg_path: Path, png_path: Path, width: int) -> bool:
    try:
        import cairosvg  # type: ignore
    except ImportError:
        return False
    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(png_path),
        output_width=width,
    )
    return True


def try_playwright(svg_path: Path, png_path: Path, width: int) -> bool:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except ImportError:
        return False

    svg_content = svg_path.read_text(encoding="utf-8")
    # Wrap in an HTML page so the browser can render it at the exact width.
    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><style>
  html, body {{ margin:0; padding:0; background: transparent; }}
  #wrap {{ display:inline-block; }}
  #wrap svg {{ display:block; width:{width}px; height:auto; }}
</style></head>
<body><div id="wrap">{svg_content}</div></body></html>"""

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width + 20, "height": width + 20})
        page.set_content(html)
        locator = page.locator("#wrap")
        locator.screenshot(path=str(png_path), omit_background=True)
        browser.close()
    return True


def rasterize(svg_path: Path, png_path: Path, width: int) -> None:
    png_path.parent.mkdir(parents=True, exist_ok=True)
    if try_cairosvg(svg_path, png_path, width):
        return
    if try_playwright(svg_path, png_path, width):
        return
    raise RuntimeError(
        "Neither cairosvg nor playwright is available. Install one:\n"
        "  pip install cairosvg --break-system-packages\n"
        "  OR\n"
        "  pip install playwright --break-system-packages && playwright install chromium"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("svg_dir", type=Path, help="Directory containing .svg files")
    ap.add_argument("png_dir", type=Path, help="Output directory for .png files")
    args = ap.parse_args()

    svgs = sorted(args.svg_dir.glob("*.svg"))
    if not svgs:
        print(f"No .svg files found in {args.svg_dir}", file=sys.stderr)
        return 1

    for svg in svgs:
        sizes = ICON_SIZES if is_icon_variant(svg.stem) else LOCKUP_SIZES
        for w in sizes:
            out = args.png_dir / f"{svg.stem}-{w}w.png"
            print(f"  {svg.name} -> {out.name} ({w}px)")
            rasterize(svg, out, w)

    print(f"\nDone. PNG files written to {args.png_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
