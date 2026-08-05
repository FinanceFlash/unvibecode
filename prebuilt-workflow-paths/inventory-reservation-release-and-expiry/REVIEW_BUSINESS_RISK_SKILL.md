---
name: review-inventory-reservation-risk
description: Review customer, revenue, permission, privacy, and operational risks in Inventory Reservation, Release, and Expiry. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Inventory Reservation, Release, and Expiry Risk

Review entry, amount or quantity, authorization, state, timing, concurrency, external effects, retry, recovery, privacy, and support paths. Prioritize:
- Overselling — Concurrent reservations allocate more stock than permitted
- Stranded inventory — Expired, cancelled, or failed orders keep stock unavailable
- Negative or inflated quantity — Duplicate reserve, release, or conversion corrupts counts
- Cross-order inventory theft — Another actor or order consumes or releases a reservation
- Premature expiry — A valid customer loses stock before the promised boundary
- Late release or conversion — Stale jobs undo committed fulfilment or revive stock
- Multi-location inconsistency — Databases, caches, sellers, or warehouses disagree
- Reservation hoarding — Automated demand blocks scarce stock and harms real customers

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition.

