---
name: understand-external-sync-code
description: Trace and explain External-system Synchronization and Checkpointing across an existing codebase. Use when locating entry points, proof or connection checks, tenant mapping, state, external calls, retries, recovery, monitoring, and tests.
---

# Understand External-system Synchronization and Checkpointing Code

Trace:
1. Scheduled, event-driven, manual, full, incremental, resume, cancel, replay, and support entry points
2. Tenant, operator, provider account, connection, credential, entity, filter, and field-scope checks
3. Run lease, configuration version, starting checkpoint, cursor, watermark, overlap, and pagination logic
4. Source fetch, rate limit, retry-after, timeout, page order, stable identity, and duplicate handling
5. Schema mapping, normalization, null, timezone, precision, version, validation, conflict, and deletion rules
6. Destination create, update, delete, idempotency, transaction, per-record result, and compensation
7. Checkpoint candidate, commit conditions, partial failure, quarantine, reconciliation, and rerun
8. Credential privacy, metrics, alerts, audit, manual repair, support tools, and tests

Explain actors, ownership, versions, states, records, checkpoints or proof, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.

