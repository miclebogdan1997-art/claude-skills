# Discrepancies

Known gaps between code and docs, stub implementations, planned-but-not-built features, and bugs that have a documented workaround.

This file is **healthy** — an empty DISCREPANCIES.md usually means nobody is auditing. Aim to keep it accurate, not empty.

---

## How to add an entry

```markdown
## <short-title>
- **What docs say**: <claim from the docs>
- **What code does**: <observed behavior>
- **Status**: Bug | Stub | Documentation gap | Planned
- **Resolution**: Fix code | Fix docs | Track as issue #NNN | Won't fix
- **Found**: YYYY-MM-DD
```

Resolved entries can either:
- Be deleted (clean file approach), or
- Be moved under `## Resolved` with a `**Resolved**: YYYY-MM-DD` line

Pick one approach and stick with it.

---

## Active

<!-- Add new entries here -->

## Example entries

<!-- Delete this section once you have real entries -->

## Voice webhook does not create bookings
- **What docs say**: voice booking flow creates a booking on call end
- **What code does**: webhook handler is a stub that logs but does not call BookingManager
- **Status**: Stub
- **Resolution**: Track as issue #42
- **Found**: 2026-04-01

## Stripe only has Solo plan configured
- **What docs say**: three subscription tiers (Solo, Team, Business)
- **What code does**: only Solo plan price ID exists in config
- **Status**: Documentation gap
- **Resolution**: Fix docs (drop Team and Business) until Stripe products are created
- **Found**: 2026-04-03

## Register creates tenant as Active instead of PendingPayment
- **What docs say**: new tenants start in PendingPayment until first invoice clears
- **What code does**: AuthManager.RegisterAsync creates tenant with Status = Active
- **Status**: Bug
- **Resolution**: Fix code (change default), then update CHANGELOG
- **Found**: 2026-04-05

---

## Resolved

<!-- Move resolved entries here, or delete them -->
