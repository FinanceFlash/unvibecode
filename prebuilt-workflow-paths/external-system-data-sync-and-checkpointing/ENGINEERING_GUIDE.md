# Engineering Guide

## Trace the implementation
1. Scheduled, event-driven, manual, full, incremental, resume, cancel, replay, and support entry points
2. Tenant, operator, provider account, connection, credential, entity, filter, and field-scope checks
3. Run lease, configuration version, starting checkpoint, cursor, watermark, overlap, and pagination logic
4. Source fetch, rate limit, retry-after, timeout, page order, stable identity, and duplicate handling
5. Schema mapping, normalization, null, timezone, precision, version, validation, conflict, and deletion rules
6. Destination create, update, delete, idempotency, transaction, per-record result, and compensation
7. Checkpoint candidate, commit conditions, partial failure, quarantine, reconciliation, and rerun
8. Credential privacy, metrics, alerts, audit, manual repair, support tools, and tests

## Rules the code should protect
- Every sync operation must remain within its tenant, connection, entity, and field scope
- Stable source identity must map to one intended destination identity
- Checkpoint advancement must not skip unapplied required changes
- Replayed pages, records, and runs must be idempotent
- Version, conflict, source-of-truth, and deletion policy must protect newer state
- Partial failure and quarantined records must remain visible
- Rate limits, retries, pagination, and concurrent runs must remain bounded
- Credentials, source data, personal data, and provider responses must remain protected

## Build or change safely
1. Confirm product decisions before relying on framework or provider defaults.
2. Follow existing authorization, validation, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, tenant, provider or connection, identity, version, state, and scope.
4. Enforce proof, permission, current-state, schema, uniqueness, ordering, and checkpoint rules before material use.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep missing events, partial records, and state divergence visible and repairable.
7. Add the core 20 tests.

