# Engineering Guide

## Trace the implementation
1. Reserve, extend, convert, release, cancel, expire, adjust, and status entry points
2. Actor, account, tenant, order, item, variant, location, seller, and ownership checks
3. Authoritative on-hand, available, reserved, committed, safety-stock, and unit calculations
4. Reservation model, idempotency, uniqueness, version, lock, transaction, and consistency controls
5. Multi-line, partial, backorder, location, lot, serial, and allocation logic
6. Trusted time, expiry job, extension, queue claim, and stale-job handling
7. Order, payment, fulfilment, cancellation, return, and reconciliation effects
8. Audit, abuse, monitoring, manual adjustment, support tools, and tests

## Rules the code should protect
- Inventory quantities must be conserved across available, reserved, and committed states
- One intended request must not create duplicate reservations
- Every reservation must bind owner, tenant, order, item, location, quantity, unit, and expiry
- Concurrent requests must not exceed explicit available or oversell policy
- Release, expiry, and conversion must apply exactly once from a valid state
- Trusted time and current version must govern expiry and extension
- Stale jobs and replays must not undo later inventory state
- Reservation and operational data must remain protected

## Build or change safely
1. Confirm product decisions before relying on framework or provider defaults.
2. Follow existing authorization, financial-state, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, object, amount or quantity, version, state, and scope.
4. Enforce permission, current-state, uniqueness, ordering, and time rules at the write.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep money, access, order, and inventory inconsistency visible and repairable.
7. Add the core 20 tests.

