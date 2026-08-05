# Engineering Guide

## Trace the implementation
1. Schedule registration, due-run creation, catch-up, backfill, manual run, retry, cancel, pause, resume, and repair entry points
2. Job version, scheduler identity, operator permission, tenant, trigger, occurrence, run key, and input-window checks
3. Claim, lease, lock, heartbeat, expiry, fencing token, takeover, overlap, partition, and concurrency logic
4. Source query, ordering, window boundaries, cursor, checkpoint, pagination, batch size, and late-data handling
5. Worker dispatch, item state, business effect, idempotency key, transaction, output receipt, and acknowledgement
6. Run summary, checkpoint commit, no-work, partial, timeout, cancellation, retry, dead letter, and completion logic
7. Backoff, jitter, retry budget, circuit breaker, manual rerun, reconciliation, alerts, and operational controls
8. Secrets, tenant isolation, retention, metrics, logs, tracing, audit, dashboards, and tests

## Rules the code should protect
- Every run must bind job and definition version, tenant, trigger, occurrence, input window, and stable run identity
- Only an enabled job or authorized manual actor may create a runnable occurrence
- At most the allowed number of owners may hold effective authority for a run or partition
- Expired or revoked workers must be fenced from committing new checkpoints or effects
- Input-window and checkpoint boundaries must be deterministic and must not silently skip eligible work
- Business effects and item outcomes must be idempotent across retries, replays, overlaps, and manual reruns
- A checkpoint must not advance beyond unresolved required work unless the documented poison-item policy says how it remains recoverable
- Completed status must match item results, output acknowledgements, and checkpoint state
- Retries must be bounded by attempts, time, concurrency, and budget and must not amplify an outage
- Tenant data, secrets, payloads, outputs, and operational controls must remain isolated and protected

## Build or change safely
1. Confirm product and operational decisions before relying on scheduler, queue, database, runtime, or provider defaults.
2. Follow existing authorization, state, transaction, privacy, logging, monitoring, and test conventions.
3. Bind every action to authoritative job, definition version, tenant, occurrence, window, lease, item, and effect identities.
4. Enforce permission, ownership, fencing, boundary, uniqueness, and time rules at business effects and checkpoint writes.
5. Make duplicate, concurrent, partial, timed-out, cancelled, and lost-response execution safe.
6. Keep run, item, effect, checkpoint, retry, and alert disagreement visible and repairable.
7. Add the core 20 tests.

