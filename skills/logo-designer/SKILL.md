---
name: logo-designer
description: "Design a professional company logo and produce a full set of deliverables — SVG source files plus PNG exports — including horizontal, stacked, icon-only, and monochrome variants. Use this skill whenever the user asks to create, design, generate, draft, mock up, or iterate on a logo, brand mark, wordmark, icon, or visual identity for a company, product, startup, app, organization, podcast, brand, side project, or personal brand — even if they don't explicitly say the word 'logo' (for example, 'I need a mark for my new coffee shop', 'can you make something visual for my SaaS', 'design me an identity for...'). Covers the full stylistic range — modern, minimalist, vintage, playful, corporate, luxury, geometric, hand-drawn, tech, editorial, and more."
---

# Logo Designer

This skill produces a complete, professional logo deliverable for a company or brand. The output is a set of SVG files (the master format — scalable, editable, high-quality) plus PNG exports at useful sizes, in all the common layout variants a real brand needs: full lockup, horizontal, stacked, icon-only, and monochrome.

SVG is the default master format because it's infinitely scalable, tiny, editable by any designer afterward, and — critically — can be generated directly as code, so the result is precise and reproducible. PNGs are rasterized from the SVGs for use in contexts that need pixels (favicons, social avatars, slides).

## The design workflow

Follow these phases in order. Don't skip the discovery phase — logos that look good but don't fit the brand are worse than useless.

### Phase 1: Discovery — understand the brand

Before drawing anything, you need enough information to make intentional choices. If any of these are missing from the user's request, ask briefly — bundle the questions so you only interrupt once. The absolute minimum is a name and some sense of what the company does. Ideal additional info:

- **Company name** (exact spelling/capitalization)
- **What they do** (industry + one-sentence description)
- **Audience** (consumer? enterprise? kids? professionals?)
- **Personality** (3-5 adjectives — "warm, trustworthy, modern" vs. "edgy, bold, irreverent")
- **Style direction** (any references, or do they want you to propose?)
- **Color preferences** (any must-have or must-avoid colors?)
- **Where it'll be used** (app icon? storefront sign? letterhead? all of the above?)

If the user is vague ("just make something cool"), don't interrogate them — make reasonable choices and explain your reasoning. You can always iterate.

### Phase 2: Concept — decide the direction

Before generating SVG, pick a concept deliberately. Write a short (3-6 line) design brief for yourself covering:

- **Logo archetype**: wordmark (text-only, like Google), lettermark (initials, like IBM), combination mark (icon + text, like Slack), brandmark (icon alone, like Apple), or emblem (contained, like Starbucks). See `references/archetypes.md` for when each works best.
- **Visual concept**: what's the *idea*? A logo without a concept is just decoration. E.g., "two overlapping circles evoke connection, using negative space to form the letter 'M'". Spell it out.
- **Typography feel**: geometric sans (modern/tech), humanist sans (friendly), serif (editorial/traditional), slab serif (sturdy/confident), script (personal/artisanal), display (distinctive/memorable).
- **Color palette**: 2-4 colors max for the primary logo. Pick intentionally — see `references/color-theory.md` for shorthand on what different colors convey.

Don't over-elaborate. A clear concept stated in one sentence is worth more than three paragraphs of flowery description.

### Phase 3: Generate the SVG

Hand-author the SVG. Don't use AI image generators for this — the skill is built around vector code because vectors are what real brands ship.

Key technical rules for the primary SVG:

- Use a **viewBox** (e.g., `viewBox="0 0 400 120"`) so the logo scales cleanly. Don't hardcode `width`/`height` on the root `<svg>`; let it scale.

- **Size the viewBox generously to fit the entire wordmark** — this is the single most common failure mode in generated logo SVGs. When text extends past the viewBox, the wordmark silently gets clipped and only the first few letters render. Calculate before writing:

  - Rough width of a wordmark at a given font-size: `character_count × font_size × 0.55` for a typical sans-serif at weight 700 with tight letter-spacing. "Wordsprout" (10 chars) at `font-size="72"` ≈ `10 × 72 × 0.55 ≈ 396px` of pure text width.
  - Total viewBox width needed: `icon_width + gap + text_width + padding_both_sides`. For a wordmark translated to `x=130` with ~400px of text, you need at minimum `130 + 400 + 20 ≈ 550px` of viewBox width.
  - When in doubt, round up. A viewBox that's 30px wider than needed just adds whitespace; one that's 30px too narrow destroys the logo.
  - If the company name is long (8+ characters), double-check the math explicitly before finalizing.

- Prefer a slightly tall viewBox so ascenders/descenders have room (e.g., `0 0 W 140` for a 72px font, not `0 0 W 80`).
- Build the **icon** on a coordinate grid that makes sense for it (e.g., a 100×100 or 64×64 grid inside a larger viewBox). Align strokes to pixel or half-pixel boundaries where possible for crisp rendering at small sizes.
- For **typography**, use a real web-safe or Google Font (`font-family="Inter, sans-serif"` etc.) — but also consider converting the wordmark to **paths** for the final master, so it renders identically everywhere without font dependencies. For the working draft, font-family strings are fine.
- Keep the **node count low**. Fewer, cleaner paths > many messy ones. A well-made logo is usually under 2KB of SVG.
- Use `<g>` groups with meaningful `id` attributes (`<g id="icon">`, `<g id="wordmark">`) so variants can reuse them.
- **No raster images** embedded. No filters or effects that won't render consistently. Gradients are OK but use sparingly — flat logos scale and reproduce better.

See `references/svg-patterns.md` for starter shapes and techniques for common logo types (monograms, geometric marks, abstract symbols, badge-style).

### Phase 4: Produce the variants

A real brand needs more than one file. Produce the following, all as separate SVGs.

**Full-color variants (for light backgrounds):**

1. **Primary / combination** — icon + wordmark in the main lockup (usually the most polished arrangement). Wordmark in dark brand color.
2. **Horizontal** — icon on the left, wordmark on the right, vertically centered. Use when space is wide (website headers, email signatures).
3. **Stacked** — icon on top, wordmark below, centered. Use when space is square-ish (app store listings, merch).

**Full-color variant for dark backgrounds** (critical — don't skip this):

4. **Primary on dark** — same layout as primary, but the wordmark is `#ffffff` (or a near-white like `#fafafa`) so it's legible on dark surfaces. The icon usually keeps its brand color, *unless* the brand color is too dark to see on dark — in that case, lighten or invert the icon too. This is one of the most common real-world uses of a logo (dark mode websites, black t-shirts, dark slide decks), so it must exist and must actually be readable.

**Icon-only:**

5. **Icon only** — just the mark, square viewBox. Use for favicons, app icons, social avatars. The icon's colors should work on both light and dark; if not, make a second dark-background version (`icon-on-dark`).

**Monochrome (single-color) variants:**

6. **Monochrome (black)** — entire logo in `#000`. Use for print, stamps, embossing, single-color reproduction on light surfaces.
7. **Monochrome (white)** — entire logo in `#ffffff`. For single-color reproduction on dark surfaces.

Name files predictably: `{slug}-primary.svg`, `{slug}-primary-on-dark.svg`, `{slug}-horizontal.svg`, `{slug}-stacked.svg`, `{slug}-icon.svg`, `{slug}-mono-black.svg`, `{slug}-mono-white.svg`.

**The "legibility on dark" test:** Before moving on, explicitly check — if someone dropped your primary logo onto a black slide, would the company name still be readable? If no, you need `primary-on-dark`. This fails silently in a lot of AI-generated logos because the wordmark is drawn once with dark text and never revisited. Don't let that happen.

### Phase 5: Validate, rasterize, and preview

First, run the validator — it catches the most common silent failure (text overflowing the viewBox):

```bash
python scripts/validate_svgs.py <svg-dir>
```

If it reports any `WARNING: text "..." appears to overflow viewBox`, widen the viewBox in that SVG (or reduce font-size, or shift the wordmark left). Don't skip this — overflow failures are invisible until someone actually views the logo and notices the last letter is cut off.

Then generate PNG exports:

```bash
python scripts/svg_to_png.py <input-svg-dir> <output-png-dir>
```

This creates PNGs at multiple sizes (16, 32, 64, 128, 256, 512, 1024) for each SVG. See the script for the full list of exported sizes per variant.

Then generate the preview HTML:

```bash
python scripts/create_preview.py <svg-dir> <output-html-path> --company-name "Company Name"
```

This builds a single HTML page showing every variant on both light and dark backgrounds, at multiple sizes — the kind of sheet a brand designer would send to a client for review. It's the most honest way for the user to judge whether the logo actually works.

### Phase 6: Deliver

Save all SVG and PNG files into the outputs folder and share them. Present the preview HTML as the main thing for the user to click — it shows everything in context. Offer to iterate on any variant if they want changes.

## Design principles to keep in mind

These aren't rules, they're sanity checks. When in doubt, apply them.

**Simplicity wins.** The logos you remember (Apple, Nike, Target) are extremely simple. If you can't describe your logo concept in one sentence, it's probably too complicated. When choosing between two drafts, pick the simpler one.

**Scalability is non-negotiable.** The logo has to work at 16px (browser tab) and at billboard size. Tiny details vanish at small sizes; complexity becomes noise at large sizes. Test mentally: "Can someone distinguish this from other logos at 24px?"

**The icon must work alone.** If the icon-only variant doesn't carry meaning without the wordmark, the icon isn't strong enough. Rethink it.

**Black-and-white test.** The monochrome version should still be recognizable and balanced. If the logo only works in color, the underlying form isn't strong.

**Avoid trends that date instantly.** Gratuitous gradients, overly-specific "2020s tech startup" shapes, crypto-style geometric gimmicks — these look dated in 3 years. Aim for something that could have been made in 1995 and still work in 2050.

**Don't over-explain via the logo.** A coffee shop's logo doesn't need to literally depict a coffee bean. In fact, it's usually stronger if it doesn't. Evocative > literal.

See `references/design-principles.md` for deeper thinking and examples.

## When the user just wants a quick logo

Not every request needs the full six-phase treatment. If the user says "just throw something together for my side project" or similar, make reasonable choices quickly and produce the core deliverables (primary SVG + icon SVG + a quick preview). You can always offer the full variant set afterward.

## Reference files

- `references/archetypes.md` — Logo archetypes (wordmark, lettermark, etc.) and when each works.
- `references/svg-patterns.md` — Starter SVG patterns for common logo types (monograms, geometric marks, abstract symbols).
- `references/color-theory.md` — Quick reference for color psychology and palette construction.
- `references/design-principles.md` — Extended notes on timeless logo design.

Read them when you need specific guidance — you don't need to read them all every time.
