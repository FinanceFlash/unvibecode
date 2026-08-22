---
name: review-scheduled-job-recovery-risk
description: Review customer, financial, security, privacy, compliance, and operational risks in Scheduled Job Execution, Checkpoint, Retry, and Recovery. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Scheduled Job Execution and Recovery Risk

Review schedule, entry, identity, authorization, ownership, windows, state, timing, concurrency, effects, checkpoints, retry, recovery, privacy, and operations. Prioritize:
- Missed execution — Schedule, timezone, misfire, or checkpoint errors leave required work unprocessed
- Duplicate business effects — Concurrent owners, replay, or lost responses charge, notify, mutate, or export twice
- Checkpoint skips work — A cursor advances before required items or effects are durably resolved
- Stale worker commits — An expired owner continues after takeover and overwrites newer results
- False completion — Partial, failed, skipped, or uncertain items are reported as successful
- Retry storm — Unbounded attempts and synchronized backoff overload dependencies and increase cost
- Wrong time window — DST, clock, inclusive-boundary, or late-data mistakes process too much or too little
- Unauthorized execution — A manual trigger, tenant swap, or privileged control runs destructive or costly work
- Unrecoverable poison item — One bad record blocks the schedule forever or is silently discarded
- Sensitive-data exposure — Job inputs, outputs, credentials, or failure payloads reach unsafe logs or operators

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition. Also state Required Skills: the specific developer expertise (for example, programming language, framework or library, database technology, authentication/authorization, concurrency, idempotency, transaction management, webhook handling, queue processing, caching, external integration, API design, or infrastructure/deployment concern) needed to understand and fix the risk. Derive Required Skills only from the trigger, behavior, and affected code or workflow already identified for that risk; do not invent technologies or expertise the evidence does not support, and keep the list concise. If no specialised expertise beyond general application development is evident, say so instead of guessing.

