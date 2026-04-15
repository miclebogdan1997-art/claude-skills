# Docs Sync Workflow

A docs-sync pass is an audit: read the code, derive ground truth, compare to docs, fix the docs (not the code).

## When to run

- Weekly or pre-release
- After a feature sprint
- When a new agent / contributor reports confusion
- When DISCREPANCIES.md hits 5+ entries
- Before handing the project off

## What you produce

One file: `docs/DOCS_SYNC_REPORT.md`. Lists every doc file modified, with a one-line "what changed" per file.

The sync report is **dated**. You can keep historical sync reports (e.g. `DOCS_SYNC_REPORT-2026-04-08.md`) or overwrite the same file each pass — pick one and be consistent.

## The pass, step by step

### 0. Pre-flight

```bash
git checkout -b chore/docs-sync-YYYY-MM-DD
```

A sync pass touches many files. Always on its own branch.

### 1. Take inventory of facts the docs claim

Open every reference doc. For each, list every quantitative or structural claim:

- "9 managers" → check there are still 9
- "endpoint POST /api/bookings has fields A, B, C" → check the controller
- "table Bookings has columns X, Y, Z" → check the entity / migration
- "component `<Topbar>` has props P, Q" → check the component file

For ADRs, list every "we use X" claim and verify code still uses X.

For the conventions hub, list every "when you add X, do Y" workflow and verify the steps still match the project structure.

### 2. Derive ground truth from code

For each fact, find the authoritative source:

| Doc claim | Authoritative source |
|---|---|
| Endpoint exists / shape | Controller file + DTO files (or OpenAPI) |
| Entity columns | Entity class + migration |
| Manager dependencies | Constructor parameter list |
| Component props | TypeScript type definition |
| Store shape | Store definition file |
| File tree | `tree -L 3 src/` output |
| Job schedule | CRON expression in deployment config |
| Env var | appsettings.json keys + actual code reads |

### 3. Classify each mismatch

| Mismatch type | What to do |
|---|---|
| **Code is newer (most common)** | Update the doc. List in sync report. |
| **Doc is newer** (e.g. doc claims a feature that doesn't exist yet) | Investigate. Likely a DISCREPANCY (planned-but-not-built or doc was aspirational). |
| **Both wrong** (doc claims behavior; code is a stub) | DISCREPANCY entry. Do **not** silently make the code match the doc. |
| **Doc has incorrect example syntax** | Fix the example. Run it to verify. |
| **Doc references file that no longer exists** | Find the new path or remove the reference. |

### 4. Regenerate `tree.md`

```bash
tree -L 3 --gitignore src/ > docs/architecture/tree.md
```

(Add a heading and a regeneration note at the top after running.)

### 5. Update CHANGELOG

Add a single entry under `[Unreleased]`:

```markdown
### Documentation
- Sync pass YYYY-MM-DD — see DOCS_SYNC_REPORT.md
```

### 6. Write the sync report

See `assets/sync-report-template.md`. Structure:

```markdown
# Documentation Sync Report

**Date**: YYYY-MM-DD
**Source of truth**: Code in `src/`
**Scope**: <which docs were audited>

---

## Files Modified

### 1. docs/api/endpoints.md
- **Added** N new endpoint sections: <list>
- **Updated** ResponseDto X to include new field
- **Removed** deprecated endpoint Y

### 2. docs/database/entities.md
- **Added** Z: column foo, column bar
- **Added** new entity Q (full table definition)
- **Marked** field W as OBSOLETE

[continue for each file changed]

---

## Files Verified (no changes)

- docs/architecture/dependencies.md
- docs/adr/* (immutable)

---

## DISCREPANCIES added

- "<title>": code stub doesn't match documented behavior
- "<title>": planned feature, not yet built

---

## Sources used

- src/Api/Controllers/* (12 files)
- src/Persistence/Migrations/* (most recent migration: AddXyz)
- Scalar OpenAPI export at /openapi/v1.json
```

### 7. Commit and PR

```bash
git add docs/
git commit -m "chore(docs): sync pass YYYY-MM-DD"
git push origin chore/docs-sync-YYYY-MM-DD
```

PR title: `chore(docs): sync pass YYYY-MM-DD`. Reviewers check that no code changed in the diff.

## What NOT to do during a sync pass

- **Do not change code.** If you find a bug, file an issue and add a DISCREPANCY entry. Code changes go in a separate PR.
- **Do not edit ADRs.** They are immutable. If an ADR's claim is now false, write a superseding ADR — but that's a separate decision, not part of a sync pass.
- **Do not add new ADRs.** Same reason.
- **Do not delete CHANGELOG history.** Append only.
- **Do not "improve" prose unrelated to the audit.** Stay focused on factual sync. Prose polish is a separate PR.

## Common findings

After a few sync passes you'll notice patterns:

- **Endpoint counts drift fastest.** Add one without updating endpoints.md and the gap compounds.
- **Field additions are silent.** New columns / props get added to entities and components without doc updates.
- **Manager / module dependency lists rot.** New cross-module calls aren't reflected.
- **CHANGELOG lags.** Multiple changes get rolled into one vague entry, or `[Unreleased]` accumulates for months.
- **DISCREPANCIES gets stale on the other end** — old entries describe bugs that were quietly fixed.

A sync pass also revisits DISCREPANCIES: for each entry, check if it's still true. Mark resolved ones as `**Status**: Resolved YYYY-MM-DD` (and remove them after one cycle if you like a clean file).

## Tooling that helps

- A script that diffs `OpenAPI.json` against `endpoints.md` (parse both, compare endpoint counts and shapes)
- A script that emits `entities.md` from migrations
- A pre-commit hook that fails if a new file under `src/Controllers/` lacks a corresponding entry in `endpoints.md`
- CI that regenerates `tree.md` and fails if it differs from the committed version (forces sync at PR time)

These are all optional. Manual passes are fine and often clearer.

## Where to read next

- Sync report template: `assets/sync-report-template.md`
- Discrepancies template: `assets/discrepancies-template.md`
- Changelog conventions: `assets/changelog-template.md`
