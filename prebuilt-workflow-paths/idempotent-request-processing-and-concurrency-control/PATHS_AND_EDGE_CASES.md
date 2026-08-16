# Paths and Edge Cases

## Supported paths
- New request with valid key processed and result stored
- Duplicate request detected and original result replayed
- Retry after transient failure with safe replay or completion
- Lock acquisition, hold, release, and timeout
- Optimistic concurrency check with version acceptance or conflict
- Key expiry, eviction, and garbage collection
- Payload-mismatch detection and rejection
- Key-store degradation with documented fallback policy

## Normal paths
- A new request with a valid idempotency key is processed once and the result is stored
- A retried request with an existing key returns the original stored result without re-execution
- A concurrent request on the same resource acquires a lock, completes, and releases it
- An optimistic concurrency check succeeds because no conflicting write occurred

## Denied paths
- The idempotency key is missing, empty, malformed, or exceeds length limits
- A key is reused with a different payload, actor, or operation
- The same key is submitted by a different actor or tenant
- A lock cannot be acquired because another request holds it
- An optimistic concurrency check fails because the resource was modified
- Key-store is unavailable and the degradation policy rejects the request

## Timing, concurrency, and boundaries
- Two requests with the same key arrive before either completes processing
- A lock holder crashes or network-partitions before releasing
- Key expiry races with a legitimate late retry
- A completed request's stored response is evicted before the client retries
- Response storage succeeds but the downstream effect partially fails
- Lock lease renewal is attempted after the lease has already expired
- Garbage collection overlaps with active key creation on the same partition
- An optimistic version read and conditional write span a clock-skew boundary

Cover valid, invalid, duplicate, expired, evicted, replayed, stale, repeated, simultaneous, partially completed, unauthorized, and recovery outcomes.
