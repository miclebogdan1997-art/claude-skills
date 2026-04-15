# Complex Shapes in Logo SVG

This guide addresses the hardest challenge in code-generated logos: organic and figurative shapes — animals, birds, plants, human figures, or any form that people have a strong mental image of. These shapes are fundamentally different from geometric marks, and trying to hand-code them as raw SVG paths almost always fails.

## Why organic shapes are hard

When you write `<path d="M 50,20 C 60,10 ..."/>` for a circle or a hexagon, small coordinate errors don't matter — the shape is still recognizable. But for an eagle, a lion, or a tree, humans have extremely precise expectations. A wing curve that's 5px off turns an eagle into a duck. A body proportion slightly wrong makes a lion look like a dog. This is the **uncanny valley of SVG**: close-but-wrong organic shapes look worse than obviously abstract ones.

## The complexity tiers

Before starting any icon, classify the shape you need:

### Tier 1: Geometric primitives
Circles, squares, hexagons, triangles, simple polygons. These are SVG's sweet spot — write them directly as `<circle>`, `<rect>`, `<polygon>`. No special approach needed.

### Tier 2: Composed geometric forms
Shapes built from combining primitives — overlapping circles, nested rounded rectangles, simple arrows, basic shields. Still safe to hand-code. Use `<path>` with simple line and arc commands, or combine multiple primitive elements.

### Tier 3: Stylized organic (the sweet spot)
Abstract representations of organic things — a leaf made from two mirrored arcs, a bird suggested by two curved strokes, wings as swept curves, a flame as overlapping teardrop shapes. **This is where most logos should land.** The form *suggests* the subject without trying to literally depict it. Hand-coding with Bézier curves works here, but use the Python generation approach below for iteration speed.

### Tier 4: Detailed silhouettes (danger zone)
Realistic animal outlines, detailed human figures, intricate botanical illustrations. **Do not attempt these as hand-coded SVG paths.** The coordinate precision required is beyond what's practical in code. If a user specifically requests this level of detail, redirect toward Tier 3 abstraction and explain why.

## The golden rule: abstract, don't illustrate

The most important design decision for organic logos is **how far to abstract**. Real-world examples:

- **Twitter/X bird**: Not a realistic bird — three overlapping circles creating a simplified silhouette. ~6 curves total.
- **Lufthansa crane**: A crane in a circle, but massively simplified — the whole bird is maybe 8-10 path commands.
- **WWF panda**: Recognizable as a panda from about 12 black shapes on white. No detail, pure silhouette.

The pattern: reduce the subject to its **minimum recognizable features**. For a bird, that's wings + a suggestion of a head/beak. For a lion, it's the mane silhouette. For a tree, it's the crown shape + trunk. Everything else is noise that makes the logo harder to code, harder to scale, and harder to remember.

### Minimum recognizable features for common subjects

| Subject | Essential features | Skip entirely |
|---------|-------------------|---------------|
| Eagle/bird | Wings (swept curves), optional head point | Feathers, talons, individual wing feathers |
| Lion | Mane outline (radiating curves), profile | Whiskers, fur texture, detailed face |
| Tree | Crown shape (circle/cloud), trunk line | Individual leaves, bark texture, branches |
| Horse | Neck arch, head profile, mane flow | Legs detail, hooves, musculature |
| Fish | Body oval, tail fork, optional fin | Scales, eye detail, gill lines |
| Flower | Petal ring (rotated ellipses), center dot | Stamen detail, leaf veins, stem thorns |
| Shield/crest | Pointed bottom, flat/curved top | Intricate heraldic detail inside |

## Python parametric generation

For Tier 3 shapes, use Python to generate SVG programmatically. This gives you:

1. **Named parameters** — `wing_spread=40` is easier to tweak than finding the right coordinate in a path string
2. **Symmetry for free** — mirror the left wing to create the right wing by flipping x-coordinates
3. **Rapid iteration** — change one number, regenerate all 6 variants at once
4. **Consistency** — all variants (icon, horizontal, stacked, monochrome) stay in sync automatically

### The generation pattern

```python
#!/usr/bin/env python3
"""Parametric logo generator — [Company Name]"""

# ── Shape parameters (tweak these) ──────────────────────
ICON_SIZE = 120
WING_SPREAD = 44
WING_HEIGHT = 30
BODY_WIDTH = 12

# ── Colors ───────────────────────────────────────────────
PRIMARY = "#1E3A8A"
ACCENT = "#FFB800"
DARK_BG = "#162D6E"

# ── Build the shape paths ────────────────────────────────
def make_right_wing(cx, cy):
    """One wing as a Bézier curve — mirror for left."""
    x0 = cx + 2
    return (
        f"M {x0},{cy} "
        f"C {x0+6},{cy-8} {x0+16},{cy-22} {x0+26},{cy-28} "
        f"C {x0+32},{cy-32} {x0+38},{cy-32} {x0+44},{cy-28} "
        f"L {x0+42},{cy-24} "
        f"C {x0+38},{cy-22} {x0+32},{cy-18} {x0+26},{cy-12} "
        f"C {x0+18},{cy-4} {x0+10},{cy+2} {x0+4},{cy+6} "
        f"Z"
    )

def mirror_wing(path_d, cx):
    """Mirror a wing path horizontally around cx."""
    # Parse and flip all x-coordinates around cx
    # ... (implementation depends on path complexity)

def make_shield(cx, cy):
    """Shield/body shape beneath the wings."""
    w = BODY_WIDTH // 2
    return (
        f"M {cx-w},{cy-14} L {cx},{cy-22} L {cx+w},{cy-14} "
        f"L {cx+w},{cy+10} "
        f"C {cx+w},{cy+18} {cx+w-2},{cy+22} {cx},{cy+24} "
        f"C {cx-w+2},{cy+22} {cx-w},{cy+18} {cx-w},{cy+10} Z"
    )

# ── SVG assembly functions ───────────────────────────────
def icon_elements(fill_primary, fill_accent, fill_bg):
    """Return SVG elements string for the icon mark."""
    cx, cy = 60, 60
    return f"""
    <path fill="{fill_accent}" d="{make_right_wing(cx, cy)}"/>
    <path fill="{fill_accent}" d="{make_left_wing(cx, cy)}"/>
    <path fill="{fill_bg}" d="{make_shield(cx, cy)}"/>
    <circle cx="{cx}" cy="{cy}" r="4" fill="{fill_accent}"/>
    """

def write_icon(path, bg_fill, el_primary, el_accent, el_bg):
    """Write the icon-only SVG variant."""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" role="img" aria-label="...">
  <rect x="4" y="4" width="112" height="112" rx="24" fill="{bg_fill}"/>
  {icon_elements(el_primary, el_accent, el_bg)}
</svg>'''
    with open(path, 'w') as f:
        f.write(svg)

# ── Generate all variants ────────────────────────────────
def generate_all(output_dir):
    write_icon(f"{output_dir}/icon.svg", ...)
    write_horizontal(f"{output_dir}/horizontal.svg", ...)
    write_stacked(f"{output_dir}/stacked.svg", ...)
    write_icon_mono(f"{output_dir}/icon-mono.svg", ...)
    write_horizontal_mono_dark(f"{output_dir}/horizontal-mono-dark.svg", ...)
    write_horizontal_mono_light(f"{output_dir}/horizontal-mono-light.svg", ...)
```

### Key principles for the generator

1. **Center of the icon grid** — define `cx, cy` once, build everything relative to it
2. **Symmetry helper** — for bilateral shapes (eagles, shields, butterflies), write one side and mirror it mathematically
3. **Named constants at the top** — `WING_SPREAD`, `BODY_HEIGHT`, etc. so you can iterate fast
4. **One function per variant** — `write_icon()`, `write_horizontal()`, etc. so changes propagate
5. **Color parameters** — pass colors into functions so monochrome variants are just a color swap

## Iteration workflow

When working on a complex organic shape:

1. **Start abstract** — begin at Tier 2-3, not Tier 4. You can always add detail; removing it from a messy shape is painful.
2. **Icon first** — get the mark working at 120×120 before adding wordmarks. If it doesn't read at icon size, it won't work anywhere.
3. **One thing at a time** — adjust wing curve, look at result, then adjust body. Don't change 5 parameters at once.
4. **Name what's wrong** — "looks like a duck" means the head-to-body ratio is off. "Looks like an airplane" means the wings are too straight/angular. Use these diagnostics:

| It looks like... | The problem is... | Fix by... |
|---|---|---|
| A duck | Head too large, body too round | Reduce head, elongate body, sharpen wing tips |
| An airplane | Wings too straight, no curve | Add more Bézier curve to wing paths, add taper |
| A person with arms out | Wings attached at body center | Move wing attachment points higher, add sweep angle |
| A blob | Not enough contrast between elements | Increase negative space, use background color for body |
| A dragonfly | Body too long and thin | Widen body, shorten relative to wings |
| A gingerbread man | Bilateral symmetry too rigid, limbs too uniform | Vary wing shape top-to-bottom, break perfect symmetry slightly |

## When to suggest abstraction to the user

If a user asks for a detailed realistic animal/figure in their logo, don't just try and fail — proactively explain the tradeoff:

> "For logo work, I'd recommend an abstracted version of [subject] rather than a detailed illustration. Think of how Twitter simplified their bird to just a few curves, or how the WWF panda is pure silhouette. This approach scales better (works at favicon size), is more memorable, and I can generate it cleanly in SVG. Want me to go with an abstract/stylized version?"

Most users will agree. If they insist on detail, suggest they commission an illustrator for the detailed version and offer to build the rest of the brand identity (wordmark, lockup variants, monochrome) around it.
