# Engineering Guide

## Trace the implementation
1. Confirm, direct-book, provider-accept, status, compensation, and support entry points
2. Customer, account, tenant, provider, resource, attendee, and permission checks
3. Slot, timezone, duration, party size, capacity, quote, terms, hold, and expiry validation
4. Booking model, confirmation number, idempotency, uniqueness, versioning, transaction, and concurrency controls
5. Capacity hold conversion or direct commitment
6. Payment prerequisite, provider calendar request, timeout, and uncertain result
7. Confirmation, reminder, notification, ledger, and operational effects
8. Audit, privacy, abuse, monitoring, reconciliation, support tools, and tests

## Rules the code should protect
- One intended request or hold must create at most one booking
- Committed capacity must remain conserved and within policy
- Booking must bind the intended customer, tenant, provider, resource, slot, timezone, and party size
- Trusted time and current state must govern hold and quote validity
- Payment and provider prerequisites must follow explicit confirmation policy
- Retries and replays must not duplicate booking or capacity effects
- Booking, capacity, payment, provider, and communication must converge
- Customer and provider data must remain protected

## Build or change safely
1. Confirm product decisions before relying on framework or provider defaults.
2. Follow existing authorization, state, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, object, time, quantity or money, version, state, and scope.
4. Enforce permission, current-state, uniqueness, ordering, and time rules at the write.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep capacity, booking, payment, and provider inconsistency visible and repairable.
7. Add the core 20 tests.

