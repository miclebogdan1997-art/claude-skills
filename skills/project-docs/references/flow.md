# Writing Flow Docs

A flow doc is the **narrative** of a multi-step runtime process: a webhook chain, an auth flow, an onboarding sequence, a job pipeline, a payment loop. It uses an ASCII sequence diagram as its spine.

## When to write one

- A process crosses 3+ layers or services
- A process has branches that affect outcome (success vs. retry vs. dead-letter)
- A process is triggered by something other than a direct user action (webhooks, CRON, queue messages)
- A process has side effects worth tracing (DB writes, external API calls, cache invalidations)

If the process is one function call, you don't need a flow doc — a docstring is enough.

## Standard structure

```markdown
# <Feature> Flow

## Entry point

What triggers this flow. The exact route, event, or invocation.

## Sequence

ASCII sequence diagram (see conventions below).

## Branches

Decision points that split the flow. One sub-section per branch.

## Side effects

DB writes, external API calls, cache invalidations, queue pushes,
emails sent, files written. Listed explicitly.

## Exit conditions

Success state. Failure states. What the caller observes for each.

## Edge cases

Race conditions, idempotency notes, retry behavior, what happens
if a downstream service is down.
```

## ASCII sequence diagram conventions

Vertical layout. One step per box (or single line). `|` and `v` for arrows.

### Linear sequence

```text
Client sends request
       |
       v
POST /api/bookings
       |
       v
BookingsController.Create()
       |
       v
BookingManager.CreateBookingAsync()
       |
       v
AvailabilityEngine.IsSlotFree()
       |
       v
BookingAccessor.InsertAsync()
       |
       v
Returns 201 Created
```

### Branches (if / else)

```text
ConversationManager.HandleMessage()
       |
       v
Has active conversation?
       |
       +--no--> Create new conversation
       |          |
       |          v
       +-yes----> Continue existing conversation
                   |
                   v
              (next step)
```

### Loops

```text
While unprocessed messages remain:
       |
       v
   Pop message
       |
       v
   Process
       |
       v
   ACK or NACK
       |
       v
   (back to top)
```

### Parallel paths

```text
WebhookManager.HandleStripeWebhook()
       |
       +--->  StripeAccessor.VerifySignature()
       |
       +--->  TenantAccessor.GetByStripeCustomerId()
       |
       v
(both must succeed)
       |
       v
   Update tenant subscription state
```

### Multi-layer expansion

When a single step expands into a sub-flow, indent it inline:

```text
ConversationManager.HandleWhatsAppMessageAsync()
       |
       +----------------------------------------------------------+
       |                                                          |
       v                                                          |
  1. Load tenant + config                                         |
       |                                                          |
       v                                                          |
  2. ClientAccessor.GetOrCreateByPhoneAsync()                     |
     Creates client record if first contact                       |
       |                                                          |
       v                                                          |
  3. ConversationAccessor.GetActiveByPhoneAsync()                 |
     Find active WhatsApp conversation                            |
     Not found -> create new conversation                         |
       ExpiresAt = now + 24 hours                                 |
       |                                                          |
       v                                                          |
       |                                                          |
       +----------------------------------------------------------+
       |
       v
  Returns response
```

### Comments / annotations

Indent under the step, no arrow:

```text
TwilioAccessor.ValidateWebhookSignature()
  Uses global Twilio auth token (per-tenant credentials removed
  in SplitTenantTwilioConfiguration migration)
  Invalid -> log warning + return INVALID_SIGNATURE
       |
       v
  (next step)
```

## Why ASCII over Mermaid

- Renders in any terminal, any markdown viewer, any plain text editor
- Diffs cleanly (Mermaid changes can be invisible in PR diffs)
- Survives migrations between docs platforms
- Forces simplicity — if you can't fit it in ASCII, the flow is too complex and needs splitting
- AI agents read it natively — no rendering layer between them and the structure

## Side effects section

Be explicit. Future readers want to know what state changed:

```markdown
## Side effects

- **DB writes**: Bookings (1 row insert), Clients (upsert)
- **External calls**: Twilio.SendMessage (1 outbound WhatsApp), Google Calendar.Insert (if staff has GCal sync)
- **Cache invalidations**: `availability:{staffId}:{date}` (in Redis)
- **Audit log**: writes to `BookingAuditLog` table
- **Emails**: confirmation email to client.email if set
```

## Exit conditions section

For each terminal state, what does the caller see?

```markdown
## Exit conditions

| Outcome | Status | Body | Side effects committed? |
|---|---|---|---|
| Booking created | 201 | BookingResponse | Yes |
| Slot taken | 409 | ProblemDetails (CONFLICT) | No |
| Validation failed | 422 | ProblemDetails (VALIDATION_FAILED) | No |
| Staff unavailable | 422 | ProblemDetails (NOT_WORKING_DAY) | No |
| Unhandled error | 500 | ProblemDetails (generic) | Partial — see compensation notes |
```

## Common mistakes

- **Pasting code instead of summarizing.** A flow doc is the story; the code is the script. Reference file paths and method names, don't paste 50 lines.
- **Skipping branches.** If a step can fail, document what happens on failure. Otherwise the doc is a happy-path lie.
- **Hidden state.** If step 3 reads from cache and step 5 writes to cache, both reads and writes appear in the diagram.
- **No entry point.** "How does this start?" must be answered in the first 3 lines.
- **Mixing two flows.** If "WhatsApp message arrives" and "voice call arrives" share 80% of the sequence, write **two** docs that cross-reference. Don't merge them and use giant if-branches.

## Where to read next

- Template: `assets/flow-template.md`
- After writing the flow, update CHANGELOG and (if relevant) link from the conventions hub's "context files per feature area" table.
