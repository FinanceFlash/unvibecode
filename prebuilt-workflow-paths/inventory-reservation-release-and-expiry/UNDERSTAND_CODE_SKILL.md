---
name: understand-inventory-reservation-code
description: Trace and explain Inventory Reservation, Release, and Expiry across an existing codebase. Use when locating entry points, authorization, state, external calls, business effects, retries, recovery, monitoring, and tests.
---

# Understand Inventory Reservation, Release, and Expiry Code

Trace:
1. Reserve, extend, convert, release, cancel, expire, adjust, and status entry points
2. Actor, account, tenant, order, item, variant, location, seller, and ownership checks
3. Authoritative on-hand, available, reserved, committed, safety-stock, and unit calculations
4. Reservation model, idempotency, uniqueness, version, lock, transaction, and consistency controls
5. Multi-line, partial, backorder, location, lot, serial, and allocation logic
6. Trusted time, expiry job, extension, queue claim, and stale-job handling
7. Order, payment, fulfilment, cancellation, return, and reconciliation effects
8. Audit, abuse, monitoring, manual adjustment, support tools, and tests

Explain actors, ownership, amounts or quantities, states, transitions, effects, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.

