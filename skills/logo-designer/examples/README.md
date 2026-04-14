# Examples

Sample outputs from the `logo-designer` skill — three logos generated from realistic briefs. Open each subfolder's `preview.html` in a browser to see every variant rendered on light and dark backgrounds at multiple sizes.

These are checked in so you can see what the skill produces without installing it. They're not used by the skill at runtime — every real invocation generates fresh SVGs from scratch.

## The briefs

**[driftwood-coffee/](driftwood-coffee/)** — *"Specialty coffee roaster in Portland. We source single-origin beans, roast light, vibe is quiet/craft. I'd love something that feels like it could have existed for 50 years."*
Result: emblem-style mark with serif typography and a warm brown/cream palette.

**[relay/](relay/)** — *"B2B dev tool that lets backend engineers replay production traffic against staging. Audience is senior backend engineers. Modern but not generic-saas."*
Result: combination mark with a stylized replay-arrow icon and a geometric sans wordmark.

**[wordsprout/](wordsprout/)** — *"Educational reading app for kids age 4-7. Warm and playful for kids, but legit and educational for parents."*
Result: combination mark with a sprouting-plant icon in greens and warm orange, rounded sans wordmark.

Each folder contains the seven SVG variants the skill produces: primary, primary-on-dark, horizontal, stacked, icon, mono-black, mono-white. PNG exports are not checked in — they regenerate from the SVGs via `scripts/svg_to_png.py`.
