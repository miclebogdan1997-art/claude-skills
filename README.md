# Skills

A collection of skills for [Claude](https://www.anthropic.com/claude) — reusable packages of instructions, reference docs, and helper scripts that Claude can load on demand to do specialized work.

Skills work in [Claude Code](https://docs.claude.com/en/docs/claude-code), [Cowork](https://www.anthropic.com/cowork), and anywhere else the Claude Agent SDK runs. When a user's request matches a skill's description, Claude loads the skill's instructions (and any referenced files or scripts) and follows them to complete the task.

## Available skills

### [logo-designer](skills/logo-designer)

Designs a complete logo identity for a company or brand: icon, wordmark, and all the variants a real brand needs (primary, horizontal, stacked, icon-only, monochrome black, monochrome white, and primary-on-dark). Produces SVG masters plus PNG exports at multiple sizes, and a single preview HTML showing every variant on light and dark backgrounds at multiple scales.

Covers the full stylistic range — modern, minimalist, vintage, playful, corporate, luxury, geometric, hand-drawn, tech, editorial, and more. Includes a validator script that catches the most common failure mode in AI-generated SVG logos (text overflowing the viewBox) before the files are shipped.

See [skills/logo-designer/examples](skills/logo-designer/examples) for sample outputs from three real briefs (a specialty coffee roaster, a B2B dev tool, and a kids' reading app).

### [project-docs](skills/project-docs)

Bootstraps and maintains a structured, agent-first documentation set for any software project. Generates a `CLAUDE.md` conventions hub, Architecture Decision Records (ADRs), reference catalogs (endpoints, entities, components, state), flow docs with ASCII sequence diagrams, a per-change CHANGELOG, and a code-vs-docs DISCREPANCIES tracker.

The format is optimized for how LLMs consume text: dense tables over prose, ASCII over Mermaid, single source of truth per fact, and explicit tracking of known gaps. Docs are updated in the same PR as the code change, with periodic sync passes as a safety net. The result is persistent context that survives between agent sessions — session 1 builds the docs, session 50 benefits from 49 sessions of accumulated structured knowledge.

Includes 5 reference guides (ADR writing, flow doc conventions, catalog formats, conventions hub structure, sync workflow) and 7 drop-in templates. Stack-agnostic — works for backend, frontend, CLIs, libraries, and monorepos.

## Installing a skill

Each skill lives in its own folder under `skills/`. To use one:

**In Cowork**, download the skill folder or the `.skill` archive and drop it into your Cowork skills directory. Cowork will pick it up on next session.

**In Claude Code**, copy the skill folder into `~/.claude/skills/` (or your project's `.claude/skills/` for project-scoped skills). Restart Claude Code and the skill will be available.

**As