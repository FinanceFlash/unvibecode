# Engineering Guide

## Trace the implementation
1. Renewal scheduler, manual renew, cancel, reverse, reactivate, grace, terminate, and provider-callback entry points
2. Actor, owner, tenant, account, plan, subscription-state, and permission checks
3. Billing timezone, period, price, currency, tax, invoice, and payment-method resolution
4. Renewal and cancellation models, idempotency, uniqueness, versioning, and concurrency controls
5. Payment request, provider status, timeout, retry handoff, and uncertain result
6. Subscription period, grace, cancellation, reactivation, and terminal-state transitions
7. Entitlement, seat, session, API key, data, invoice, and notification effects
8. Audit, privacy, monitoring, reconciliation, support tools, and tests

## Rules the code should protect
- One subscription period must produce at most one successful renewal
- Cancellation and renewal must bind the intended account, tenant, subscription, and version
- Trusted time must determine renewal, grace, and cancellation boundaries
- Paid access must remain until the written effective boundary
- Terminated access must be released consistently across all entitlement surfaces
- Uncertain payment must not cause duplicate billing or premature termination
- Concurrent and replayed actions must converge on one subscription state
- Billing and personal data must remain protected

## Build or change safely
1. Confirm product decisions before relying on framework or provider defaults.
2. Follow existing authorization, financial-state, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, object, amount or quantity, version, state, and scope.
4. Enforce permission, current-state, uniqueness, ordering, and time rules at the write.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep money, access, order, and inventory inconsistency visible and repairable.
7. Add the core 20 tests.

