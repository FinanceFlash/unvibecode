---
name: understand-scheduled-job-recovery-code
description: Trace and explain Scheduled Job Execution, Checkpoint, Retry, and Recovery across an existing codebase. Use when locating schedules, entry points, authorization, leases, input windows, effects, checkpoints, retries, recovery, monitoring, and tests.
---

# Understand Scheduled Job Execution and Recovery Code

Trace:
1. Schedule registration, due-run creation, catch-up, backfill, manual run, retry, cancel, pause, resume, and repair entry points
2. Job version, scheduler identity, operator permission, tenant, trigger, occurrence, run key, and input-window checks
3. Claim, lease, lock, heartbeat, expiry, fencing token, takeover, overlap, partition, and concurrency logic
4. Source query, ordering, window boundaries, cursor, checkpoint, pagination, batch size, and late-data handling
5. Worker dispatch, item state, business effect, idempotency key, transaction, output receipt, and acknowledgement
6. Run summary, checkpoint commit, no-work, partial, timeout, cancellation, retry, dead letter, and completion logic
7. Backoff, jitter, retry budget, circuit breaker, manual rerun, reconciliation, alerts, and operational controls
8. Secrets, tenant isolation, retention, metrics, logs, tracing, audit, dashboards, and tests

Explain actors, ownership, versions, states, windows, effects, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.

