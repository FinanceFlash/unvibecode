# Permission and Abuse Guide

## Permission boundaries
- One idempotency key must not produce more than one state-mutating effect
- A duplicate request must return the stored original result without re-execution
- A reused key with a materially different payload must be rejected before any effect
- Every key must bind to exactly one actor, tenant, operation, and request fingerprint
- Concurrent requests targeting the same resource must be serialized or safely resolved
- Lock expiry must not silently discard committed work or permit conflicting writes
- Key expiry or eviction must not silently permit re-execution of a completed operation
- Stored responses, request fingerprints, and key metadata must not leak across actors or tenants

## Misuse paths
- Duplicate execution — Concurrent requests, retries, or lost responses apply the same effect more than once
- Lost idempotency proof — A key is evicted or expires before the client retries, permitting silent re-execution
- Payload-mismatch bypass — A reused key with changed parameters executes a different operation under the original key
- Cross-tenant key collision — A key from one tenant matches or controls an operation in another tenant
- Deadlock or lock starvation — Competing requests block indefinitely, causing timeouts and customer-visible failures
- Stale-read corruption — An optimistic check reads old state, overwrites a concurrent update, and loses data
- Key-store outage escalation — Idempotency-store unavailability blocks all state-mutating requests instead of degrading gracefully
- Response-replay data leak — A stored response containing sensitive data is returned to a different session or actor
- Key-flooding denial of service — An attacker creates millions of keys to exhaust storage or degrade lookup performance
- Lock-acquisition abuse — Repeated lock requests from one source prevent legitimate requests from proceeding

Protect actor identity, tenant scope, key ownership, authoritative business objects, stored responses, lock state, support tools, and audit records. Deny uncertain ownership or permission.
