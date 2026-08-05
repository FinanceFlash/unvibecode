---
name: implement-scheduled-job-recovery
description: Implement or modify Scheduled Job Execution, Checkpoint, Retry, and Recovery. Use when adding or changing schedule handling, authorization, leases, windows, effects, checkpoints, retries, recovery, security controls, monitoring, or tests.
---

# Implement Scheduled Job Execution and Recovery

Confirm:
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

Follow project conventions and protect:
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

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

