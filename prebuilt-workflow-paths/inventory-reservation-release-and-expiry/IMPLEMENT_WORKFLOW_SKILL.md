---
name: implement-inventory-reservation
description: Implement or modify Inventory Reservation, Release, and Expiry. Use when adding or changing validation, authorization, state transitions, financial or inventory effects, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement Inventory Reservation, Release, and Expiry

Confirm:
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

Follow project conventions and protect:
- Inventory quantities must be conserved across available, reserved, and committed states
- One intended request must not create duplicate reservations
- Every reservation must bind owner, tenant, order, item, location, quantity, unit, and expiry
- Concurrent requests must not exceed explicit available or oversell policy
- Release, expiry, and conversion must apply exactly once from a valid state
- Trusted time and current version must govern expiry and extension
- Stale jobs and replays must not undo later inventory state
- Reservation and operational data must remain protected

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

