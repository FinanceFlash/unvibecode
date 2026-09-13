---
name: review-account-data-erasure-risk
description: Review customer, security, privacy, compliance, and operational risks in Right-to-erasure and Account-data Deletion. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Account-data Erasure Risk

Review entry, identity, authorization, policy, state, timing, concurrency, external effects, retry, recovery, privacy, and support paths. Prioritize:
- Wrong-person deletion — Weak identity or account resolution destroys another customer's data
- Incomplete erasure — Hidden stores, processors, indexes, backups, or derived data retain personal information
- Unlawful deletion — Required tax, fraud, dispute, safety, or legal-hold evidence is removed
- Excess retention — Exceptions preserve more data or purpose than permitted
- Data reappearance — Late events, restores, caches, or resynchronization recreate deleted records
- Account inconsistency — Credentials, sessions, billing, entitlement, and profile state disagree
- Cross-tenant deletion — Shared identifiers or jobs remove another customer's records
- Sensitive-data exposure — Identity proof, inventory, retained data, or deletion evidence reaches unsafe logs

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition. Also state Required Skills: the specific developer expertise (for example, programming language, framework or library, database technology, authentication/authorization, concurrency, idempotency, transaction management, webhook handling, queue processing, caching, external integration, API design, or infrastructure/deployment concern) needed to understand and fix the risk. Derive Required Skills only from the trigger, behavior, and affected code or workflow already identified for that risk; do not invent technologies or expertise the evidence does not support, and keep the list concise. If no specialised expertise beyond general application development is evident, say so instead of guessing.

