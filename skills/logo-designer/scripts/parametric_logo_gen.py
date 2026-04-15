#!/usr/bin/env python3
"""
Parametric Logo Generator — Template

This is a starting template for generating logo SVGs with complex organic shapes.
Copy this file, rename it for your project, and customize the shape functions.

Usage:
    python parametric_logo_gen.py <output-dir> --name "Company Name" --tagline "Optional Tagline"

The generator produces all 6 standard logo variants from the same shape definitions,
ensuring consistency across icon, horizontal, stacked, and monochrome versions.
"""

import argparse
import os
import re


# ══════════════════════════════════════════════════════════════════════════════
# SHAPE PARAMETERS — Tweak these to iterate on the design
# ══════════════════════════════════════════════════════════════════════════════

ICON_SIZE = 120          # Icon canvas size (square)
ICON_RADIUS = 24         # Rounded corner radius for icon background
ICON_PADDING = 4         # Padding inside icon background

# Shape-specific parameters — CUSTOMIZE THESE for your logo
# Example: wing parameters for a bird mark
WING_SPREAD = 44         # How far wings extend from center
WING_HEIGHT = 28         # Vertical height of wing curve
WING_TAPER = 6           # How much wing tips taper
BODY_WIDTH = 12          # Width of central body/shield
BODY_HEIGHT = 46         # Height of central body/shield
CENTER_DOT_R = 4         # Radius of center accent dot


# ══════════════════════════════════════════════════════════════════════════════
# COLORS — Define your palette here
# ══════════════════════════════════════════════════════════════════════════════

PRIMARY = "#1E3A8A"      # Main brand color (used for backgrounds, text)
PRIMARY_DARK = "#162D6E"  # Darker variant (gradients, monochrome bg)
ACCENT = "#FFB800"       # Accent color (icon elements, highlights)
WHITE = "#FFFFFF"
BLACK = "#000000"

# Gradient definition (set USE_GRADIENT=False for flat design)
USE_GRADIENT = True
GRADIENT_TOP = PRIMARY
GRADIENT_BOTTOM = PRIMARY_DARK


# ══════════════════════════════════════════════════════════════════════════════
# TYPOGRAPHY
# ══════════════════════════════════════════════════════════════════════════════

FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"
NAME_FONT_SIZE = 56
NAME_FONT_WEIGHT = 800
NAME_LETTER_SPACING = 2
TAGLINE_FONT_SIZE = 32
TAGLINE_FONT_WEIGHT = 600
TAGLINE_LETTER_SPACING = 6


# ══════════════════════════════════════════════════════════════════════════════
# SHAPE BUILDERS — The core of the generator
# ══════════════════════════════════════════════════════════════════════════════

def make_right_wing(cx, cy):
    """Build right wing as a Bézier curve path. Mirror this for the left wing."""
    x0 = cx + 2
    return (
        f"M {x0},{cy-8} "
        f"C {x0+6},{cy-16} {x0+16},{cy-WING_HEIGHT} {x0+WING_SPREAD-18},{cy-WING_HEIGHT-4} "
        f"C {x0+WING_SPREAD-12},{cy-WING_HEIGHT-8} {x0+WING_SPREAD-6},{cy-WING_HEIGHT-8} {x0+WING_SPREAD},{cy-WING_HEIGHT-4} "
        f"L {x0+WING_SPREAD-2},{cy-WING_HEIGHT+4} "
        f"C {x0+WING_SPREAD-6},{cy-WING_HEIGHT+6} {x0+WING_SPREAD-12},{cy-WING_HEIGHT+10} {x0+WING_SPREAD-18},{cy-16} "
        f"C {x0+WING_SPREAD-26},{cy-8} {x0+10},{cy-2} {x0+4},{cy+2} "
        f"Z"
    )


def make_left_wing(cx, cy):
    """Mirror of right wing. Flips x-coordinates around center."""
    x0 = cx - 2
    return (
        f"M {x0},{cy-8} "
        f"C {x0-6},{cy-16} {x0-16},{cy-WING_HEIGHT} {x0-WING_SPREAD+18},{cy-WING_HEIGHT-4} "
        f"C {x0-WING_SPREAD+12},{cy-WING_HEIGHT-8} {x0-WING_SPREAD+6},{cy-WING_HEIGHT-8} {x0-WING_SPREAD},{cy-WING_HEIGHT-4} "
        f"L {x0-WING_SPREAD+2},{cy-WING_HEIGHT+4} "
        f"C {x0-WING_SPREAD+6},{cy-WING_HEIGHT+6} {x0-WING_SPREAD+12},{cy-WING_HEIGHT+10} {x0-WING_SPREAD+18},{cy-16} "
        f"C {x0-WING_SPREAD+26},{cy-8} {x0-10},{cy-2} {x0-4},{cy+2} "
        f"Z"
    )


def make_shield(cx, cy):
    """Central shield/body shape beneath the wings."""
    w = BODY_WIDTH // 2
    h = BODY_HEIGHT // 2
    top_y = cy - h + 8
    bottom_y = cy + h - 8
    peak_y = top_y - 8  # pointed top of shield
    return (
        f"M {cx-w},{top_y} L {cx},{peak_y} L {cx+w},{top_y} "
        f"L {cx+w},{cy+4} "
        f"C {cx+w},{cy+12} {cx+w-2},{cy+16} {cx},{bottom_y} "
        f"C {cx-w+2},{cy+16} {cx-w},{cy+12} {cx-w},{cy+4} Z"
    )


def make_center_dot(cx, cy):
    """Small accent dot at the center of the mark."""
    return f'<circle cx="{cx}" cy="{cy}" r="{CENTER_DOT_R}"/>'


# ══════════════════════════════════════════════════════════════════════════════
# SVG ASSEMBLY
# ══════════════════════════════════════════════════════════════════════════════

def gradient_def(grad_id):
    """Return a linearGradient definition, or empty string if flat."""
    if not USE_GRADIENT:
        return ""
    return f'''<defs>
    <linearGradient id="{grad_id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{GRADIENT_TOP}"/>
      <stop offset="100%" stop-color="{GRADIENT_BOTTOM}"/>
    </linearGradient>
  </defs>'''


def icon_bg(grad_id=None, flat_color=None):
    """Icon background rectangle."""
    fill = f'url(#{grad_id})' if grad_id else flat_color
    p = ICON_PADDING
    s = ICON_SIZE - 2 * p
    return f'<rect x="{p}" y="{p}" width="{s}" height="{s}" rx="{ICON_RADIUS}" fill="{fill}"/>'


def icon_mark(wing_fill, shield_fill, dot_fill):
    """The icon mark elements (wings + shield + dot)."""
    cx, cy = ICON_SIZE // 2, ICON_SIZE // 2
    elements = []
    elements.append(f'<path fill="{wing_fill}" d="{make_left_wing(cx, cy)}"/>')
    elements.append(f'<path fill="{wing_fill}" d="{make_right_wing(cx, cy)}"/>')
    elements.append(f'<path fill="{shield_fill}" d="{make_shield(cx, cy)}"/>')
    elements.append(f'<circle cx="{cx}" cy="{cy}" r="{CENTER_DOT_R}" fill="{dot_fill}"/>')
    return "\n    ".join(elements)


# ══════════════════════════════════════════════════════════════════════════════
# VARIANT GENERATORS
# ══════════════════════════════════════════════════════════════════════════════

def gen_icon(name_text, tagline_text):
    """Icon-only variant (square)."""
    grad = gradient_def("bg")
    bg = icon_bg(grad_id="bg") if USE_GRADIENT else icon_bg(flat_color=PRIMARY)
    mark = icon_mark(ACCENT, PRIMARY_DARK, ACCENT)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ICON_SIZE} {ICON_SIZE}" role="img" aria-label="{name_text} icon">
  {grad}
  {bg}
    {mark}
</svg>'''


def gen_icon_monochrome(name_text):
    """Icon monochrome variant."""
    mark = icon_mark(WHITE, PRIMARY_DARK, WHITE)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ICON_SIZE} {ICON_SIZE}" role="img" aria-label="{name_text} icon mono">
  {icon_bg(flat_color=PRIMARY_DARK)}
    {mark}
</svg>'''


def gen_horizontal(name_text, tagline_text, name_fill, tagline_fill, mono=False):
    """Horizontal lockup: icon left, text right."""
    # Calculate viewBox width
    name_width = len(name_text) * NAME_FONT_SIZE * 0.62
    total_w = ICON_SIZE + 48 + name_width + 40
    total_h = 140

    grad = "" if mono else gradient_def("bgH")
    bg_fill = f'url(#bgH)' if (USE_GRADIENT and not mono) else (PRIMARY_DARK if mono else PRIMARY)
    mark_wing = WHITE if mono else ACCENT
    mark_shield = PRIMARY_DARK
    mark_dot = WHITE if mono else ACCENT

    cx, cy = ICON_SIZE // 2, ICON_SIZE // 2
    text_x = ICON_SIZE + 38

    # Build tagline line
    tagline_el = ""
    if tagline_text:
        tagline_el = f'\n    <text x="{text_x}" y="118" font-size="{TAGLINE_FONT_SIZE}" font-weight="{TAGLINE_FONT_WEIGHT}" letter-spacing="{TAGLINE_LETTER_SPACING}" fill="{tagline_fill}">{tagline_text}</text>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {int(total_w)} {total_h}" role="img" aria-label="{name_text} logo">
  {grad}
  <g transform="translate(10,10)">
    <rect width="{ICON_SIZE}" height="{ICON_SIZE}" rx="{ICON_RADIUS}" fill="{bg_fill}"/>
    {icon_mark(mark_wing, mark_shield, mark_dot)}
  </g>
  <g transform="translate({int(text_x - ICON_SIZE + 120)},0)" font-family="{FONT_FAMILY}">
    <text x="0" y="78" font-size="{NAME_FONT_SIZE}" font-weight="{NAME_FONT_WEIGHT}" letter-spacing="{NAME_LETTER_SPACING}" fill="{name_fill}">{name_text}</text>{tagline_el}
  </g>
</svg>'''


def gen_stacked(name_text, tagline_text):
    """Stacked lockup: icon on top, text below centered."""
    name_width = len(name_text) * (NAME_FONT_SIZE - 4) * 0.62
    total_w = max(400, name_width + 80)
    center_x = total_w / 2
    icon_x = center_x - ICON_SIZE / 2

    grad = gradient_def("bgS")

    tagline_el = ""
    if tagline_text:
        tagline_el = f'\n    <text x="{int(center_x)}" y="240" font-size="{TAGLINE_FONT_SIZE - 2}" font-weight="{TAGLINE_FONT_WEIGHT}" letter-spacing="{TAGLINE_LETTER_SPACING}" fill="{ACCENT}">{tagline_text}</text>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {int(total_w)} 280" role="img" aria-label="{name_text} stacked">
  {grad}
  <g transform="translate({int(icon_x)},10)">
    <rect width="{ICON_SIZE}" height="{ICON_SIZE}" rx="{ICON_RADIUS}" fill="url(#bgS)"/>
    {icon_mark(ACCENT, PRIMARY_DARK, ACCENT)}
  </g>
  <g text-anchor="middle" font-family="{FONT_FAMILY}">
    <text x="{int(center_x)}" y="195" font-size="{NAME_FONT_SIZE - 4}" font-weight="{NAME_FONT_WEIGHT}" letter-spacing="{NAME_LETTER_SPACING}" fill="{PRIMARY}">{name_text}</text>{tagline_el}
  </g>
</svg>'''


def gen_horizontal_mono_light(name_text, tagline_text):
    """Horizontal monochrome for light backgrounds (all dark color)."""
    return gen_horizontal(name_text, tagline_text,
                          name_fill=PRIMARY_DARK, tagline_fill=PRIMARY_DARK, mono=True)


def gen_horizontal_mono_dark(name_text, tagline_text):
    """Horizontal monochrome for dark backgrounds — TODO: invert to white."""
    # For dark bg: icon bg stays dark, elements white, text white
    # This needs custom assembly since it's inverted
    name_width = len(name_text) * NAME_FONT_SIZE * 0.62
    total_w = ICON_SIZE + 48 + name_width + 40
    text_x = ICON_SIZE + 38

    cx, cy = ICON_SIZE // 2, ICON_SIZE // 2

    tagline_el = ""
    if tagline_text:
        tagline_el = f'\n    <text x="0" y="118" font-size="{TAGLINE_FONT_SIZE}" font-weight="{TAGLINE_FONT_WEIGHT}" letter-spacing="{TAGLINE_LETTER_SPACING}" fill="{WHITE}">{tagline_text}</text>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {int(total_w)} 140" role="img" aria-label="{name_text} mono light">
  <g transform="translate(10,10)">
    <rect width="{ICON_SIZE}" height="{ICON_SIZE}" rx="{ICON_RADIUS}" fill="{WHITE}"/>
    {icon_mark(PRIMARY_DARK, WHITE, PRIMARY_DARK)}
  </g>
  <g transform="translate({int(text_x - ICON_SIZE + 120)},0)" font-family="{FONT_FAMILY}">
    <text x="0" y="78" font-size="{NAME_FONT_SIZE}" font-weight="{NAME_FONT_WEIGHT}" letter-spacing="{NAME_LETTER_SPACING}" fill="{WHITE}">{name_text}</text>{tagline_el}
  </g>
</svg>'''


# ══════════════════════════════════════════════════════════════════════════════
# FILE OUTPUT
# ══════════════════════════════════════════════════════════════════════════════

def slugify(text):
    """Convert text to filename-safe slug."""
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def generate_all(output_dir, name, tagline=""):
    """Generate all logo variants and save to output_dir/svg/."""
    svg_dir = os.path.join(output_dir, "svg")
    os.makedirs(svg_dir, exist_ok=True)

    slug = slugify(name)

    variants = {
        f"{slug}-icon.svg": gen_icon(name, tagline),
        f"{slug}-icon-monochrome.svg": gen_icon_monochrome(name),
        f"{slug}-horizontal.svg": gen_horizontal(name, tagline, PRIMARY, ACCENT),
        f"{slug}-stacked.svg": gen_stacked(name, tagline),
        f"{slug}-horizontal-monochrome-dark.svg": gen_horizontal_mono_light(name, tagline),
        f"{slug}-horizontal-monochrome-light.svg": gen_horizontal_mono_dark(name, tagline),
    }

    for filename, svg_content in variants.items():
        path = os.path.join(svg_dir, filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"  ✓ {filename}")

    print(f"\nGenerated {len(variants)} SVG variants in {svg_dir}/")
    return svg_dir


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate logo SVG variants")
    parser.add_argument("output_dir", help="Directory to save generated files")
    parser.add_argument("--name", required=True, help="Company/brand name")
    parser.add_argument("--tagline", default="", help="Optional tagline")
    args = parser.parse_args()

    print(f"Generating logo for: {args.name}")
    if args.tagline:
        print(f"Tagline: {args.tagline}")

    generate_all(args.output_dir, args.name, args.tagline)
