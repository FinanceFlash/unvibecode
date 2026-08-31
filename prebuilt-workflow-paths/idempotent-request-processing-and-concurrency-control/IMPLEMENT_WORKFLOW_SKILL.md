---
name: implement-idempotent-request
description: Implement or modify Idempotent Request Processing and Concurrency Control. Use when adding or changing key validation, duplicate detection, lock mechanisms, concurrency controls, response storage, expiry, recovery, privacy controls, monitoring, or tests.
---

# Implement Idempotent Request Processing and Concurrency Control

Confirm:
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

Follow project conventions and protect:
- One idempotency key must not produce more than one state-mutating effect
- A duplicate request must return the stored original result without re-execution
- A reused key with a materially different payload must be rejected before any effect
- Every key must bind to exactly one actor, tenant, operation, and request fingerprint
- Concurrent requests targeting the same resource must be serialized or safely resolved
- Lock expiry must not silently discard committed work or permit conflicting writes
- Key expiry or eviction must not silently permit re-execution of a completed operation
- Stored responses, request fingerprints, and key metadata must not leak across actors or tenants

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.
