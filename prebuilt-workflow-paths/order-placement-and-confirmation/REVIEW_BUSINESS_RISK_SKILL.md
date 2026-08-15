---
name: review-order-placement-risk
description: Review customer, revenue, permission, privacy, and operational risks in Order Placement and Confirmation. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Order Placement and Confirmation Risk

Review entry, amount or quantity, authorization, state, timing, concurrency, external effects, retry, recovery, privacy, and support paths. Prioritize:
- Duplicate order — Concurrency, retries, or lost responses create repeated purchases
- Wrong items or total — The committed order differs from the accepted checkout snapshot
- Payment–order divergence — Money moves without an order or an order confirms without required payment
- Inventory–order divergence — The order confirms without stock or holds stock without a valid order
- Unauthorized order — Another account or tenant controls checkout or destination
- Stale checkout — Expired price, promotion, availability, terms, or address is committed
- False confirmation — Customer receives success while fulfilment prerequisites are missing
- Personal-data exposure — Addresses, customer data, pricing, tokens, or internal decisions reach unsafe logs

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition. Also state Required Skills: the specific developer expertise (for example, programming language, framework or library, database technology, authentication/authorization, concurrency, idempotency, transaction management, webhook handling, queue processing, caching, external integration, API design, or infrastructure/deployment concern) needed to understand and fix the risk. Derive Required Skills only from the trigger, behavior, and affected code or workflow already identified for that risk; do not invent technologies or expertise the evidence does not support, and keep the list concise. If no specialised expertise beyond general application development is evident, say so instead of guessing.

