# Writing the Conventions Hub

The conventions hub is the **single file an agent reads first** when working on the project. Standard locations:

- `CLAUDE.md` — Claude Code, Anthropic agents
- `AGENTS.md` — vendor-neutral convention
- `.cursorrules` — Cursor
- `.windsurfrules` — Windsurf

Same content, different filename per tool. Most projects pick one and symlink the others, or duplicate the content (small enough that drift is manageable).

Lives at the **repo root**, not in `docs/`. Agents look for it before they look anywhere else.

## What goes in it

### Required sections

#### 1. What is this project

One paragraph. Plain English. No marketing.

> Multi-tenant SaaS connecting WhatsApp + Voice with an internal booking calendar. Business owners subscribe, configure staff and services, connect their WhatsApp number. Their clients book appointments via WhatsApp or phone call. AI handles the conversation.

#### 2. Tech stack

Bullet list. Versions where they matter. Hosting/runtime details.

```
- Runtime: .NET 10, ASP.NET Core Web API
- ORM: Entity Framework Core, Code First + migrations
- Database: PostgreSQL (Neon serverless)
- Cache: Redis (Upstash)
- Hosting: Azure Container Apps (scale to zero)
- ...
```

#### 3. Architecture

The layering rule, with a small ASCII diagram. **One** sentence per layer max.

```text
Controllers -> Managers -> Engines -> Accessors -> External
Utilities -> any layer
DataContracts -> shared DTOs + enums
```

Plus a STRICT rules block:

```
- Controllers call ONLY Managers
- Managers call Engines + Accessors (limited cross-Manager calls)
- Engines are synchronous pure logic — no DB, no HTTP
- Accessors call DB or external APIs only
- NEVER skip layers
```

#### 4. Solution / project structure

ASCII tree at module level (not file level — that's `tree.md`'s job).

#### 5. Coding standards

Rules that survive across tasks:

- Async patterns
- Error handling (Result<T> vs exceptions)
- Test naming
- Migration location
- Logging convention
- Time zone handling
- Money / decimal handling

#### 6. Workflow rules — "when you add X"

Tables of "when this kind of change happens, do these steps." This is the highest-leverage section because it tells the agent which docs to update.

```markdown
### When you add a new endpoint

1. Add interface method to DataContracts/Interfaces/Managers/
2. Add request/response DTOs
3. Implement in Manager
4. Add controller action
5. Update docs/api/endpoints.md

### When you add a new entity

1. Create entity in Persistence/Entities/
2. Create EF configuration
3. Add DbSet to DbContext
4. Create migration
5. Update docs/database/entities.md
6. Update docs/database/relationships.md
```

#### 7. Before starting any task

Short checklist. Put this near the top — agents read top-down.

```
1. Read CLAUDE.md (this file)
2. Read relevant interface files
3. Read existing implementations of similar features
4. Check DISCREPANCIES.md for known issues
5. Check CHANGELOG.md to understand current version
```

#### 8. Known issues

A short pointer to `docs/DISCREPANCIES.md` plus the 3-5 most load-bearing known issues quoted inline so they show up in the agent's context without needing a second read.

### High-leverage optional sections

#### File naming conventions table

```markdown
| Type | Convention | Example |
|------|-----------|---------|
| Interface | I{Name}{Layer} | IBookingManager |
| Implementation | {Name}{Layer} | BookingManager |
| Request DTO | {Action}{Entity}Request | CreateBookingRequest |
| Response DTO | {Entity}Response | BookingResponse |
| Test class | {Class}Tests | BookingManagerTests |
| Test method | {Method}_{Scenario}_{Expected} | Create_ValidRequest_Returns201 |
```

Saves the agent from inventing names that violate convention.

#### Error code → HTTP status mapping

For any project that uses a Result/Either pattern with error codes:

```markdown
| ErrorCode | HTTP Status |
|-----------|-------------|
| *_NOT_FOUND | 404 |
| VALIDATION_FAILED | 422 |
| INVALID_CREDENTIALS | 401 |
| ACCOUNT_SUSPENDED | 403 |
| * (default) | 500 |
```

#### Sub-agent / parallelization strategy

For AI-assisted multi-agent work, document what can be parallelized vs. what must be sequential:

```markdown
STEP 1 — DataContracts first (blocking — must finish first):
  - Interfaces, DTOs, Enums

STEP 2 — Parallel implementation (run simultaneously):
  - Accessor + tests
  - Engine + tests
  - Manager (after Step 1 + Accessors)

NEVER parallelize:
  - Database migrations (always sequential)
  - DI registration changes
  - appsettings.json
```

#### Context files per feature area

A table mapping feature areas to "the 4-6 files you should read before touching this":

```markdown
**Booking feature**:
- IBookingManager, BookingManager
- IBookingAccessor, BookingAccessor
- IAvailabilityEngine, ISchedulingEngine
- BookingsController
```

#### Git workflow

Branch naming, commit conventions, PR requirements. Critical for agents that might otherwise commit to main.

```markdown
**Never commit or push directly to `master`.**

For every change:
1. git checkout -b feature/<name>
2. Commit on the branch
3. Push and open a PR
4. Merge only through PR review

Branch naming:
- feature/<name>
- fix/<name>
- chore/<name>
```

#### Environment variables

List of env vars the project reads. Agents adding integrations need to know where to register new ones.

#### Scheduled jobs

If the project has CRON or background jobs, list them in a table:

```markdown
| Job | Schedule | Binary arg | Purpose |
|-----|----------|------------|---------|
| ReminderJob | */15 * * * * | reminders | WhatsApp reminders |
```

#### Frontend / sub-project pointer

If the project is a monorepo with separable subprojects, dedicate a section to each, with a pointer to its own conventions hub:

```markdown
## Frontend (MyApp.Web)

The frontend lives in `MyApp.Web/` as an independent Next.js project
with its own package.json, Dockerfile, CI/CD pipeline.

For frontend conventions, see `MyApp.Web/CLAUDE.md` (or
`MyApp.Web/docs/INDEX.md`).
```

## Length and shape

Target: 200-400 lines. If you exceed 500, you've lost the agent — either split into sub-files (one per subproject) or move depth to `docs/`.

The hub is a **table of contents to your project**, not a textbook.

## Common mistakes

- **Drift between hub and docs/.** If the hub says "9 managers" and `architecture/overview.md` says "6 managers", one is wrong. Sync pass should catch this.
- **Project history in the hub.** Belongs in CHANGELOG, not here.
- **Reasoning instead of rules.** Why a decision was made → ADR. What the rule is → hub.
- **Examples that drift from code.** Don't quote method signatures that change every sprint. Quote stable interface shapes only.
- **Marketing-style intros.** "MyProject is a cutting-edge platform leveraging…" → Delete. State what it does in plain words.

## Where to read next

- Template: `assets/conventions-hub-template.md`
- "When you add X" workflows are also summarized in the top-level SKILL.md
