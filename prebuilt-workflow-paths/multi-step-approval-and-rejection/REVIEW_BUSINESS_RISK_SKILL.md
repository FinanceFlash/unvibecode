---
name: review-multi-step-approval-risk
description: Review customer, business, permission, privacy, and operational risks in Multi-step Approval and Rejection. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Multi-step Approval Risk

Review entry, validation, authorization, state, timing, concurrency, external effects, retry, recovery, privacy, and support paths. Prioritize:
- Unauthorized approval — An ineligible or out-of-scope person commits a business decision
- Conflict or self-approval — Separation-of-duties rules are bypassed
- Skipped approval — A required stage, order, or quorum is ignored
- Stale-version approval — Reviewers approve data that is no longer authoritative
- Conflicting final state — Concurrent approve, reject, withdraw, or expire actions disagree
- Duplicate downstream action — A replayed final decision repeats payment, provisioning, publication, or other work
- SLA or escalation failure — Important requests remain unattended or go to the wrong substitute
- Evidence exposure — Sensitive request data or reviewer comments reach the wrong audience or logs

For each material risk, explain the trigger, current or expected behavior, business consequence, protection, decision or test, and acceptance condition. Also state Required Skills: the specific developer expertise (for example, programming language, framework or library, database technology, authentication/authorization, concurrency, idempotency, transaction management, webhook handling, queue processing, caching, external integration, API design, or infrastructure/deployment concern) needed to understand and fix the risk. Derive Required Skills only from the trigger, behavior, and affected code or workflow already identified for that risk; do not invent technologies or expertise the evidence does not support, and keep the list concise. If no specialised expertise beyond general application development is evident, say so instead of guessing.

