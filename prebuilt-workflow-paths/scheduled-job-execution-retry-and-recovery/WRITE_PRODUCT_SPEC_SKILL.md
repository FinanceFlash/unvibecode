---
name: write-scheduled-job-recovery-spec
description: Write or review a product specification for Scheduled Job Execution, Checkpoint, Retry, and Recovery. Use when defining actors, schedules, states, windows, checkpoints, paths, edge cases, acceptance criteria, recovery, permissions, or business risks.
---

# Write a Scheduled Job Execution and Recovery Specification

Use application-native terms. Decide:
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

Write scope, actors, objects, states, paths, business outcomes, permissions, recovery, privacy, misuse, acceptance criteria, and unanswered decisions.

