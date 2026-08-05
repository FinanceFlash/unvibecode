# Retry and Recovery Guide

## Partial failures
- Booking commits but capacity conversion fails
- Capacity commits but booking record fails
- Payment succeeds but booking commit fails
- Booking commits but provider calendar rejects or times out
- Booking confirms but reminder or customer message fails
- Commit succeeds but the client response is lost

## Recovery rules
- Use request, hold, and booking idempotency identities consistently.
- Re-read booking, hold, capacity, payment, provider, and trusted-time state before retrying.
- Never create a second booking solely because confirmation or response was lost.
- Compensate capacity or payment only under explicit current-state policy.
- Reconcile booking, capacity, payment, provider calendar, reminders, and customer communication.

