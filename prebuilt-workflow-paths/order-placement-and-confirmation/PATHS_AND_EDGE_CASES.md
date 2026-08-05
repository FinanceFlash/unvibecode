# Paths and Edge Cases

## Supported paths
- Authenticated customer order
- Guest checkout order
- Order with completed payment prerequisite
- Order with permitted pending payment
- Order using an active inventory hold
- Multi-item, seller, or shipment order where explicitly supported
- Rejected or expired checkout
- Uncertain commit, reconciliation, compensation, and manual repair

## Normal paths
- A valid checkout creates one immutable confirmed order
- The committed order retains the exact accepted item and financial snapshot
- Payment, inventory, fulfilment, and confirmation references attach to the same order

## Denied paths
- Required customer, item, address, price, currency, terms, or checkout data is missing or invalid
- Quote, promotion, inventory hold, or checkout has expired or changed materially
- The actor cannot order for the account, tenant, seller, region, or product
- Payment or inventory policy prevents confirmation

## Timing, concurrency, and boundaries
- Two order submissions arrive together
- Quote or inventory hold expires exactly during commit
- Cart, address, price, or customer data changes after snapshot
- Payment or order commit succeeds but the response is lost
- Late payment or inventory result arrives after rejection or cancellation

Cover valid, invalid, duplicate, expired, stale, replayed, repeated, simultaneous, partially completed, unauthorized, and recovery outcomes.

