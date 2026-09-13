---
name: review-booking-cancellation-risk
description: Review customer, revenue, permission, privacy, and operational risks in Booking Cancellation, Capacity Release, and Refund Request. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Booking Cancellation and Capacity Release Risk

Review entry, quantity or money, authorization, state, timing, concurrency, external effects, retry, recovery, privacy, and support paths. Prioritize:
- Unauthorized cancellation — Another account or tenant destroys a valid booking
- Capacity not released — Cancelled inventory remains unavailable and revenue is lost
- Excess capacity release — Duplicate cancellation or stale jobs oversell the slot
- Duplicate or wrong refund — Repeated handoff or wrong policy creates financial loss
- Incorrect penalty — Timezone or cut-off errors charge or deny the customer unfairly
- Booking–provider divergence — Local cancellation and external reservation disagree
- Cancellation after service — Stale action reverses a completed or checked-in booking
- Personal-data exposure — Schedule, customer, reason, payment, or provider data reaches unsafe logs

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition. Also state Required Skills: the specific developer expertise (for example, programming language, framework or library, database technology, authentication/authorization, concurrency, idempotency, transaction management, webhook handling, queue processing, caching, external integration, API design, or infrastructure/deployment concern) needed to understand and fix the risk. Derive Required Skills only from the trigger, behavior, and affected code or workflow already identified for that risk; do not invent technologies or expertise the evidence does not support, and keep the list concise. If no specialised expertise beyond general application development is evident, say so instead of guessing.

