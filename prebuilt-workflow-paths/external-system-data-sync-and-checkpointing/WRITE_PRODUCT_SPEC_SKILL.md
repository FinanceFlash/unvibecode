---
name: write-external-sync-spec
description: Write or review a product specification for External-system Synchronization and Checkpointing. Use when defining actors, states, proof or synchronization rules, edge cases, acceptance criteria, recovery, privacy, or business risks.
---

# Write a External-system Synchronization and Checkpointing Specification

Use application-native terms. Decide:
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

Write scope, actors, objects, states, paths, business outcomes, permissions, validation, recovery, privacy, misuse, acceptance criteria, and unanswered decisions.

