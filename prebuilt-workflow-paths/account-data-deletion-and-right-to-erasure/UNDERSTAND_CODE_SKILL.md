---
name: understand-account-data-erasure-code
description: Trace and explain Right-to-erasure and Account-data Deletion across an existing codebase. Use when locating entry points, authorization, policy, state, external calls, material effects, retries, recovery, monitoring, and tests.
---

# Understand Account-data Erasure Code

Trace:
1. Deletion request, verify, scope, approve, deny, hold, cancel, execute, confirm, appeal, and support entry points
2. Requester, representative, account, tenant, alias, contact, identity-proof, and permission checks
3. Data inventory, ownership, category, purpose, system, processor, dependency, and derived-data mapping
4. Retention, legal hold, tax, fraud, safety, dispute, contract, and shared-record decisions
5. Account restriction, session, credential, entitlement, billing, and communication consequences
6. Deletion, anonymization, database, file, cache, index, analytics, log, backup, and processor tasks
7. Task idempotency, batching, checkpoint, retry, acknowledgement, reappearance prevention, and reconciliation
8. Privacy, encryption, evidence, deadline, metrics, audit, support tools, and tests

Explain actors, ownership, versions, states, evidence or data, effects, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.

