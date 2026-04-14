# Logo Design Principles — Deeper Notes

## The job of a logo

A logo's job is not to explain what the company does. It's to serve as a recognizable visual signature — a shorthand that lets customers find, remember, and distinguish the brand. A logo is a placeholder for a reputation. The reputation does the work; the logo just has to be something the reputation can attach to.

This reframes a lot of novice instincts. A coffee shop logo doesn't need to show a coffee bean. A bookstore logo doesn't need to show a book. In fact, pictorially literal logos often get in the way — they box the brand in ("we're JUST a coffee shop, forever") and they look like every other coffee shop's logo.

## The five qualities of a good logo

A well-traveled framework:

1. **Simple** — strips away everything non-essential. Can be drawn from memory.
2. **Memorable** — distinctive enough to stick. Has a "hook" — some element that's different from competitors.
3. **Timeless** — avoids trend markers that will date. A logo should still work in 20 years.
4. **Versatile** — works across sizes (favicon to billboard), colors (full color to B&W), and contexts (embroidery to pixel screen).
5. **Appropriate** — suits the industry and audience. A serious law firm and a children's toy company have different visual languages.

If you're torn between two drafts, the one that scores higher on these is usually the better choice.

## Concept > execution

Great logos start from a concept. Before drawing, you should be able to state the idea in one sentence.

- **Amazon**: arrow from A to Z (everything under the sun), and a smile.
- **FedEx**: hidden arrow in the negative space (forward motion).
- **Toblerone**: bear hidden in the mountain (the brand is from Bern, "city of bears").
- **Nike**: a wing (named for the Greek goddess of victory).

You don't need to hide Easter eggs — most good logos have a simple "this evokes that" — but you should have a reason for the choices.

When generating a logo, write down the concept first, then let the concept constrain the design choices. "Icon is a growing sprout stylized as a G" is a concept. "Just something green and modern-looking" is not.

## Why simple wins

Three specific reasons:

**Recognition.** Simple shapes are encoded into memory faster. You can recognize the Apple silhouette in 100ms; you can't recognize a detailed emblem that fast.

**Reproduction.** Simple logos reproduce cleanly in every medium — embroidered on a hat, stamped on a coffee cup, rendered in a favicon, printed in a newspaper. Complex logos lose detail in at least one of these contexts.

**Longevity.** Every trend-y detail (the overused 2010 gradient-and-sheen, the 2015 flat geometric, the 2020 "blob" wordmark) anchors the logo to a moment. Simplicity is more trend-resistant because there's less to become dated.

## Typography choices matter more than you think

For wordmarks and combination marks, the typeface is doing most of the work. Some rough guidance:

- **Geometric sans** (Inter, Poppins, Futura, Circular) — modern, tech, rational.
- **Humanist sans** (Open Sans, Source Sans, Avenir) — friendly, neutral, approachable.
- **Grotesque / neo-grotesque sans** (Helvetica, Inter, Aktiv Grotesk) — neutral, professional, default-looking (both a strength and weakness).
- **Old-style serif** (Garamond, Sabon) — classic, traditional, editorial, book publishing.
- **Modern/transitional serif** (Times, Didot) — elegant, fashion, editorial.
- **Slab serif** (Rockwell, Roboto Slab) — sturdy, confident, utilitarian.
- **Script** (varies wildly) — personal, feminine, artisanal, feminine-coded, fashion, signature-style.
- **Display** (one-off custom) — distinctive, entertainment, bold brands.

Avoid the obvious amateur signals: Comic Sans (unless you're being deliberately arch), Papyrus, Brush Script, Impact. Also avoid stacking multiple typefaces in one logo — one typeface, used well, is almost always stronger.

## Kerning and optical adjustments

The default spacing between letters in most fonts isn't optimized for large display sizes. For a wordmark at 60px+, you'll almost always want to **tighten letter-spacing** (e.g., `letter-spacing: -2` to `-4` in SVG). Look at each letter pair and adjust if one gap looks larger than the others. This is what separates a polished wordmark from an amateur one.

## Grid and geometry

Logos usually feel better when built on an underlying geometric grid. Circles, squares, and triangles with consistent proportions read as "intentional." The famous logos you can think of almost all have this quality — you can draw construction lines through them and the proportions are clean.

You don't have to be rigid about it, but as a sanity check: are the curves all drawn with a consistent radius family? Are the line weights consistent? Is the x-height of the wordmark aligned to something in the icon?

## Common traps

- **Over-designed icons.** Too many details, too many elements. Strip ruthlessly.
- **Clichéd visual metaphors.** Globes for "global." Handshakes for "partnership." Gears for "engineering." Avoid unless you have a genuinely fresh angle.
- **Unreadable wordmarks.** Custom typography is great until the name becomes hard to read. Legibility first, style second.
- **Bad stock-icon combos.** Taking a free stock icon and slapping the company name next to it. Looks cheap.
- **Trying to do too much.** A logo isn't a billboard. It doesn't have room for a tagline, a mission statement, and three icons. Make it one thing.

## When to propose vs. ask

If the user has given you a clear brand brief, just make decisions and execute. Show work, explain reasoning, move fast. You can always iterate.

If the user has given you almost nothing ("make a logo for my company, it's called Acme") and the name is ambiguous, it's fine to ask one batched question — what does the company do, and what mood are they going for? Don't interrogate with ten questions; that's worse than making a reasonable guess and iterating.
