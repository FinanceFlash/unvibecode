# Permission and Abuse Guide

## Permission boundaries
- Every run must bind job and definition version, tenant, trigger, occurrence, input window, and stable run identity
- Only an enabled job or authorized manual actor may create a runnable occurrence
- At most the allowed number of owners may hold effective authority for a run or partition
- Expired or revoked workers must be fenced from committing new checkpoints or effects
- Input-window and checkpoint boundaries must be deterministic and must not silently skip eligible work

## Misuse paths
- Missed execution — Schedule, timezone, misfire, or checkpoint errors leave required work unprocessed
- Duplicate business effects — Concurrent owners, replay, or lost responses charge, notify, mutate, or export twice
- Checkpoint skips work — A cursor advances before required items or effects are durably resolved
- Stale worker commits — An expired owner continues after takeover and overwrites newer results
- False completion — Partial, failed, skipped, or uncertain items are reported as successful
- Retry storm — Unbounded attempts and synchronized backoff overload dependencies and increase cost
- Wrong time window — DST, clock, inclusive-boundary, or late-data mistakes process too much or too little
- Unauthorized execution — A manual trigger, tenant swap, or privileged control runs destructive or costly work
- Unrecoverable poison item — One bad record blocks the schedule forever or is silently discarded
- Sensitive-data exposure — Job inputs, outputs, credentials, or failure payloads reach unsafe logs or operators

Protect scheduler and operator identity, tenant scope, job controls, checkpoints, inputs, outputs, secrets, privileged repair tools, and audit records. Deny uncertain identity, ownership, current authority, or tenant.

