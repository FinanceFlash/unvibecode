---
name: review-booking-confirmation-risk
description: Review customer, revenue, permission, privacy, and operational risks in Booking Confirmation and Capacity Commitment. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Booking Confirmation and Capacity Commitment Risk

Review entry, quantity or money, authorization, state, timing, concurrency, external effects, retry, recovery, privacy, and support paths. Prioritize:
- Double booking — Concurrent confirmations commit the same exclusive capacity
- Wrong slot or resource — Timezone, identity, or mapping errors confirm a different service
- Booking–capacity divergence — The customer is confirmed without capacity or capacity is consumed without a booking
- Payment–booking divergence — Money moves without a reservation or a booking confirms without required payment
- Stale hold or quote — Expired terms, price, or capacity is committed
- Unauthorized booking — Another account or tenant controls customer, provider, or resource
- False confirmation — The customer receives success while provider or capacity commitment is missing
- Personal-data exposure — Contact, attendee, schedule, payment, or provider data reaches unsafe logs

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition. Also state Required Skills: the specific developer expertise (for example, programming language, framework or library, database technology, authentication/authorization, concurrency, idempotency, transaction management, webhook handling, queue processing, caching, external integration, API design, or infrastructure/deployment concern) needed to understand and fix the risk. Derive Required Skills only from the trigger, behavior, and affected code or workflow already identified for that risk; do not invent technologies or expertise the evidence does not support, and keep the list concise. If no specialised expertise beyond general application development is evident, say so instead of guessing.

