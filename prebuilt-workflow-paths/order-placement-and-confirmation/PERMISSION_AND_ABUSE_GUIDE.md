# Permission and Abuse Guide

## Permission boundaries
- One ready checkout must create at most one intended order
- The committed order must preserve the accepted item and financial snapshot
- Actor, account, tenant, merchant, address, and checkout ownership must be enforced
- Order totals and currency must remain reproducible
- Payment and inventory prerequisites must follow explicit confirmation policy

## Misuse paths
- Duplicate order — Concurrency, retries, or lost responses create repeated purchases
- Wrong items or total — The committed order differs from the accepted checkout snapshot
- Payment–order divergence — Money moves without an order or an order confirms without required payment
- Inventory–order divergence — The order confirms without stock or holds stock without a valid order
- Unauthorized order — Another account or tenant controls checkout or destination
- Stale checkout — Expired price, promotion, availability, terms, or address is committed
- False confirmation — Customer receives success while fulfilment prerequisites are missing
- Personal-data exposure — Addresses, customer data, pricing, tokens, or internal decisions reach unsafe logs

Protect actor identity, tenant scope, authoritative business objects, financial data, provider proof, support tools, and audit records. Deny uncertain ownership or permission.

