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

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition.

