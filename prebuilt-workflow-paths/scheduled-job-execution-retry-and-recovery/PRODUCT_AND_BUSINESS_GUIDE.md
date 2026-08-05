# Product and Business Guide

## Boundary
Starts when an enabled schedule makes a bounded job run due or an authorized operator requests an equivalent manual run. Ends when one run completes, safely records no work, remains partially failed with repair work, exhausts retries, or is cancelled—with its lease, input window, outputs, checkpoint, alerts, and audit state consistent.

## People and systems
- Scheduler, timer, or orchestration platform
- Job runner, coordinator, lease store, and workers
- Source datastore, checkpoint store, and output destination
- External service or business-effect provider
- Authorized operator, support engineer, and incident responder
- Service owner, security, SRE, and monitoring systems

## Things created or changed
- Job definition, version, enabled state, schedule, timezone, and misfire policy
- Due time, run, run identity, trigger source, input window, and attempt
- Claim, lease, owner, heartbeat, expiry, cancellation, and fencing token
- Checkpoint, cursor, page, batch, item, item outcome, and failure
- Output, business effect, idempotency key, receipt, and acknowledgement
- Retry, backoff, dead-letter item, alert, run summary, metrics, logs, and audit event

## Stages
- Job: enabled or paused; version current or retired
- Run: due → claimable → claimed → running → completed, no work, partial, failed, timed out, cancelled, retrying, or exhausted
- Lease: absent → acquired → renewed → released, expired, or revoked
- Checkpoint: committed → candidate → committed, unchanged, or awaiting reconciliation
- Item: eligible → claimed → applied, skipped, failed, uncertain, or awaiting repair

## Product decisions
- Schedule expression, trusted timezone, daylight-saving overlap or gap behavior, and calendar exclusions
- Misfire grace period, catch-up, backfill, skip, and maximum historical-run policy
- How stable run identity is derived from job, schedule occurrence, tenant, input window, and version
- Whether overlaps are prohibited, queued, merged, or partitioned and how leases are fenced
- Input-window start and end inclusivity, ordering, late-arriving data, pagination, and checkpoint meaning
- Maximum items, pages, runtime, concurrency, resource use, external calls, and business-effect rate
- Per-item and whole-run success, partial completion, skip, poison item, and completion-summary rules
- Timeout, cancellation, heartbeat, retryable errors, maximum attempts, backoff, jitter, and retry budget
- When outputs and checkpoints commit and how lost responses, replays, and manual reruns remain idempotent
- Alerts, escalation, repair, reconciliation, retention, tenant isolation, secret handling, observability, and audit

## Happy paths
- One due schedule occurrence is claimed once, processes its bounded window, commits effects, then advances its checkpoint
- A run with no eligible work records a truthful no-work outcome under the documented checkpoint policy
- A permitted catch-up or manual repair run uses an explicit window and does not duplicate completed effects

## Negative paths
- Job definition, schedule, timezone, run identity, input window, checkpoint, tenant, or required configuration is missing or invalid
- The job is paused, disabled, retired, outside its calendar, or triggered by an unauthorized operator
- A lease cannot be acquired or the run conflicts with the overlap policy
- An input item, provider, output, checkpoint, or completion state is failed or uncertain

## Edge cases
- Daylight-saving time creates a missing or repeated local schedule time
- An item timestamp or cursor lies exactly on the window or page boundary
- Two schedulers claim the same occurrence or a lease expires while the old worker continues
- Outputs commit but the checkpoint or completion response is lost
- Late-arriving input appears behind an already committed checkpoint

## Acceptance criteria
1. Every run must bind job and definition version, tenant, trigger, occurrence, input window, and stable run identity
2. Only an enabled job or authorized manual actor may create a runnable occurrence
3. At most the allowed number of owners may hold effective authority for a run or partition
4. Expired or revoked workers must be fenced from committing new checkpoints or effects
5. Input-window and checkpoint boundaries must be deterministic and must not silently skip eligible work
6. Business effects and item outcomes must be idempotent across retries, replays, overlaps, and manual reruns
7. A checkpoint must not advance beyond unresolved required work unless the documented poison-item policy says how it remains recoverable
8. Completed status must match item results, output acknowledgements, and checkpoint state
9. Retries must be bounded by attempts, time, concurrency, and budget and must not amplify an outage
10. Tenant data, secrets, payloads, outputs, and operational controls must remain isolated and protected

## Business risks
| Risk | Business consequence |
|---|---|
| Missed execution | Schedule, timezone, misfire, or checkpoint errors leave required work unprocessed |
| Duplicate business effects | Concurrent owners, replay, or lost responses charge, notify, mutate, or export twice |
| Checkpoint skips work | A cursor advances before required items or effects are durably resolved |
| Stale worker commits | An expired owner continues after takeover and overwrites newer results |
| False completion | Partial, failed, skipped, or uncertain items are reported as successful |
| Retry storm | Unbounded attempts and synchronized backoff overload dependencies and increase cost |
| Wrong time window | DST, clock, inclusive-boundary, or late-data mistakes process too much or too little |
| Unauthorized execution | A manual trigger, tenant swap, or privileged control runs destructive or costly work |
| Unrecoverable poison item | One bad record blocks the schedule forever or is silently discarded |
| Sensitive-data exposure | Job inputs, outputs, credentials, or failure payloads reach unsafe logs or operators |

