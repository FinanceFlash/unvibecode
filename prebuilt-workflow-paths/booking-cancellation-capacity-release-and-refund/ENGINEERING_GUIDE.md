# Engineering Guide

## Trace the implementation
1. Cancel, provider-cancel, administrative cancel, status, compensation, and support entry points
2. Customer, account, tenant, provider, booking-owner, and permission checks
3. Booking status, version, slot, timezone, cut-off, reason, fee, penalty, and refund-basis evaluation
4. Cancellation model, idempotency, uniqueness, transaction, versioning, and concurrency controls
5. Exact capacity release, waitlist handoff, and stale-release protection
6. Refund-request creation and payment-reference binding
7. Provider cancellation, timeout, callback, customer and provider notification
8. Audit, privacy, abuse, monitoring, reconciliation, support tools, and tests

## Rules the code should protect
- Only an authorized actor may cancel a current eligible booking
- Cancellation policy must use trusted booking state, time, timezone, and version
- Capacity release must equal unused committed capacity and happen exactly once
- Refund request must bind one cancellation, payment, customer, and policy basis
- Cancellation must not undo completed, checked-in, or superseded service outside explicit policy
- Retries and replays must not duplicate release, refund, waitlist, or notification effects
- Booking, provider, capacity, payment, refund, and communication must converge
- Customer and provider data must remain protected

## Build or change safely
1. Confirm product decisions before relying on framework or provider defaults.
2. Follow existing authorization, state, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, object, time, quantity or money, version, state, and scope.
4. Enforce permission, current-state, uniqueness, ordering, and time rules at the write.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep capacity, booking, payment, and provider inconsistency visible and repairable.
7. Add the core 20 tests.

