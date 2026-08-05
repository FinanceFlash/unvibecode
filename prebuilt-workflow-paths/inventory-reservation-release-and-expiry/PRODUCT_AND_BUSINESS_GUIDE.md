# Product and Business Guide

## Boundary
Starts when an eligible order or demand requests a quantity of a specific sellable resource. Ends when an exactly-once reservation is active, converted to committed consumption, released, expired, rejected, or visibly requires reconciliation while inventory quantities remain conserved.

## People and systems
- Customer demand or order service
- Inventory reservation service
- Warehouse, store, seller, or capacity owner
- Database, cache, or inventory provider
- Expiry scheduler and queue worker
- Fulfilment and cancellation services
- Operations, support, and audit teams

## Things created or changed
- Product, variant, SKU, location, lot, or capacity unit
- On-hand, available, reserved, committed, and safety-stock quantities
- Reservation, owner, order, line, quantity, idempotency key, and version
- Creation, expiry, extension, release, and conversion time
- Allocation across locations or lots
- Backorder or rejection outcome
- Inventory movement, reconciliation exception, and audit record

## Stages
- Reservation: requested → active → consumed, released, expired, cancelled, rejected, or exception
- Quantity: available → reserved → committed or returned to available
- Order line: awaiting inventory → reserved, partially reserved, backordered, or unavailable
- Expiry job: scheduled → claimed → applied, obsolete, or failed

## Product decisions
- Authoritative inventory source and consistency model
- Reservation owner, tenant, order, item, variant, location, and quantity binding
- Atomic all-lines versus partial allocation policy
- Oversell, backorder, safety-stock, and priority rules
- Reservation lifetime, trusted clock, extension, and maximum duration
- When reservation converts to committed consumption
- Which cancellation, payment, or fulfilment events release inventory
- Multi-location, lot, serial, substitution, and split-allocation policy
- Idempotency, locking, versioning, retry, expiry-worker, and reconciliation policy
- Reservation-rate, hoarding, fairness, monitoring, and manual-adjustment controls

## Happy paths
- Available quantity is reserved once for the intended order
- A valid reservation converts once when the order commits to fulfilment
- Cancellation or expiry releases the exact unused quantity once

## Negative paths
- Item, variant, location, order, owner, or quantity is missing or invalid
- Available inventory is insufficient under policy
- Reservation is expired, released, consumed, cancelled, or owned elsewhere
- An extension, release, or conversion violates current state

## Edge cases
- Two customers request the last unit together
- Reservation converts exactly at expiry
- Release, expiry, and conversion arrive together
- Inventory source or location changes during allocation
- A multi-line reservation partially succeeds

## Acceptance criteria
1. Only an eligible owner and demand may reserve inventory
2. Item, variant, location, tenant, order, line, quantity, unit, and reservation must remain bound
3. Available, reserved, and committed quantities must be conserved and never become invalid
4. Concurrent requests must not oversell beyond explicit policy
5. One reservation request must not create duplicate holds
6. Expired, released, consumed, cancelled, or rejected reservations cannot be reused
7. Release and conversion must change quantity exactly once
8. Expiry and extension must use trusted current state and time
9. Partial multi-line failure must follow explicit atomicity or compensation policy
10. Reservation details, customer references, operational controls, and audit records must remain protected

## Business risks
| Risk | Business consequence |
|---|---|
| Overselling | Concurrent reservations allocate more stock than permitted |
| Stranded inventory | Expired, cancelled, or failed orders keep stock unavailable |
| Negative or inflated quantity | Duplicate reserve, release, or conversion corrupts counts |
| Cross-order inventory theft | Another actor or order consumes or releases a reservation |
| Premature expiry | A valid customer loses stock before the promised boundary |
| Late release or conversion | Stale jobs undo committed fulfilment or revive stock |
| Multi-location inconsistency | Databases, caches, sellers, or warehouses disagree |
| Reservation hoarding | Automated demand blocks scarce stock and harms real customers |

