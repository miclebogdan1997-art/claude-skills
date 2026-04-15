# Documentation Sync Report

**Date**: YYYY-MM-DD
**Source of truth**: Code in `src/` directory
**Reference**: `docs/CHANGELOG.md` used as pointer only
**Scope**: <which docs were audited — "all" or list>

---

## Files Modified

### 1. docs/<path>/<file>.md
- **Added** <N> new <thing> sections: <comma-separated list>
- **Updated** <thing> to include <change>
- **Removed** <deprecated thing>

### 2. docs/<path>/<file>.md
- **Added** <Entity X>: <columns added>
- **Added** new entity <Y> (full table definition)
- **Marked** <field Z> as OBSOLETE

### 3. docs/<path>/<file>.md
- **Updated** <count> N → M (<reason for delta>)
- **Added** <new item> to <table>

### 4. docs/architecture/tree.md
- **Regenerated** from actual filesystem
- Now includes <new top-level items>

[Continue for each file changed]

---

## Files Verified (no changes)

- `docs/<path>/<file>.md`
- `docs/<path>/<file>.md`
- `docs/adr/*` (immutable — only checked status accuracy)

---

## DISCREPANCIES added

- "<title>": <one-line summary>
- "<title>": <one-line summary>

## DISCREPANCIES resolved

- "<title>": <how it was resolved>

---

## Sources used

- `<path>/<file or pattern>` (<count> files)
- `<path>/<file or pattern>` (most recent: <ref>)
- `<external source if any, e.g. OpenAPI export>`

---

## Sync pass notes

<Anything noteworthy — recurring drift patterns, suggestions for
automation, areas that need a follow-up sync sooner than usual.>

<!--
After saving:
1. Add an entry to docs/CHANGELOG.md under [Unreleased] → ### Documentation:
   "Sync pass YYYY-MM-DD — see DOCS_SYNC_REPORT.md"
2. Commit on branch: chore/docs-sync-YYYY-MM-DD
3. Open PR titled: "chore(docs): sync pass YYYY-MM-DD"
4. Reviewer confirms zero code changes in the diff
-->
