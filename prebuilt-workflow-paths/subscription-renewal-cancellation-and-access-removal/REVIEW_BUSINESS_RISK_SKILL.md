---
name: review-subscription-renewal-cancellation-risk
description: Review customer, revenue, permission, privacy, and operational risks in Subscription Renewal, Cancellation, and Entitlement Release. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Subscription Renewal and Cancellation Risk

Review entry, amount or access, authorization, state, timing, concurrency, external effects, retry, recovery, privacy, and support paths. Prioritize:
- Duplicate renewal charge — Scheduler replay or concurrency bills one period more than once
- Premature access loss — Cancellation or partial failure removes paid entitlement too early
- Free continued access — Termination fails to release entitlement, seats, keys, or sessions
- Billing–access divergence — Payment, invoice, subscription, and entitlement disagree
- Unauthorized cancellation — Another user or tenant terminates a paid subscription
- Missed renewal — A valid due subscription is skipped or silently stranded
- Hidden or ineffective cancellation — The customer believes renewal stopped but billing continues
- Sensitive-data exposure — Billing, payment, cancellation, or account data reaches unsafe logs

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition. Also state Required Skills: the specific developer expertise (for example, programming language, framework or library, database technology, authentication/authorization, concurrency, idempotency, transaction management, webhook handling, queue processing, caching, external integration, API design, or infrastructure/deployment concern) needed to understand and fix the risk. Derive Required Skills only from the trigger, behavior, and affected code or workflow already identified for that risk; do not invent technologies or expertise the evidence does not support, and keep the list concise. If no specialised expertise beyond general application development is evident, say so instead of guessing.

