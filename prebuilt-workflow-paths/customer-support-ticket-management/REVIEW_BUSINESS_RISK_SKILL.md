---
name: review-support-ticket-risk
description: Review customer, business, permission, privacy, and operational risks in Customer Support Ticket Lifecycle. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Support Ticket Lifecycle Risk

Review entry, validation, authorization, state, timing, concurrency, external effects, retry, recovery, privacy, and support paths. Prioritize:
- Lost customer issue — A valid request is accepted externally but no actionable ticket exists
- Unauthorized ticket access — Another customer, tenant, or agent sees or changes protected support data
- Internal-note exposure — Private investigation content is sent to the customer
- Incorrect routing or priority — Critical issues wait in the wrong queue or low-risk issues consume emergency capacity
- False resolution — A ticket closes while the customer problem or promised action remains incomplete
- SLA failure — Deadlines pause incorrectly or escalation never occurs
- Duplicate business action — Retries repeat refunds, credits, notifications, or account changes
- Sensitive-data exposure — Messages, attachments, credentials, or personal data reach unsafe logs or recipients

For each material risk, explain the trigger, current or expected behavior, business consequence, protection, decision or test, and acceptance condition. Also state Required Skills: the specific developer expertise (for example, programming language, framework or library, database technology, authentication/authorization, concurrency, idempotency, transaction management, webhook handling, queue processing, caching, external integration, API design, or infrastructure/deployment concern) needed to understand and fix the risk. Derive Required Skills only from the trigger, behavior, and affected code or workflow already identified for that risk; do not invent technologies or expertise the evidence does not support, and keep the list concise. If no specialised expertise beyond general application development is evident, say so instead of guessing.

