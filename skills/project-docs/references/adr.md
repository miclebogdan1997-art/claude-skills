# Writing ADRs

An Architecture Decision Record captures **one** decision at the moment it was made, and what trade-offs were accepted.

## What an ADR is for

- Recording why a non-obvious choice was made
- Giving future readers (humans and agents) the rationale without spelunking through chat logs and PR descriptions
- Making it cheap to change a decision later — the next ADR explicitly supersedes the old one

## What an ADR is NOT for

- Tutorials ("how to use Postgres")
- Reference material ("our table schema")
- Process docs ("how we do code review")
- Trivial choices ("we use 2-space indent") — those go in the conventions hub
- Multi-decision essays — split them into multiple ADRs

If you can't write the decision in one sentence, it's probably more than one ADR.

## Required structure

```markdown
# ADR-NNN: <short title in title case>

**Status**: Proposed | Accepted | Superseded by ADR-NNN | Deprecated
**Date**: YYYY-MM-DD
**Prompt**: <optional — N (Description), useful for AI-assisted projects>

## Context

What forces are at play? What constraints? What were the candidate
options? Be concrete about the trade space — list 2-4 alternatives
that were seriously considered.

## Decision

The chosen option, stated declaratively. Then the reasons, as a
short bullet list. Then trade-offs accepted, as a separate bullet
list.

## Consequences

What follows from this decision. Use sub-headings:

**Positive**:
- ...

**Negative**:
- ...

(Or merge into a single "Trade-offs" list — pick one style and stick
with it across all your ADRs.)
```

## Numbering

Zero-padded sequential per scope:

- `ADR-001-<slug>.md`, `ADR-002-<slug>.md`, …
- Slug is kebab-case, 1-4 words, content-bearing (`idesign-architecture`, not `architecture-1`)
- Per-scope: backend and frontend can each restart at 001 if they live under separate `docs/` trees. Make the scope obvious from the directory.

Never renumber. If ADR-003 is wrong, write ADR-007 that supersedes it; mark ADR-003's status as `Superseded by ADR-007`.

## Status lifecycle

```
Proposed ──accept──> Accepted ──supersede──> Superseded by ADR-NNN
   │                     │
   └────reject───────────┴────deprecate───> Deprecated
```

- **Proposed**: under discussion, not yet binding
- **Accepted**: binding; code is expected to follow it
- **Superseded by ADR-NNN**: replaced by a newer decision; keep the file, update the status line
- **Deprecated**: no longer relevant (e.g. the subsystem was removed); keep the file for history

## The Prompt field (optional but useful)

For AI-assisted development, add a `**Prompt**:` line tracing which prompt or session the ADR came from:

```
**Prompt**: 2 (API Client, Stores, TanStack Query)
```

Why: when you're 30 prompts deep into a project, it's invaluable to see "this decision came from the prompt where I asked for the state-management setup." It also makes it obvious which ADRs were retroactive vs. captured in the moment.

For human-only projects, replace with `**PR**: #NNN` or `**Source**: <link>` or omit entirely.

## Common mistakes

- **Writing ADRs for things that aren't decisions.** "We use TypeScript" is not an ADR if there was no real alternative considered. Put it in the conventions hub.
- **Editing an Accepted ADR to reflect later changes.** Never. Write a new ADR.
- **Single-option Context sections.** If you don't list alternatives, the rationale is unfalsifiable. Force yourself to list at least one rejected option, even if it's "do nothing."
- **Marketing-style Decision sections.** "We chose X because it is fast, scalable, and modern." → Replace with concrete claims tied to your constraints.
- **Forgetting to update INDEX.md.** Every new ADR needs a row in the registry.
- **Including code samples longer than 10 lines.** ADRs are about the decision, not the implementation. Reference the code path instead.

## Example: a strong ADR

```markdown
# ADR-006: JWT Carries userId Only; Tenant via X-Tenant-Id Header

**Status**: Accepted
**Date**: 2026-04-01

## Context

Users belong to multiple tenants. We need every request to know
both the user identity and which tenant context it's operating in.
Options:

1. Embed tenantId in the JWT — one token per (user, tenant) pair
2. Embed list of tenantIds in the JWT — one token, server picks
3. JWT has userId only; tenant comes from a request header

## Decision

Option 3. JWT contains userId + email. Tenant context comes from
`X-Tenant-Id` request header. A global filter validates the user
belongs to the specified tenant.

Reasons:
- One token works across all of a user's tenants — no token swap on switch
- Tokens stay small (no tenant list to grow with membership)
- Switching tenant is a header change, not a re-auth round-trip

Trade-offs:
- Every protected endpoint needs the tenant validation filter
- Clients must know to send X-Tenant-Id (we document this in api/)

## Consequences

**Positive**:
- Tenant switch is instant; no re-login flow
- Token size is bounded regardless of memberships

**Negative**:
- Header injection is the new attack surface — validated server-side
- Endpoints that legitimately don't need a tenant must opt out
  via [SkipTenantCheck]
```

Note what makes this strong: three alternatives listed, decision is one sentence, reasons are concrete (not "modern" or "scalable"), trade-offs are honest.

## Where to read next

- Template to copy: `assets/adr-template.md`
- INDEX.md format: `assets/index-template.md`
- After writing the ADR, update CHANGELOG (see `assets/changelog-template.md`)
