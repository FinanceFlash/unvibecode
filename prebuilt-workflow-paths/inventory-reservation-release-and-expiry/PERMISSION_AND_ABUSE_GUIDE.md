# Permission and Abuse Guide

## Permission boundaries
- Inventory quantities must be conserved across available, reserved, and committed states
- One intended request must not create duplicate reservations
- Every reservation must bind owner, tenant, order, item, location, quantity, unit, and expiry
- Concurrent requests must not exceed explicit available or oversell policy
- Release, expiry, and conversion must apply exactly once from a valid state

## Misuse paths
- Overselling — Concurrent reservations allocate more stock than permitted
- Stranded inventory — Expired, cancelled, or failed orders keep stock unavailable
- Negative or inflated quantity — Duplicate reserve, release, or conversion corrupts counts
- Cross-order inventory theft — Another actor or order consumes or releases a reservation
- Premature expiry — A valid customer loses stock before the promised boundary
- Late release or conversion — Stale jobs undo committed fulfilment or revive stock
- Multi-location inconsistency — Databases, caches, sellers, or warehouses disagree
- Reservation hoarding — Automated demand blocks scarce stock and harms real customers

Protect actor identity, tenant scope, authoritative business objects, financial data, provider proof, support tools, and audit records. Deny uncertain ownership or permission.

