---
name: implement-order-placement
description: Implement or modify Order Placement and Confirmation. Use when adding or changing validation, authorization, state transitions, financial or inventory effects, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement Order Placement and Confirmation

Confirm:
- Who may place orders for an account, tenant, seller, or guest checkout
- Authoritative item, price, discount, tax, shipping, currency, and address snapshot
- Quote, cart, promotion, and inventory-hold lifetime
- Whether payment or reservation must complete before order commit
- Order id, number, and idempotency policy
- Partial availability, split seller, split shipment, and backorder policy
- Terms, consent, age, region, export, and product eligibility checks
- How uncertain payment or inventory outcomes affect confirmation
- Customer confirmation, receipt, fulfilment, and merchant-notification timing
- Abuse, order velocity, privacy, audit, monitoring, and manual review

Follow project conventions and protect:
- One ready checkout must create at most one intended order
- The committed order must preserve the accepted item and financial snapshot
- Actor, account, tenant, merchant, address, and checkout ownership must be enforced
- Order totals and currency must remain reproducible
- Payment and inventory prerequisites must follow explicit confirmation policy
- Retries and replays must not duplicate orders or downstream effects
- Order, payment, inventory, fulfilment, and confirmation must converge
- Customer and transaction data must remain protected

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

