# Product and Business Guide

## Boundary
Starts when a client submits a state-mutating request that carries an idempotency key or requires exactly-once execution semantics. Ends when the request is accepted and its effect applied exactly once, rejected as a validated duplicate returning the original result, or denied because the key, lock, or concurrency constraint cannot be satisfied, with the outcome, key state, and audit record stored consistently.

## People and systems
- Client application, mobile app, browser, or upstream service
- API gateway, load balancer, or reverse proxy
- Idempotency-key store (database, cache, or distributed key-value store)
- Distributed lock manager or coordination service
- Application service processing the state-mutating operation
- Downstream services, databases, message brokers, and external providers
- Operations, support, and security teams

## Things created or changed
- Idempotency key record and its binding to request fingerprint
- Lock or lease record with owner, scope, and expiry
- Request fingerprint (hash of actor, operation, and material parameters)
- Original response stored for replay on duplicate detection
- State-mutating effect (database write, external call, message publish)
- Concurrency-control version, row version, or optimistic lock token
- Audit log entry linking key, actor, operation, outcome, and timing

## Stages
- Idempotency key: absent → received → validated → bound → completed → expired or evicted
- Lock: uncontested → acquired → held → released, expired, or stolen
- Request: received → deduplicated or accepted → processing → committed or failed
- Concurrency token: issued → checked at write → accepted or rejected

## Product decisions
- Whether idempotency keys are client-generated, server-generated, or derived from request content
- Key format, length, character-set, and uniqueness requirements
- Key lifetime, expiry policy, and maximum storage duration
- Which operations require idempotency keys and which are naturally idempotent
- Payload-mismatch policy: reject, warn, or ignore when a key is reused with different parameters
- Lock scope: per-resource, per-actor, per-operation, or per-actor-resource combination
- Lock timeout, lease duration, and renewal policy
- Optimistic versus pessimistic concurrency strategy per operation
- Whether the original response is replayed verbatim or reconstructed from current state
- Key-storage technology, partitioning, replication, and consistency requirements
- Rate limits, quota, and abuse controls for key creation
- Privacy and retention policy for stored request fingerprints and response bodies

## Happy paths
- A new request with a valid idempotency key is processed once and the result is stored
- A retried request with an existing key returns the original stored result without re-execution
- A concurrent request on the same resource acquires a lock, completes, and releases it
- An optimistic concurrency check succeeds because no conflicting write occurred

## Negative paths
- The idempotency key is missing, empty, malformed, or exceeds length limits
- A key is reused with a different payload, actor, or operation
- The same key is submitted by a different actor or tenant
- A lock cannot be acquired because another request holds it
- An optimistic concurrency check fails because the resource was modified

## Edge cases
- Two requests with the same key arrive simultaneously before either completes
- A lock holder crashes or becomes unreachable before releasing the lock
- The idempotency-key store becomes unavailable during request processing
- Key expiry races with a legitimate late retry
- A completed request's stored response is evicted before the client retries
- Response storage succeeds but the downstream effect partially fails

## Acceptance criteria
1. A state-mutating operation with a valid idempotency key must produce its effect exactly once
2. A duplicate request must return the original result without re-executing the operation
3. A key reused with a materially different payload must be rejected before execution
4. A key must bind to exactly one actor, tenant, and operation
5. Concurrent requests on the same resource must not corrupt state or produce duplicate effects
6. Lock expiry must release resources without losing committed work
7. Key storage, lock state, operation result, and audit record must remain consistent
8. Expired, evicted, or garbage-collected keys must not silently permit re-execution
9. Request fingerprints, stored responses, and key metadata must respect privacy and retention policy
10. Every idempotency decision and concurrency outcome must be auditable

## Business risks
| Risk | Business consequence |
|---|---|
| Duplicate execution | The same payment, order, message, or state change is applied more than once |
| Lost idempotency proof | A key is evicted or expires before the client retries, permitting silent re-execution |
| Payload-mismatch bypass | A reused key with changed parameters executes a different operation under the original key |
| Cross-tenant key collision | A key from one tenant matches or controls an operation in another tenant |
| Deadlock or lock starvation | Competing requests block indefinitely, causing timeouts and customer-visible failures |
| Stale-read corruption | An optimistic check reads old state, overwrites a concurrent update, and loses data |
| Key-store outage escalation | Idempotency-store unavailability blocks all state-mutating requests instead of degrading gracefully |
| Response-replay data leak | A stored response containing sensitive data is returned to a different session or actor |
