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

For each material risk, explain the trigger, current or expected behavior, business consequence, protection, decision or test, and acceptance condition.

