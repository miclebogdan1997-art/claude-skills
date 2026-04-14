#!/usr/bin/env python3
"""
Generate a single HTML preview page showing every logo variant on the
background it was designed for, at multiple sizes. This is the main
deliverable the user looks at to judge whether the logo actually works.

Variants are auto-classified by filename:
  - *mono-white*, *on-dark*, *reversed* -> shown on DARK backgrounds only
  - *mono-black*                        -> shown on LIGHT backgrounds only
  - *primary*, *horizontal*, *stacked*  -> shown on LIGHT backgrounds
    (unless there's a matching on-dark variant; then only on light)
  - *icon*                              -> shown on BOTH (icons usually
    use colors that work on either)

Usage:
    python create_preview.py <svg-dir> <output-html-path> --company-name "Acme Co"
"""
from __future__ import annotations

import argparse
from pathlib import Path


PREVIEW_ORDER = [
    "primary",
    "primary-on-dark",
    "horizontal",
    "horizontal-on-dark",
    "stacked",
    "stacked-on-dark",
    "icon",
    "icon-on-dark",
    "mono-black",
    "mono-white",
]


def variant_key(path: Path) -> int:
    stem = path.stem.lower()
    for i, key in enumerate(PREVIEW_ORDER):
        if stem.endswith(key):
            return i
    return len(PREVIEW_ORDER)


def background_policy(stem: str) -> tuple[bool, bool]:
    """Return (show_on_light, show_on_dark) for a given variant filename stem."""
    s = stem.lower()
    # Explicitly dark-bg variants
    if any(tag in s for tag in ("mono-white", "on-dark", "reversed", "-inverse")):
        return (False, True)
    # Explicitly light-bg variants
    if "mono-black" in s:
        return (True, False)
    # Icons are typically usable on either — show both
    if s.endswith("icon") or "-icon-" in s or s.endswith("-icon"):
        return (True, True)
    # Everything else (primary, horizontal, stacked, wordmark, etc.) is light-bg
    return (True, False)


def size_policy(stem: str) -> list[str]:
    """Return the sizes to render for this variant.

    Combination marks and wordmarks become illegible at favicon size —
    that's what the icon variant is for. Showing them at 32px would
    create a false "my logo doesn't work" signal.
    """
    s = stem.lower()
    if s.endswith("icon") or "-icon-" in s or s.endswith("-icon"):
        return ["med", "small", "tiny"]  # icon is the one that must survive tiny
    # Lockups (primary/horizontal/stacked, their on-dark & mono versions)
    # — show at large + medium only; they're not meant for favicon use.
    return ["big", "med"]


def inline_svg(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    # Strip XML declaration if present
    if text.startswith("<?xml"):
        text = text.split("?>", 1)[1].lstrip()
    return text


SIZE_LABELS = {"big": "large", "med": "medium", "small": "small (64px)", "tiny": "tiny (32px)"}


def build_cells(content: str, light: bool, dark: bool, sizes: list[str]) -> str:
    cells = []
    if light:
        for sz in sizes:
            cells.append(
                f'<div class="size-cell light"><div class="svg-wrap {sz}">{content}</div>'
                f'<small>light · {SIZE_LABELS[sz]}</small></div>'
            )
    if dark:
        for sz in sizes:
            cells.append(
                f'<div class="size-cell dark"><div class="svg-wrap {sz}">{content}</div>'
                f'<small>dark · {SIZE_LABELS[sz]}</small></div>'
            )
    return "".join(cells)


def build_html(svg_dir: Path, company: str) -> str:
    svgs = sorted(svg_dir.glob("*.svg"), key=variant_key)
    sections = []
    for svg in svgs:
        label = svg.stem
        light, dark = background_policy(label)
        sizes = size_policy(label)
        content = inline_svg(svg)
        cells_html = build_cells(content, light, dark, sizes)
        bg_note = []
        if light:
            bg_note.append("light backgrounds")
        if dark:
            bg_note.append("dark backgrounds")
        note = " + ".join(bg_note)
        sections.append(f"""
        <section class="variant">
          <header>
            <h2>{label}</h2>
            <span class="meta">{note} <span class="filename">· {svg.name}</span></span>
          </header>
          <div class="sizes">{cells_html}</div>
        </section>
        """)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{company} — Logo Preview</title>
<style>
  :root {{
    --fg: #0f172a;
    --muted: #64748b;
    --border: #e2e8f0;
    --light-bg: #ffffff;
    --dark-bg: #0f172a;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", sans-serif;
    color: var(--fg);
    background: #f8fafc;
    padding: 48px 32px;
    line-height: 1.5;
  }}
  .page {{ max-width: 1200px; margin: 0 auto; }}
  h1 {{ font-size: 32px; margin: 0 0 4px; letter-spacing: -0.02em; }}
  .tagline {{ color: var(--muted); margin: 0 0 40px; font-size: 15px; }}
  section.variant {{
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
  }}
  section.variant header {{
    display: flex; align-items: baseline; justify-content: space-between;
    margin-bottom: 16px;
    gap: 16px;
  }}
  section.variant h2 {{ font-size: 18px; margin: 0; text-transform: capitalize; letter-spacing: -0.01em; }}
  .meta {{ color: var(--muted); font-size: 13px; text-align: right; }}
  .filename {{ font-family: ui-monospace, monospace; }}
  .sizes {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 12px;
    align-items: stretch;
  }}
  .size-cell {{
    border: 1px solid var(--border);
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px 16px;
    min-height: 140px;
    position: relative;
  }}
  .size-cell.light {{ background: var(--light-bg); }}
  .size-cell.dark {{ background: var(--dark-bg); border-color: var(--dark-bg); }}
  .size-cell small {{
    position: absolute; bottom: 6px; left: 8px;
    font-size: 10px; letter-spacing: 0.04em; text-transform: uppercase;
    color: var(--muted);
  }}
  .size-cell.dark small {{ color: #94a3b8; }}
  .svg-wrap.big svg {{ width: 240px; height: auto; max-height: 140px; }}
  .svg-wrap.med svg {{ width: 120px; height: auto; max-height: 80px; }}
  .svg-wrap.small svg {{ width: 64px; height: auto; max-height: 64px; }}
  .svg-wrap.tiny svg {{ width: 32px; height: auto; max-height: 32px; }}
  .svg-wrap {{ display: flex; align-items: center; justify-content: center; }}
  footer {{ color: var(--muted); font-size: 13px; margin-top: 32px; }}
</style>
</head>
<body>
<div class="page">
  <h1>{company}</h1>
  <p class="tagline">Logo preview — each variant shown on the background it was designed for, at large/medium/tiny sizes.</p>
  {''.join(sections)}
  <footer>Each SVG is rendered at large (240px), medium (120px), and tiny (32px) widths to approximate the
  scales you'd actually use it at — headers, cards, and favicons. If the tiny rendering is illegible,
  the logo needs simplification. If a variant disappears on its intended background, it needs a color fix.</footer>
</div>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("svg_dir", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--company-name", default="Logo Preview")
    args = ap.parse_args()

    html = build_html(args.svg_dir, args.company_name)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html, encoding="utf-8")
    print(f"Preview written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
