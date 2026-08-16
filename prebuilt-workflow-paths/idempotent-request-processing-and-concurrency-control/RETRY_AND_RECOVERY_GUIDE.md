# Retry and Recovery Guide

## Partial failures
- Key is bound but the downstream effect fails before committing
- Effect commits but the response-storage write fails
- Lock is acquired but the holder crashes before releasing
- Key-store write succeeds but the downstream database transaction rolls back
- Response is stored but a secondary effect (notification, audit, replication) fails
- Garbage collection deletes a key whose stored response was still needed for replay
- Optimistic version write fails but the caller has already prepared dependent state

## Recovery rules
- Use the idempotency key and request fingerprint as the stable identity for recovery.
- Re-read authoritative key state, lock state, and downstream effect status before retrying.
- Never re-execute a completed effect solely because the stored response was lost or evicted.
- Distinguish between incomplete (retriable), completed (replay only), failed (compensate), and expired (require new key) states.
- Reconstruct stored responses from authoritative downstream state when cache or response storage is lost.
- Release or expire locks held by crashed or partitioned processes using lease-based expiry and fencing tokens.
- Reconcile key-store state, downstream-effect state, and audit records after partial failures.
- Log every recovery action with the original key, actor, operation, failure reason, and resolution outcome.
