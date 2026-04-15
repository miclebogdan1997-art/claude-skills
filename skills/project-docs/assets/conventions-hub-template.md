# <Project Name>
Last updated: YYYY-MM-DD

## What is <Project Name>

One paragraph in plain English. What it does, who it's for.

## Tech stack

- Runtime: <name + version>
- Framework: <name + version>
- ORM / data layer: <name + version>
- Database: <name + provider>
- Cache: <name>
- Hosting: <provider + tier>
- Background jobs: <provider>
- External integrations: <list>
- Auth: <strategy>

## Architecture

<One sentence summarizing the layering or module strategy.>

```text
<ASCII diagram of layers or module dependency direction>
```

STRICT rules:
- <rule 1 in present tense>
- <rule 2 in present tense>
- <rule 3 in present tense>
- NEVER <forbidden action>

## Solution structure

```text
<repo-root>/
├── src/
│   ├── <Module 1>/   <one-line purpose>
│   ├── <Module 2>/   <one-line purpose>
│   └── ...
└── tests/
    ├── <Tests 1>/    <one-line purpose>
    └── ...
```

## Multi-tenancy / authorization model

<If applicable: how tenant context flows, how auth is enforced,
what filters apply globally.>

## Coding standards

- <Async pattern rule>
- <Error handling rule — Result<T> vs exceptions>
- <Cancellation token rule>
- <DI / lifetime rule>
- <Migration location rule>
- <Logging convention>
- <Test naming pattern>
- <Time zone handling rule (UTC everywhere?)>
- <Money / decimal handling rule>

## File naming conventions

| Type | Convention | Example |
|------|-----------|---------|
| Interface | <pattern> | <example> |
| Implementation | <pattern> | <example> |
| Request DTO | <pattern> | <example> |
| Response DTO | <pattern> | <example> |
| Test class | <pattern> | <example> |
| Test method | <pattern> | <example> |

## Workflow rules

### When you add a new entity

1. Create entity in `<path>`
2. Create config / migration in `<path>`
3. Update `docs/<reference-catalog>.md`
4. Update `docs/CHANGELOG.md` under `[Unreleased]`

### When you add a new endpoint

1. Add interface / handler in `<path>`
2. Add request/response DTOs in `<path>`
3. Implement
4. Update `docs/<endpoints-catalog>.md`
5. Update `docs/CHANGELOG.md`

### When you add a new external integration

1. Create adapter in `<path>`
2. Add env var to `<config-file>`
3. Add env var to this file's "Environment Variables" section
4. Update `docs/architecture/dependencies.md`
5. Update `docs/CHANGELOG.md`

### When you make an architecture decision

1. Write `docs/adr/ADR-NNN-<slug>.md`
2. Add row to `docs/INDEX.md`
3. Update `docs/CHANGELOG.md`

### When you find a bug or doc gap

1. Fix the code (or open an issue)
2. Add entry to `docs/DISCREPANCIES.md`
3. Note the fix in `docs/CHANGELOG.md`
4. Do NOT edit ADRs

## Before starting any task

1. Read this file
2. Read relevant interface files in `<path>`
3. Read existing implementations of similar features
4. Check `docs/DISCREPANCIES.md` for known issues
5. Check `docs/CHANGELOG.md` to understand recent changes

## Context files per feature area

**<Feature 1>**:
- `<file 1>`
- `<file 2>`
- `<file 3>`

**<Feature 2>**:
- `<file 1>`
- `<file 2>`

## Sub-agent / parallelization strategy

<Optional — for AI-assisted multi-agent work>

STEP 1 — <blocking step that must finish first>:
  - <task A>
  - <task B>

STEP 2 — Parallel implementation:
  - <task C>
  - <task D>
  - <task E>

NEVER parallelize:
  - <serial task 1>
  - <serial task 2>

## Error code → HTTP status mapping

<If applicable>

| Error code | HTTP status |
|---|---|
| `*_NOT_FOUND` | 404 |
| `VALIDATION_FAILED` | 422 |
| `INVALID_CREDENTIALS` | 401 |
| `*` (default) | 500 |

## Scheduled jobs

<If applicable>

| Job | Schedule | Binary arg | Purpose |
|-----|----------|------------|---------|
| <name> | <cron> | <arg> | <purpose> |

## Environment variables

| Variable | Purpose | Required? |
|---|---|---|
| `<NAME>` | <purpose> | Yes / No |

## Git workflow

**Never commit or push directly to `main`.**

For every change:
1. `git checkout -b <branch>`
2. Commit on the branch
3. Push and open a PR
4. Merge only through PR review

Branch naming:
- `feature/<n>`
- `fix/<n>`
- `chore/<n>`

## Known issues

See `docs/DISCREPANCIES.md` for the full list. Top items:

- <Issue 1 in one line>
- <Issue 2 in one line>
- <Issue 3 in one line>

## Documentation

Full docs in `docs/`:
- `docs/INDEX.md` — ADR registry
- `docs/CHANGELOG.md`
- `docs/DISCREPANCIES.md`
- `docs/architecture/` — overview, dependencies, tree
- `docs/adr/` — architecture decision records
- `docs/<reference-folder>/` — endpoints, entities, components, etc.
- `docs/flows/` — multi-step process docs

<!--
Optional sub-project pointer (for monorepos):

## <Sub-project name>

The <name> lives in `<path>/` as a separate <type> project with its
own package manager, CI, and deployment.

For <name> conventions, see `<path>/CLAUDE.md`.
-->
