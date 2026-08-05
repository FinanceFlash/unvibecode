# Engineering Guide

## Trace the implementation
1. Place-order, guest checkout, confirmation, status, cancellation-on-failure, and support entry points
2. Customer, guest, account, tenant, merchant, region, product, and order permission checks
3. Cart or checkout snapshot, item, variant, quantity, price, discount, tax, shipping, currency, address, and terms validation
4. Order model, order number, idempotency, uniqueness, transaction, version, and concurrency controls
5. Payment prerequisite, attempt reference, uncertain result, and compensation policy
6. Inventory reservation, expiry, availability, and compensation handoff
7. Fulfilment, ledger, receipt, notification, and merchant effects
8. Audit, privacy, monitoring, reconciliation, support tools, and tests

## Rules the code should protect
- One ready checkout must create at most one intended order
- The committed order must preserve the accepted item and financial snapshot
- Actor, account, tenant, merchant, address, and checkout ownership must be enforced
- Order totals and currency must remain reproducible
- Payment and inventory prerequisites must follow explicit confirmation policy
- Retries and replays must not duplicate orders or downstream effects
- Order, payment, inventory, fulfilment, and confirmation must converge
- Customer and transaction data must remain protected

## Build or change safely
1. Confirm product decisions before relying on framework or provider defaults.
2. Follow existing authorization, financial-state, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, object, amount or quantity, version, state, and scope.
4. Enforce permission, current-state, uniqueness, ordering, and time rules at the write.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep money, access, order, and inventory inconsistency visible and repairable.
7. Add the core 20 tests.

