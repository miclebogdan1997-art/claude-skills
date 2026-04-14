#!/usr/bin/env python3
"""
Sanity-check logo SVGs before delivery. Catches the most common failure mode:
a wordmark whose text extends past the viewBox, which causes silent clipping.

Usage:
    python validate_svgs.py <svg-dir>

Exit code is non-zero if any SVG looks broken. The check is heuristic (it
estimates text width from character count and font-size), so treat warnings
as "look at this before shipping", not as hard errors.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


VIEWBOX_RE = re.compile(r'viewBox\s*=\s*"([^"]+)"')
TEXT_RE = re.compile(
    r'<text\b([^>]*)>(.*?)</text>',
    re.DOTALL,
)
FONT_SIZE_RE = re.compile(r'font-size\s*=\s*"([\d.]+)"')
X_ATTR_RE = re.compile(r'\sx\s*=\s*"([\-\d.]+)"')
TRANSLATE_RE = re.compile(r'translate\(\s*([\-\d.]+)\s*[, ]\s*([\-\d.]+)\s*\)')
STRIP_TAGS = re.compile(r'<[^>]+>')

# Conservative width estimate per glyph at a given font-size for a typical
# 700-weight sans-serif. Real text width varies with font and letter-spacing,
# so we err on the side of "might overflow".
CHAR_WIDTH_FACTOR = 0.58


def parse_viewbox(svg: str) -> tuple[float, float] | None:
    m = VIEWBOX_RE.search(svg)
    if not m:
        return None
    parts = m.group(1).replace(",", " ").split()
    if len(parts) != 4:
        return None
    try:
        _, _, w, h = map(float, parts)
        return w, h
    except ValueError:
        return None


def check_svg(path: Path) -> list[str]:
    """Return a list of warning strings for this SVG (empty if OK)."""
    warnings: list[str] = []
    svg = path.read_text(encoding="utf-8")

    vb = parse_viewbox(svg)
    if vb is None:
        warnings.append("missing or malformed viewBox attribute")
        return warnings
    vb_w, vb_h = vb

    # Walk through every <text> element. We track the nearest enclosing
    # translate() transform from the parent <g> by scanning backward.
    for m in TEXT_RE.finditer(svg):
        attrs, inner = m.group(1), m.group(2)
        text = STRIP_TAGS.sub("", inner).strip()
        if not text:
            continue
        # font-size: check on text, or inherit from nearest ancestor <g>.
        fs_m = FONT_SIZE_RE.search(attrs)
        font_size = float(fs_m.group(1)) if fs_m else None
        if font_size is None:
            # Find parent group's font-size by scanning backward
            head = svg[: m.start()]
            parent = FONT_SIZE_RE.findall(head)
            font_size = float(parent[-1]) if parent else 16.0

        # x attribute on the <text>
        x_m = X_ATTR_RE.search(attrs)
        x = float(x_m.group(1)) if x_m else 0.0

        # Nearest ancestor translate(): scan backward
        head = svg[: m.start()]
        translates = TRANSLATE_RE.findall(head)
        tx = float(translates[-1][0]) if translates else 0.0

        # Estimated rightmost x of the text
        estimated_width = len(text) * font_size * CHAR_WIDTH_FACTOR
        right_edge = tx + x + estimated_width

        if right_edge > vb_w:
            overflow = right_edge - vb_w
            warnings.append(
                f'text "{text}" appears to overflow viewBox by ~{overflow:.0f}px '
                f'(right edge ≈ {right_edge:.0f}, viewBox width = {vb_w:.0f}). '
                f'Widen viewBox to at least {right_edge + 20:.0f} to leave padding.'
            )

    return warnings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("svg_dir", type=Path)
    args = ap.parse_args()

    svgs = sorted(args.svg_dir.glob("*.svg"))
    if not svgs:
        print(f"No .svg files in {args.svg_dir}", file=sys.stderr)
        return 1

    total_warnings = 0
    for svg in svgs:
        warnings = check_svg(svg)
        if warnings:
            print(f"\n{svg.name}:")
            for w in warnings:
                print(f"  WARNING: {w}")
                total_warnings += 1
        else:
            print(f"{svg.name}: OK")

    print(f"\n{total_warnings} warning(s) across {len(svgs)} file(s)")
    return 0 if total_warnings == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
