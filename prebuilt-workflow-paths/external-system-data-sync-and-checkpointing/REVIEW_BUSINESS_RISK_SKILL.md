---
name: review-external-sync-risk
description: Review customer, data, security, privacy, and operational risks in External-system Synchronization and Checkpointing. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review External-system Synchronization and Checkpointing Risk

Review entry, authentication or connection, tenant mapping, state, ordering, provider behavior, retry, recovery, privacy, load, and downstream paths. Prioritize:
- Missed records — Checkpoint advancement skips unapplied changes
- Duplicate records or effects — Replayed pages, unstable ids, or concurrent runs apply data repeatedly
- Destructive overwrite — Stale external data replaces newer authoritative destination state
- Wrong deletion — Out-of-order tombstones remove current records
- Cross-tenant synchronization — Connection, filter, id mapping, or cache mixes customer data
- Partial hidden success — Run reports complete despite failed records or destinations
- Runaway provider load — Paging, retries, or cursor loops consume quotas and cost
- Credential or data exposure — Tokens, source records, personal data, or errors reach unsafe logs

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition. Also state Required Skills: the specific developer expertise (for example, programming language, framework or library, database technology, authentication/authorization, concurrency, idempotency, transaction management, webhook handling, queue processing, caching, external integration, API design, or infrastructure/deployment concern) needed to understand and fix the risk. Derive Required Skills only from the trigger, behavior, and affected code or workflow already identified for that risk; do not invent technologies or expertise the evidence does not support, and keep the list concise. If no specialised expertise beyond general application development is evident, say so instead of guessing.

