---
name: review-idempotent-request-risk
description: Review customer, revenue, permission, privacy, and operational risks in Idempotent Request Processing and Concurrency Control. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Idempotent Request Processing and Concurrency Control Risk

Review entry, key validation, duplicate detection, lock acquisition, concurrency resolution, state mutation, response storage, expiry, recovery, privacy, and support paths. Prioritize:
- Duplicate execution — Concurrent requests, retries, or lost responses apply the same effect more than once
- Lost idempotency proof — A key is evicted or expires before the client retries, permitting silent re-execution
- Payload-mismatch bypass — A reused key with changed parameters executes a different operation under the original key
- Cross-tenant key collision — A key from one tenant matches or controls an operation in another tenant
- Deadlock or lock starvation — Competing requests block indefinitely, causing timeouts and customer-visible failures
- Stale-read corruption — An optimistic check reads old state, overwrites a concurrent update, and loses data
- Key-store outage escalation — Idempotency-store unavailability blocks all state-mutating requests instead of degrading gracefully
- Response-replay data leak — A stored response containing sensitive data is returned to a different session or actor

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition.
