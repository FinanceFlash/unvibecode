---
name: review-transactional-notification-delivery-risk
description: Review customer, business, permission, privacy, and operational risks in Transactional Email, SMS, Push, or In-app Delivery. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Transactional Notification Delivery Risk

Review entry, validation, authorization, state, timing, concurrency, external effects, retry, recovery, privacy, and support paths. Prioritize:
- Wrong recipient — Account, tenant, destination, or identity resolution sends protected information elsewhere
- Ineligible channel — Preference, consent, verification, suppression, or purpose rules are bypassed
- Duplicate notification — Replayed events or lost responses send the same business message repeatedly
- Missing critical notice — The application records success although no provider attempt or recoverable handoff exists
- Unsafe rendering — Template variables, markup, links, or attachments expose data or enable injection
- False delivery state — Provider acceptance is recorded as final delivery or callbacks move status backward
- Message amplification — One event or attacker triggers unbounded provider traffic and cost
- Secret or personal-data exposure — Destinations, content, tokens, provider responses, or credentials reach unsafe logs

For each material risk, explain the trigger, current or expected behavior, business consequence, protection, decision or test, and acceptance condition. Also state Required Skills: the specific developer expertise (for example, programming language, framework or library, database technology, authentication/authorization, concurrency, idempotency, transaction management, webhook handling, queue processing, caching, external integration, API design, or infrastructure/deployment concern) needed to understand and fix the risk. Derive Required Skills only from the trigger, behavior, and affected code or workflow already identified for that risk; do not invent technologies or expertise the evidence does not support, and keep the list concise. If no specialised expertise beyond general application development is evident, say so instead of guessing.

