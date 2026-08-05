# Paths and Edge Cases

## Supported paths
- One due schedule occurrence is claimed once, processes its bounded window, commits effects, then advances its checkpoint
- A run with no eligible work records a truthful no-work outcome under the documented checkpoint policy
- A permitted catch-up or manual repair run uses an explicit window and does not duplicate completed effects
- Bounded retry followed by exhausted or manual-repair outcome
- Partial-batch recovery and stale-worker takeover

## Normal paths
- One due schedule occurrence is claimed once, processes its bounded window, commits effects, then advances its checkpoint
- A run with no eligible work records a truthful no-work outcome under the documented checkpoint policy
- A permitted catch-up or manual repair run uses an explicit window and does not duplicate completed effects

## Denied paths
- Job definition, schedule, timezone, run identity, input window, checkpoint, tenant, or required configuration is missing or invalid
- The job is paused, disabled, retired, outside its calendar, or triggered by an unauthorized operator
- A lease cannot be acquired or the run conflicts with the overlap policy
- An input item, provider, output, checkpoint, or completion state is failed or uncertain

## Timing, concurrency, and boundaries
- Daylight-saving time creates a missing or repeated local schedule time
- An item timestamp or cursor lies exactly on the window or page boundary
- Two schedulers claim the same occurrence or a lease expires while the old worker continues
- Outputs commit but the checkpoint or completion response is lost
- Late-arriving input appears behind an already committed checkpoint

Cover valid, invalid, duplicate, stale, replayed, repeated, simultaneous, partially completed, unauthorized, expired-lease, timed-out, cancelled, and recovery outcomes.

