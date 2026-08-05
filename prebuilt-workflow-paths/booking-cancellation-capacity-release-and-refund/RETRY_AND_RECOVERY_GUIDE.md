# Retry and Recovery Guide

## Partial failures
- Booking cancels but capacity release fails
- Capacity releases but booking state does not commit
- Cancellation commits but refund request fails
- Local cancellation commits but provider cancellation fails
- Cancellation commits but waitlist or notification fails
- Cancellation succeeds but the client response is lost

## Recovery rules
- Use booking, cancellation, and idempotency identities consistently.
- Re-read booking, provider, capacity, payment, refund, and trusted-time state before retrying.
- Never repeat capacity release or refund handoff solely because a response was lost.
- Make provider disagreement and incomplete customer outcomes visible.
- Reconcile booking, capacity, provider, waitlist, payment, refund, and communication.

