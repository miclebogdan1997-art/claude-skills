# <Feature> Flow

## Entry point

What triggers this flow. Be exact:
- HTTP route: `POST /api/<path>`
- CRON: `*/15 * * * *` (job binary arg `<arg>`)
- Webhook from <provider>
- User action: clicks `<Button>` in `<Page>`

## Sequence

```text
<First actor> <action>
       |
       v
<Layer 1>.<Method>()
       |
       v
<Layer 2>.<Method>()
  Comment annotating what this step does
       |
       v
<Decision point>
       |
       +--no--> <Path A first step>
       |          |
       |          v
       |       <Path A second step>
       |          |
       |          v
       +-yes----> <Path B first step>
                   |
                   v
              (next step)
```

## Branches

### When <condition>

What happens, what state is committed, what the caller observes.

### When <other condition>

What happens, what state is committed, what the caller observes.

## Side effects

- **DB writes**: `<table>` (insert / update / delete N rows)
- **External calls**: `<Provider>.<Method>` (with what payload, idempotent?)
- **Cache**: invalidates `<key-pattern>`
- **Queue**: pushes to `<queue-name>`
- **Email / SMS / WhatsApp**: sends to `<recipient>` using `<template>`

## Exit conditions

| Outcome | Status / Result | Body / Effect | Side effects committed? |
|---|---|---|---|
| Success | <code> | <shape> | Yes |
| <Failure 1> | <code> | <shape> | No |
| <Failure 2> | <code> | <shape> | Partial — see compensation |

## Edge cases

- **Idempotency**: <are duplicate calls safe? what's the dedupe key?>
- **Retries**: <does the caller retry? with what backoff? are retries safe?>
- **Concurrency**: <what happens if two requests race?>
- **Downstream failure**: <what happens if `<external-service>` is down?>
