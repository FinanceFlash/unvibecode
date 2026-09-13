---
name: review-checkout-payment-risk
description: Review customer, revenue, permission, privacy, and operational risks in Checkout Payment Authorization and Capture. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Checkout Payment Authorization and Capture Risk

Review entry, amount or access, authorization, state, timing, concurrency, external effects, retry, recovery, privacy, and support paths. Prioritize:
- Duplicate charge — Concurrent requests, retries, or lost responses capture payment more than once
- Wrong amount or currency — The provider charge differs from the authoritative checkout
- Payment–order divergence — Money moves but the order, entitlement, fulfilment, or ledger does not
- False success — A decline, timeout, authorization, or pending state is shown as captured
- Unauthorized payment action — Another account or tenant controls the order or capture
- Stale authorization — Expired, voided, cancelled, or previously captured authorization is reused
- Card-testing or cost abuse — Automated attempts create fraud, provider fees, or customer harm
- Secret or personal-data exposure — Payment data, tokens, provider responses, or credentials reach unsafe logs

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition. Also state Required Skills: the specific developer expertise (for example, programming language, framework or library, database technology, authentication/authorization, concurrency, idempotency, transaction management, webhook handling, queue processing, caching, external integration, API design, or infrastructure/deployment concern) needed to understand and fix the risk. Derive Required Skills only from the trigger, behavior, and affected code or workflow already identified for that risk; do not invent technologies or expertise the evidence does not support, and keep the list concise. If no specialised expertise beyond general application development is evident, say so instead of guessing.

