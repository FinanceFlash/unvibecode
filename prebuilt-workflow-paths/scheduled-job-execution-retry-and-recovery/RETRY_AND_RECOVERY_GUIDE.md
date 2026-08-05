# Retry and Recovery Guide

## Partial failures
- Business outputs commit but the checkpoint does not
- The checkpoint commits but the run response or completion event is lost
- A batch contains successful, failed, skipped, and uncertain items
- The lease expires while the original worker is still executing
- An external provider accepts an effect but its acknowledgement is lost
- A late-arriving record falls behind a previously committed window

## Recovery rules
- Use stable job, occurrence, tenant, window, item, effect, and attempt identities consistently.
- Re-read lease authority, checkpoint, item outcomes, output receipts, and run state before retrying.
- Fence stale workers and never assume a timeout means an effect did not happen.
- Keep partial, failed, skipped, poison, and uncertain items visible and repairable.
- Reconcile schedule occurrences, inputs, effects, checkpoints, run summaries, alerts, and audit evidence.

