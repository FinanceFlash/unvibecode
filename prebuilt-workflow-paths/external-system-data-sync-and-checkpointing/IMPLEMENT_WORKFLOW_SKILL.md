---
name: implement-external-sync
description: Implement or modify External-system Synchronization and Checkpointing. Use when adding or changing verification or synchronization logic, authorization, state transitions, external calls, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement External-system Synchronization and Checkpointing

Confirm:
- Source of truth and allowed sync direction for each field and entity
- Tenant, provider account, entity, date, status, and field scope
- Full snapshot versus incremental cursor, timestamp, change token, or event sequence
- Checkpoint inclusive or exclusive semantics and overlap window
- Page and batch size, ordering, stable ids, deduplication, and idempotency
- Schema mapping, null, default, enumeration, timezone, precision, and version policy
- Conflict resolution, optimistic version, local edits, and deletion or tombstone policy
- Whether partial batch success may advance any checkpoint
- Rate-limit, retry, backoff, circuit-breaker, scheduling, and concurrent-run policy
- Credential rotation, privacy, audit, metrics, alert, reconciliation, and manual repair policy

Follow project conventions and protect:
- Every sync operation must remain within its tenant, connection, entity, and field scope
- Stable source identity must map to one intended destination identity
- Checkpoint advancement must not skip unapplied required changes
- Replayed pages, records, and runs must be idempotent
- Version, conflict, source-of-truth, and deletion policy must protect newer state
- Partial failure and quarantined records must remain visible
- Rate limits, retries, pagination, and concurrent runs must remain bounded
- Credentials, source data, personal data, and provider responses must remain protected

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

