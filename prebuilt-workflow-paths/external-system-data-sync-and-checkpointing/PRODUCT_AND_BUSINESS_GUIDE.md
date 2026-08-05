# Product and Business Guide

## Boundary
Starts when a scheduled job, event, or authorized request begins synchronization for a defined source, destination, tenant, and scope. Ends when eligible changes are applied and the checkpoint advances safely, no changes are confirmed, or partial failure remains explicit and recoverable without silent loss or overwrite.

## People and systems
- Sync scheduler, event, or authorized operator
- Source external system
- Destination local or external system
- Connector, mapping, and transformation service
- Credential and tenant-configuration service
- Queue, checkpoint, and reconciliation services
- Data owner, support, security, and operations teams

## Things created or changed
- Sync definition, tenant, source, destination, entity type, filters, and version
- Credential, connection, scope, and provider account
- Sync run, lease, batch, page, cursor, watermark, checkpoint, and attempt
- Source record, destination record, stable external id, version, timestamp, and hash
- Mapped fields, validation errors, conflicts, deletions, and tombstones
- Applied changes, rejected records, reconciliation exception, metrics, and audit record

## Stages
- Sync run: scheduled → running → completed, partial, failed, cancelled, or paused
- Checkpoint: absent or previous → candidate → committed or retained
- Record: fetched → validated → mapped → created, updated, deleted, skipped, conflicted, quarantined, or failed
- Connection: active → rate limited, unauthorized, expired, unavailable, or disabled

## Product decisions
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

## Happy paths
- An incremental sync applies all eligible changes once and advances the checkpoint
- A no-change run confirms source state without modifying records
- An authorized deletion or tombstone removes or deactivates the intended destination record

## Negative paths
- Sync definition, tenant, connection, entity, cursor, mapping, or credential is missing or invalid
- The source or destination is unauthorized or unavailable
- A record violates schema, ownership, version, or conflict policy
- A stale update or deletion would overwrite newer authoritative state

## Edge cases
- Two sync runs overlap for the same scope
- A change occurs exactly at checkpoint or watermark boundary
- Source pages reorder, repeat, or change during pagination
- Records apply but checkpoint persistence fails
- Credential, schema, mapping, or source version changes mid-run

## Acceptance criteria
1. Every run must bind the intended tenant, source, destination, entity, filters, mapping, and configuration version
2. Only authorized source data and destination fields may be read or changed
3. Stable external identity must prevent duplicate destination records
4. Checkpoint semantics must not skip boundary changes or create uncontrolled repeats
5. A checkpoint must not advance beyond unapplied or unresolved changes outside explicit policy
6. Record ordering, versions, conflicts, and deletions must follow source-of-truth policy
7. Retries, replayed pages, and overlapping runs must remain idempotent
8. Partial failure, quarantine, drift, and reconciliation work must remain visible
9. Credentials, source data, personal data, errors, and provider responses must remain protected
10. Run, batch, record, checkpoint, rate, retry, and repair outcomes must remain auditable

## Business risks
| Risk | Business consequence |
|---|---|
| Missed records | Checkpoint advancement skips unapplied changes |
| Duplicate records or effects | Replayed pages, unstable ids, or concurrent runs apply data repeatedly |
| Destructive overwrite | Stale external data replaces newer authoritative destination state |
| Wrong deletion | Out-of-order tombstones remove current records |
| Cross-tenant synchronization | Connection, filter, id mapping, or cache mixes customer data |
| Partial hidden success | Run reports complete despite failed records or destinations |
| Runaway provider load | Paging, retries, or cursor loops consume quotas and cost |
| Credential or data exposure | Tokens, source records, personal data, or errors reach unsafe logs |

