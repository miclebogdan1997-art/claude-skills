---
name: project-docs
description: Bootstrap, write, and maintain a structured documentation set for a software project — Architecture Decision Records (ADRs), narrative flow docs with ASCII sequence diagrams, tabular reference catalogs (endpoints / entities / components / state), an agent-readable conventions hub (CLAUDE.md / AGENTS.md), per-change CHANGELOG, code-vs-docs DISCREPANCIES log, and DOCS_SYNC_REPORT audits. Use this skill whenever the user asks to write or update an ADR, document a feature, set up a `docs/` folder, regenerate a file tree, sync docs against the codebase, audit documentation drift, add a CHANGELOG entry, or organize a `CLAUDE.md` / `AGENTS.md` / `.cursorrules` style instructions file. Stack-agnostic — works for backend, frontend, CLIs, libraries, monorepos.
---

# Project Documentation

A discipline for keeping a project's documentation honest, navigable, and code-derived rather than invented.

## When to consult this skill

- "Write an ADR for X" / "document this decision"
- "Document the <feature> flow" / "explain how <X> works step-by-step"
- "Set up `docs/` for this repo" / "I need a documentation structure"
- "Update the docs after this change" / "what docs need updating?"
- "Sync the docs with the code" / "audit my docs"
- "Add an entry to the CHANGELOG"
- "Generate / regenerate the file tree"
- "Write a CLAUDE.md / AGENTS.md for this project"
- The user references a CHANGELOG, DISCREPANCIES, or sync-report file
- The user adds a new endpoint, entity, component, or external integration and asks what to document

If unsure whether docs are involved, read the repo root and `docs/` first — if there's already an ADR folder, an `INDEX.md`, a CHANGELOG, or a `CLAUDE.md`, this skill applies.

## Philosophy

Documentation that survives:

1. **Lives in the repo.** Not in a wiki, not in Notion. Diffs through PRs, ages with the code.
2. **Is derived from code, not invented.** When docs and code disagree, code wins — and the gap goes into `DISCREPANCIES.md` until fixed.
3. **Uses ASCII over images** for sequence diagrams, trees, dependency graphs. Diffable, terminal-readable, no broken Mermaid renderers.
4. **Separates four concerns**: WHY (ADRs) / WHAT (reference catalogs) / HOW (flows) / RULES (conventions hub). Don't merge them.
5. **Has an audit trail** (CHANGELOG) and an **honesty trail** (DISCREPANCIES). Both are first-class files.
6. **Names files by content, not by position.** Prefer `whatsapp-booking.md` over `flow-1.md`.

## Why this format — agent-first, human-friendly

The primary reader of these docs is an AI agent. The format — dense tables, ASCII diagrams, short sentences, single source of truth per fact — is optimized for how LLMs consume text, not for how a developer reads on a wide monitor with coffee.

### What each doc type gives an agent

| Doc | What it tells the agent |
|---|---|
| `CLAUDE.md` | Read first. Stack, layering rules, "when you do X update Y" checklists, task preamble. Sets the mental context for every session. |
| ADRs | "Why this architecture and not another" — prevents the agent from proposing solutions that were already considered and rejected. |
| Reference catalogs | Fast lookup: "what columns does entity X have?", "what props does component Y take?" — without reading source files. |
| Flow docs | "What happens when a webhook arrives" — the ASCII sequence diagram gives the agent a map before it touches code. |
| `DISCREPANCIES.md` | "Warning: the voice webhook is a stub" — prevents the agent from assuming something works when it doesn't. |
| `CHANGELOG.md` | Recent context: what changed in the last few prompts or releases. Keeps the agent from re-doing or conflicting with recent work. |

### Context that survives between sessions

AI agents are stateless. Every new session starts with a blank slate — no memory of what was built yesterday, what decisions were made, or what broke last time. Without docs, the agent's only option is to re-read every source file and reverse-engineer the project's intent from code alone. This is slow, token-expensive, and lossy (code shows *what*, not *why*).

This documentation set acts as **persistent memory across sessions**. When an agent reads `CLAUDE.md` → `CHANGELOG.md` → the relevant flow doc, it reconstructs in seconds what took the previous session hours to build up. Specifically:

- `CLAUDE.md` restores the architectural mental model (layering, conventions, "don't do X")
- `CHANGELOG.md` tells the agent what happened recently — no risk of re-implementing yesterday's work or conflicting with it
- `DISCREPANCIES.md` carries forward known issues so the agent doesn't rediscover them
- ADRs preserve decision rationale so the agent doesn't re-open settled debates
- Reference catalogs give the agent a working index of the codebase without re-scanning files

The more sessions a project goes through, the more valuable this becomes. Session 1 builds the docs. Session 50 benefits from 49 sessions of accumulated, structured context that would otherwise be lost.

### Why these specific format choices

- **ASCII over Mermaid.** Agents see ASCII directly as structured text. Mermaid is a rendering language — an opaque blackbox between the agent and the structure it encodes.
- **Tables over prose.** "The table has columns id, tenant_id, staff_id, service_id, starts_at…" wastes tokens. A table row is a lookup, not a paragraph to parse.
- **Single source of truth per fact.** Agents handle contradictions poorly. If an endpoint's request shape appears in both `endpoints.md` and a flow doc and they differ, the agent picks one arbitrarily. Centralize in the catalog, link from the flow.
- **DISCREPANCIES as a first-class file.** Agents tend to trust documentation. If the code lies relative to the docs, the agent needs an official place that says "this is known to be wrong." Without it, the agent builds on false assumptions.

### The human benefit (collateral, but real)

Anyone who opens the repo 6 months later sees the same story the agent sees. Onboarding becomes "read CLAUDE.md, then the 2-3 flow docs for your area" instead of a week of tribal knowledge transfer. The docs are human-readable — they're just not human-*optimized*. Dense tables and ASCII diagrams are fast to scan once you know the format.

## The four document types

| Type | Purpose | Mutability | Typical filename |
|---|---|---|---|
| **Conventions hub** | Single agent-readable file: stack, rules, workflows, "before you start" checklists | Living | `CLAUDE.md`, `AGENTS.md`, `.cursorrules` |
| **ADR** | One architectural decision, captured at the moment it was made | Immutable once Accepted | `adr/ADR-001-<slug>.md` |
| **Reference doc** | Structured catalog of code-derived facts (endpoints, entities, components, stores) | Regenerated | `endpoints.md`, `entities.md`, `components.md` |
| **Flow doc** | Narrative + ASCII sequence diagram of a multi-step process | Updated when flow changes | `<feature-name>.md` |

Plus three **audit artifacts**:

| File | Purpose |
|---|---|
| `CHANGELOG.md` | Per-change log, chronological, with `[Unreleased]` at the top |
| `DISCREPANCIES.md` | Known gaps between code and docs, or known bugs/stubs |
| `DOCS_SYNC_REPORT.md` | Output of a docs-sync pass — what changed and why |

## Standard tree

```
repo-root/
├── CLAUDE.md                    agent conventions hub (root, not in docs/)
└── docs/
    ├── INDEX.md                 ADR registry table
    ├── CHANGELOG.md
    ├── DISCREPANCIES.md
    ├── adr/
    │   ├── ADR-001-<slug>.md
    │   └── ADR-002-<slug>.md
    ├── architecture/
    │   ├── overview.md          system at 1000ft
    │   ├── dependencies.md      what depends on what
    │   └── tree.md              regenerated file tree
    ├── reference/               or domain-specific subdir name
    │   ├── <catalog-1>.md
    │   └── <catalog-2>.md
    └── flows/
        ├── <feature-1>.md
        └── <feature-2>.md
```

For monorepos with separable subprojects (e.g. backend + frontend), nest a parallel `docs/` under each subproject. Each subproject can have its own `CLAUDE.md` at its root, or the root `CLAUDE.md` can point to them.

---

## Writing an ADR

An Architecture Decision Record captures one decision at the moment it was made. Once Accepted, it is **never edited** — superseded ADRs get a new ADR that supersedes them.

**Required fields**: Status (Proposed / Accepted / Superseded by ADR-NNN / Deprecated), Date (ISO 8601), Context, Decision, Consequences (split Positive / Negative or Trade-offs).

**Optional but recommended**: a `Prompt:` or `Source:` field tracing where the decision came from — useful in AI-assisted development for provenance ("Prompt 3: TanStack Query setup").

Numbering: zero-padded sequential per scope (ADR-001 through ADR-NNN). Backend and frontend can each restart at 001 if they live under separate `docs/` trees.

For the full template and examples, read `references/adr.md` and copy from `assets/adr-template.md`.

After writing an ADR, **also update**:
- `docs/INDEX.md` — add a row to the registry table
- `docs/CHANGELOG.md` — note the new ADR under `[Unreleased]`

## Writing a flow doc

A flow doc tells the story of a multi-step runtime process — a webhook handler chain, an auth flow, an onboarding sequence, a job pipeline. Format:

1. **Entry point** — what triggers it (HTTP route, button click, CRON, message received)
2. **Sequence** — ASCII sequence diagram (vertical, with `|` and `v` arrows) showing every layer crossed
3. **Branches & error paths** — what happens on failure at each step
4. **Side effects** — DB writes, external calls, queue pushes, cache invalidations
5. **Exit conditions** — success state, failure states

Use ASCII over Mermaid. ASCII renders in any terminal, diffs cleanly, and survives format migrations. For ASCII diagram conventions (loops, branches, parallel arrows, indentation), read `references/flow.md`. Template: `assets/flow-template.md`.

## Writing a reference catalog

A reference doc is a structured catalog of code-derived facts. Examples:

- **endpoints.md** — every HTTP route with method, path, auth requirements, request/response shape, error codes
- **entities.md** — every DB entity with columns, types, indexes, relationships
- **components.md** — every reusable UI component with file path, props type, usage notes
- **state.md** — every store / query key / context with shape and ownership rules
- **dependencies.md** — what calls what across modules
- **tree.md** — regenerated `tree -L N` output of the source folder

Catalogs use **tables, not prose**. The reader should be able to Ctrl-F a name and land on its row. For table column conventions and what to include per catalog type, read `references/reference-catalog.md`.

Catalogs are **regenerated**, not hand-edited. The pattern is: read code → emit catalog. They go stale fast — that's why the sync workflow exists.

## Writing the conventions hub

The conventions hub is the **single file an agent reads first**. Standard locations: `CLAUDE.md` (Claude Code), `AGENTS.md` (vendor-neutral), `.cursorrules` (Cursor), `.windsurfrules` (Windsurf). Same content, different filenames per tool.

Required sections:

1. **What is this project** — one paragraph
2. **Tech stack** — bullet list, versions, hosting
3. **Architecture** — the layering rule, with a small ASCII diagram
4. **Solution structure** — the project tree at module level
5. **Coding standards** — rules that survive across tasks (async patterns, naming, error handling)
6. **Workflow rules** — "when you add X, do Y, Z, W"
7. **Before starting any task** — short checklist (read INDEX, check DISCREPANCIES, check CHANGELOG)
8. **Known issues** — pointer to DISCREPANCIES.md

Optional but high-leverage:

- **File naming conventions table** (Interface / Implementation / Test / DTO patterns)
- **Error code → HTTP status mapping** (for backend projects)
- **Sub-agent / parallelization strategy** for AI-assisted work
- **Git workflow** (branch naming, never commit to main, PR-only)

For full hub structure with examples, read `references/conventions-hub.md`. Template: `assets/conventions-hub-template.md`.

## Writing CHANGELOG entries

Format: per-change blocks under `[Unreleased]` at the top, then dated/numbered releases below. Each block lists `### Added`, `### Changed`, `### Fixed`, `### Removed`, `### Deprecated` in that order, omitting empty sections.

For AI-assisted projects, "release" can mean "prompt N completed" rather than "v1.2.0". Either is fine — be consistent.

Template: `assets/changelog-template.md`.

## Writing DISCREPANCIES entries

Every time you find a gap between code and docs, or a stub/TODO that contradicts what docs claim, log it:

```
## <short-title>
- **What docs say**: ...
- **What code does**: ...
- **Status**: Bug | Stub | Documentation gap
- **Resolution**: Fix code | Fix docs | Track as issue #NNN
```

DISCREPANCIES is a **healthy** file. An empty DISCREPANCIES.md is suspicious — it usually means nobody is auditing.

Template: `assets/discrepancies-template.md`.

---

## The "when you add X" workflow tables

The conventions hub should encode workflows so future agents (and humans) know exactly which docs to update for each kind of change. Recommended tables:

### When you add a new entity / database table

1. Create entity + ORM config + migration (or equivalent)
2. Update `reference/entities.md`
3. Update `reference/relationships.md`
4. Note in `CHANGELOG.md` under `[Unreleased]` → `### Added`

### When you add a new endpoint / route

1. Add interface / handler / controller (per project pattern)
2. Update `reference/endpoints.md`
3. Note in `CHANGELOG.md`

### When you add a new external integration

1. Create accessor / client / adapter (per project pattern)
2. Add env var to config
3. Add env var to conventions hub's "Environment Variables" list
4. Update `architecture/dependencies.md`
5. Note in `CHANGELOG.md`

### When you add a new component / store / hook (frontend)

1. Implement
2. Update `reference/components.md` (or `state.md` for stores)
3. Note in `CHANGELOG.md`

### When you make an architecture decision

1. Write `adr/ADR-NNN-<slug>.md`
2. Add row to `INDEX.md`
3. Note in `CHANGELOG.md`

### When you find a bug or doc gap

1. Fix the code (or open an issue)
2. Add an entry to `DISCREPANCIES.md`
3. Note the fix in `CHANGELOG.md`
4. Do **not** edit ADRs — they are immutable

---

## Keeping docs in sync — the PR rule

Documentation must be updated in the same PR as the code change, not in a follow-up. Docs that lag behind code by even one PR are already stale — and stale docs are worse than no docs, because agents trust them.

### The rule

**Every PR that changes behavior must update the relevant docs before merge.** "Behavior" means: new/changed endpoints, entities, flows, config, dependencies, or architecture. Pure refactors (rename, extract method, move file) that don't change external behavior still require a `tree.md` regeneration if the file structure changed.

### What to update per change type

| Change type | Docs to update |
|---|---|
| New/changed endpoint | `reference/endpoints.md`, `CHANGELOG.md` |
| New/changed entity | `reference/entities.md`, `CHANGELOG.md` |
| New/changed flow | `flows/<feature>.md`, `CHANGELOG.md` |
| New config / env var | `CLAUDE.md` (env vars table), `.env.example`, `CHANGELOG.md` |
| Architecture decision | `adr/ADR-NNN-<slug>.md`, `INDEX.md`, `CHANGELOG.md` |
| New dependency / integration | `architecture/dependencies.md`, `CLAUDE.md` (tech stack), `CHANGELOG.md` |
| File structure change | `architecture/tree.md` |
| Bug fix for documented behavior | `DISCREPANCIES.md` (remove entry if it was tracked), `CHANGELOG.md` |

### How to enforce this

For human teams: add a PR checklist item — "Docs updated? If no, why not." Reviewers should block PRs that change behavior without updating docs.

For AI-assisted workflows: the conventions hub (`CLAUDE.md`) already encodes "when you add X, update Y" rules. Any agent that reads `CLAUDE.md` before starting a task will follow the workflow tables. If the agent skips a doc update, it's a sign that `CLAUDE.md` is missing a workflow rule for that change type — fix the hub, not the agent.

For CI enforcement (optional but recommended): a script that compares changed source files against a mapping of "source path → doc path" and flags PRs where source changed but the corresponding doc didn't. This catches drift mechanically rather than relying on discipline.

### What this replaces

With the PR rule in place, the periodic docs-sync pass (below) becomes a **safety net**, not the primary mechanism. Most drift should be caught at PR time. The sync pass catches what slipped through — renamed files, subtle behavior changes, accumulated staleness in catalogs.

---

## Doing a docs sync pass

Periodically (weekly, before a release, or after a sprint) audit the docs against the code. Output: `DOCS_SYNC_REPORT.md` listing every file modified and why.

The pass:

1. Read every reference doc, list every fact it claims (endpoint count, entity columns, manager dependencies, etc.)
2. Read the code, derive ground-truth versions of each fact
3. For each mismatch:
   - **Code newer**: update the doc, list under `## Files Modified` in the sync report
   - **Doc newer (rare)**: investigate — is the code missing something? Likely DISCREPANCIES entry.
   - **Both wrong** (e.g. doc claims behavior, code is a stub): DISCREPANCIES entry, do not silently fix
4. Regenerate `architecture/tree.md` from the actual file system
5. Update CHANGELOG with a "Documentation sync — YYYY-MM-DD" entry
6. Write `DOCS_SYNC_REPORT.md` summarizing what changed

For the full audit checklist and report format, read `references/sync-workflow.md`. Template: `assets/sync-report-template.md`.

A sync pass is **destructive to documentation** (overwrites stale claims) but **non-destructive to code**. If you're tempted to change code during a sync, stop — open a separate PR.

---

## Style rules

- **No marketing language.** Docs describe what is, not what is great. "Fast, scalable, modern" → delete. "Runs on ACA scale-to-zero, cold start ~600ms" → keep.
- **No emoji.** They render inconsistently across terminals and viewers.
- **One H1 per file**, matching the filename's intent.
- **Code blocks have a language tag** (```` ```ts ````, ```` ```sql ````, ```` ```bash ````). Use ```` ```text ```` for ASCII diagrams.
- **Tables for catalogs, prose for flows, ASCII for diagrams.** Don't mix.
- **Dates in ISO 8601** (`2026-04-15`), not `4/15/26` or `April 15, 2026`.
- **Relative links between docs** (`./adr/ADR-001-foo.md`), never absolute URLs to GitHub.
- **Fenced code blocks**, never indented — they break inside lists.
- **Sentence-length lines wrap around 80 columns** in narrative; tables and code blocks don't wrap.

---

## Bootstrapping a new project's docs

If the user has no docs yet, do this in order:

1. Create the standard tree (above)
2. Write `CLAUDE.md` at root — interview the user briefly for stack + conventions, or read the code to derive them
3. Write `docs/INDEX.md` (empty registry)
4. Write `docs/CHANGELOG.md` with `[Unreleased]` and a "Documentation initialized — YYYY-MM-DD" entry
5. Write `docs/DISCREPANCIES.md` (empty, with a one-line "no known issues" placeholder)
6. Write `docs/architecture/overview.md` from a code read
7. Write `docs/architecture/tree.md` by running `tree -L 3 src/` (or equivalent)
8. Identify reference catalogs needed — usually 2-4 (endpoints + entities for backend, components + state for frontend)
9. Identify the 2-3 most important runtime flows and write flow docs for them
10. Write ADRs **only retroactively** for decisions that are already controversial or load-bearing — don't fabricate ADRs for trivial choices

For a brand-new project where code doesn't exist yet, skip steps 6-9 and write only `CLAUDE.md`, `INDEX.md`, `CHANGELOG.md`, `DISCREPANCIES.md`. Add the rest as code lands.

---

## Reference files in this skill

Read on demand:

| File | When to read |
|---|---|
| `references/adr.md` | Writing or updating an ADR — full template, examples, common mistakes |
| `references/flow.md` | Writing a flow doc — ASCII conventions, branches, loops, parallel paths |
| `references/reference-catalog.md` | Writing a reference doc — table conventions per catalog type |
| `references/conventions-hub.md` | Writing or updating CLAUDE.md / AGENTS.md — section-by-section guide |
| `references/sync-workflow.md` | Doing a docs-sync pass — audit checklist and sync report format |

Templates in `assets/`:

| File | Purpose |
|---|---|
| `adr-template.md` | Drop-in ADR template |
| `flow-template.md` | Drop-in flow doc template |
| `conventions-hub-template.md` | Drop-in CLAUDE.md / AGENTS.md template |
| `changelog-template.md` | Drop-in CHANGELOG.md scaffold |
| `discrepancies-template.md` | Drop-in DISCREPANCIES.md scaffold |
| `sync-report-template.md` | Drop-in DOCS_SYNC_REPORT.md scaffold |
| `index-template.md` | Drop-in INDEX.md scaffold |

Open the relevant reference, then copy the matching asset, then fill it in.
