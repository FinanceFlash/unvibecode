---
name: write-inventory-reservation-spec
description: Write or review a product specification for Inventory Reservation, Release, and Expiry. Use when defining actors, states, financial or inventory rules, policy decisions, edge cases, acceptance criteria, recovery, or business risks.
---

# Write a Inventory Reservation, Release, and Expiry Specification

Use application-native terms. Decide:
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

Write scope, actors, objects, states, paths, customer and business outcomes, permissions, recovery, privacy, misuse, acceptance criteria, and unanswered decisions.

