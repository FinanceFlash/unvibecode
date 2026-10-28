---
name: review-provider-onboarding-risk
description: Review customer, revenue, permission, privacy, and operational risks in Seller or Service-provider Onboarding and Eligibility. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Seller or Service-provider Onboarding Risk

Review entry, evidence or money, authorization, state, timing, concurrency, external effects, retry, recovery, privacy, and support paths. Prioritize:
- Fake or ineligible provider — Fraudulent supply reaches customers and damages trust or safety
- Premature activation — Listing or order access is granted before required checks complete
- Duplicate seller identity — One provider evades history, limits, suspension, or fee obligations
- Reviewer or exception bypass — Unauthorized approval defeats marketplace policy
- Incorrect scope — Provider receives the wrong category, territory, role, or listing entitlement
- Expired evidence — Licences, insurance, tax, or identity proof remains trusted after validity ends
- Payout or account mismatch — Revenue routes to an account not bound to the approved provider
- Sensitive-data exposure — Identity, ownership, bank, tax, or review evidence reaches unsafe audiences or logs

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition. Also state Required Skills: the specific developer expertise (for example, programming language, framework or library, database technology, authentication/authorization, concurrency, idempotency, transaction management, webhook handling, queue processing, caching, external integration, API design, or infrastructure/deployment concern) needed to understand and fix the risk. Derive Required Skills only from the trigger, behavior, and affected code or workflow already identified for that risk; do not invent technologies or expertise the evidence does not support, and keep the list concise. If no specialised expertise beyond general application development is evident, say so instead of guessing.

