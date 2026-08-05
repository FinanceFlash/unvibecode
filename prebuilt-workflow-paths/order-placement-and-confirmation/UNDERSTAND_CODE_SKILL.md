---
name: understand-order-placement-code
description: Trace and explain Order Placement and Confirmation across an existing codebase. Use when locating entry points, authorization, state, external calls, business effects, retries, recovery, monitoring, and tests.
---

# Understand Order Placement and Confirmation Code

Trace:
1. Place-order, guest checkout, confirmation, status, cancellation-on-failure, and support entry points
2. Customer, guest, account, tenant, merchant, region, product, and order permission checks
3. Cart or checkout snapshot, item, variant, quantity, price, discount, tax, shipping, currency, address, and terms validation
4. Order model, order number, idempotency, uniqueness, transaction, version, and concurrency controls
5. Payment prerequisite, attempt reference, uncertain result, and compensation policy
6. Inventory reservation, expiry, availability, and compensation handoff
7. Fulfilment, ledger, receipt, notification, and merchant effects
8. Audit, privacy, monitoring, reconciliation, support tools, and tests

Explain actors, ownership, amounts or quantities, states, transitions, effects, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.

