# Product and Business Guide

## Boundary
Starts when a checkout is ready to place with an authoritative customer, item snapshot, price, address, and payment policy. Ends when one immutable order is rejected, committed and confirmed, or remains explicitly uncertain with payment, inventory, fulfilment, and customer communication reconciled.

## People and systems
- Customer or authorized purchaser
- Checkout, cart, and order services
- Pricing, tax, promotion, and address services
- Payment and inventory services
- Fulfilment and notification services
- Merchant, support, finance, and operations teams

## Things created or changed
- Checkout or cart snapshot
- Customer, guest identity, account, tenant, and destination
- Product, variant, quantity, seller, and line-item snapshot
- Price, discount, tax, shipping, total, and currency snapshot
- Order, order number, idempotency key, and terms acceptance
- Payment and inventory references
- Fulfilment request, confirmation, receipt, and audit record

## Stages
- Checkout: ready → placing → converted, rejected, expired, or uncertain
- Order: absent → committing → confirmed, payment pending, on hold, failed, or cancelled
- Payment and inventory references: required → linked, pending, failed, or exception
- Fulfilment handoff: absent → requested → accepted or failed

## Product decisions
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

## Happy paths
- A valid checkout creates one immutable confirmed order
- The committed order retains the exact accepted item and financial snapshot
- Payment, inventory, fulfilment, and confirmation references attach to the same order

## Negative paths
- Required customer, item, address, price, currency, terms, or checkout data is missing or invalid
- Quote, promotion, inventory hold, or checkout has expired or changed materially
- The actor cannot order for the account, tenant, seller, region, or product
- Payment or inventory policy prevents confirmation

## Edge cases
- Two order submissions arrive together
- Quote or inventory hold expires exactly during commit
- Cart, address, price, or customer data changes after snapshot
- Payment or order commit succeeds but the response is lost
- Late payment or inventory result arrives after rejection or cancellation

## Acceptance criteria
1. Only an eligible ready checkout may create an order
2. Customer, tenant, merchant, items, quantities, prices, currency, address, and terms must bind to one snapshot
3. One checkout and idempotency key must not create duplicate orders
4. Order totals must equal the accepted line, discount, tax, shipping, and rounding components
5. Stale quotes, holds, promotions, and mutable cart data must not silently change the committed order
6. Payment and inventory prerequisites must follow explicit commit and confirmation policy
7. Order, payment, inventory, fulfilment, ledger, and customer confirmation must converge
8. Repeated, simultaneous, or lost-response execution must return one order outcome
9. Personal data, addresses, prices, tokens, and internal risk information must remain protected
10. Partial failure must remain visible, auditable, and repairable

## Business risks
| Risk | Business consequence |
|---|---|
| Duplicate order | Concurrency, retries, or lost responses create repeated purchases |
| Wrong items or total | The committed order differs from the accepted checkout snapshot |
| Payment–order divergence | Money moves without an order or an order confirms without required payment |
| Inventory–order divergence | The order confirms without stock or holds stock without a valid order |
| Unauthorized order | Another account or tenant controls checkout or destination |
| Stale checkout | Expired price, promotion, availability, terms, or address is committed |
| False confirmation | Customer receives success while fulfilment prerequisites are missing |
| Personal-data exposure | Addresses, customer data, pricing, tokens, or internal decisions reach unsafe logs |

