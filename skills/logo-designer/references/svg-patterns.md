# SVG Patterns for Common Logo Types

Starter patterns you can adapt. Don't treat these as templates to copy verbatim — they're meant to get you past the blank page and show the *shape* of good logo SVG.

## Structural conventions

Every logo SVG should look roughly like this:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 120" role="img" aria-label="Company Name logo">
  <g id="icon" transform="translate(0,10)">
    <!-- icon paths, built on a 100x100 grid -->
  </g>
  <g id="wordmark" transform="translate(120,10)" fill="#1a1a1a" font-family="Inter, sans-serif" font-weight="700">
    <text x="0" y="70" font-size="64" letter-spacing="-2">Company</text>
  </g>
</svg>
```

The `<g id="icon">` and `<g id="wordmark">` groups make it trivial to produce variants: just drop one group for icon-only, rearrange `transform` for stacked vs. horizontal.

## Monogram (single letter in a shape)

```svg
<svg viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="48" fill="#1e40af"/>
  <text x="50" y="68" text-anchor="middle" font-family="Inter, sans-serif"
        font-weight="800" font-size="56" fill="white" letter-spacing="-2">M</text>
</svg>
```

Variations: use a rounded square (`<rect rx="20">`), a hexagon (`<polygon>`), or cut the letter out of the shape using `mask` so the letter becomes negative space.

## Geometric abstract mark

```svg
<svg viewBox="0 0 100 100">
  <!-- Two overlapping circles forming a lens/vesica shape -->
  <circle cx="38" cy="50" r="30" fill="#0ea5e9" fill-opacity="0.85"/>
  <circle cx="62" cy="50" r="30" fill="#6366f1" fill-opacity="0.85"/>
</svg>
```

Key techniques: overlapping shapes with partial opacity create a third color in the overlap, evoking connection/union. Simple forms (circle, square, triangle) arranged with intention > complex custom paths.

## Wordmark with custom detail

```svg
<svg viewBox="0 0 400 100">
  <g font-family="Inter, sans-serif" font-weight="800" font-size="80" letter-spacing="-4" fill="#0f172a">
    <text x="0" y="75">acme</text>
    <!-- A single accent dot -->
    <circle cx="370" cy="70" r="6" fill="#f97316"/>
  </g>
</svg>
```

Technique: a tiny accent (a dot, a cut in a letter, a color shift on one glyph) makes a plain wordmark feel designed. Less is more.

## Icon built from letterforms (negative space)

Use `<mask>` to cut shapes out:

```svg
<svg viewBox="0 0 100 100">
  <defs>
    <mask id="cut">
      <rect width="100" height="100" fill="white"/>
      <text x="50" y="70" text-anchor="middle" font-family="Inter, sans-serif"
            font-weight="900" font-size="72" fill="black">A</text>
    </mask>
  </defs>
  <rect width="100" height="100" rx="16" fill="#ef4444" mask="url(#cut)"/>
</svg>
```

This stamps an "A" hole through a red rounded square.

## Badge / emblem style

```svg
<svg viewBox="0 0 200 200">
  <circle cx="100" cy="100" r="95" fill="none" stroke="#1a1a1a" stroke-width="3"/>
  <circle cx="100" cy="100" r="85" fill="none" stroke="#1a1a1a" stroke-width="1"/>
  <!-- top arc text -->
  <path id="top-arc" d="M 30 100 A 70 70 0 0 1 170 100" fill="none"/>
  <text font-family="Georgia, serif" font-size="16" letter-spacing="4" fill="#1a1a1a">
    <textPath href="#top-arc" startOffset="50%" text-anchor="middle">EST. 2026 · HANDCRAFTED</textPath>
  </path>
  <!-- center mark -->
  <text x="100" y="115" text-anchor="middle" font-family="Georgia, serif"
        font-weight="bold" font-size="40" fill="#1a1a1a">NORTH</text>
</svg>
```

Emblems use concentric containers, curved text (`textPath`), and usually serif or slab-serif typography for that craft/heritage feel.

## Gradient (use sparingly)

```svg
<svg viewBox="0 0 100 100">
  <defs>
    <linearGradient id="grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6366f1"/>
      <stop offset="100%" stop-color="#ec4899"/>
    </linearGradient>
  </defs>
  <rect width="100" height="100" rx="24" fill="url(#grad)"/>
</svg>
```

Rule of thumb: if you can make the logo work flat, do that. Gradients should enhance a design that's already strong, not rescue a weak one. Flat logos print and photocopy cleanly; gradients don't.

## Converting wordmark text to paths

When finalizing, you'll often want the wordmark as explicit `<path>` data rather than relying on a font. For drafts, font-family strings are fine; for production, you'd typically use a designer tool to outline the text. Note this in the delivery if you leave it as live text — the user may need to install the referenced font.

## Common mistakes to avoid

- **Don't use `width`/`height` attributes on the root `<svg>`** — it prevents scaling. Use `viewBox` alone.
- **Don't use `filter` effects** (drop-shadow, blur) for core brand marks. They render inconsistently and can't be printed.
- **Don't embed raster images** with `<image href="data:...">`. Defeats the point of SVG.
- **Don't use `stroke` for primary logo forms** unless you really want a line-drawn look. Filled shapes are more reliable at small sizes because strokes can render sub-pixel and become fuzzy.
- **Don't forget the `viewBox`** — without it, the SVG won't scale.
