# Skills

A collection of skills for [Claude](https://www.anthropic.com/claude) — reusable packages of instructions, reference docs, and helper scripts that Claude can load on demand to do specialized work.

Skills work in [Claude Code](https://docs.claude.com/en/docs/claude-code), [Cowork](https://www.anthropic.com/cowork), and anywhere else the Claude Agent SDK runs. When a user's request matches a skill's description, Claude loads the skill's instructions (and any referenced files or scripts) and follows them to complete the task.

## Available skills

### [logo-designer](skills/logo-designer)

Designs a complete logo identity for a company or brand: icon, wordmark, and all the variants a real brand needs (primary, horizontal, stacked, icon-only, monochrome black, monochrome white, and primary-on-dark). Produces SVG masters plus PNG exports at multiple sizes, and a single preview HTML showing every variant on light and dark backgrounds at multiple scales.

Covers the full stylistic range — modern, minimalist, vintage, playful, corporate, luxury, geometric, hand-drawn, tech, editorial, and more. Includes a validator script that catches the most common failure mode in AI-generated SVG logos (text overflowing the viewBox) before the files are shipped.

See [skills/logo-designer/examples](skills/logo-designer/examples) for sample outputs from three real briefs (a specialty coffee roaster, a B2B dev tool, and a kids' reading app).

## Installing a skill

Each skill lives in its own folder under `skills/`. To use one:

**In Cowork**, download the skill folder or the `.skill` archive and drop it into your Cowork skills directory. Cowork will pick it up on next session.

**In Claude Code**, copy the skill folder into `~/.claude/skills/` (or your project's `.claude/skills/` for project-scoped skills). Restart Claude Code and the skill will be available.

**As a plugin bundle**, you can also package multiple skills together as a `.plugin` for easier distribution — see the [Claude Code plugin docs](https://docs.claude.com/en/docs/claude-code).

## Repo structure

```
skills/
  <skill-name>/
    SKILL.md          # The skill itself (YAML frontmatter + instructions)
    references/       # Reference docs loaded on demand
    scripts/          # Helper scripts the skill can run
    assets/           # Templates, fonts, icons used in outputs
```

Every skill has a `SKILL.md` at its root with YAML frontmatter declaring the `name` and `description`. The description is what Claude uses to decide whether to invoke the skill, so it should be specific about when to trigger.

## Contributing

If you want to add a skill, open a PR with a new folder under `skills/`. Keep the SKILL.md under ~500 lines; put longer docs in `references/` and only load them when needed (progressive disclosure — this keeps Claude's working context lean).

## License

[MIT](LICENSE) — free to use, modify, redistribute.
