# Engineering Guide

## Trace the implementation
1. API entry points that accept, require, or generate idempotency keys
2. Key validation, format enforcement, length limits, and character-set checks
3. Key-store lookup, insertion, binding, and duplicate-detection logic
4. Request fingerprint computation (actor, operation, material parameters)
5. Payload-mismatch detection and rejection path
6. Lock acquisition, lease creation, timeout, renewal, and release mechanisms
7. Optimistic concurrency version reads, conditional writes, and conflict handling
8. Original-response storage, retrieval, and replay on duplicate detection
9. Downstream effect execution within the idempotent boundary
10. Key expiry, eviction, garbage collection, and storage-pressure management
11. Audit logging, observability, privacy controls, and error handling

## Rules the code should protect
- One idempotency key must not produce more than one state-mutating effect
- A duplicate request must return the stored original result without re-execution
- A reused key with a materially different payload must be rejected before any effect
- Every key must bind to exactly one actor, tenant, operation, and request fingerprint
- Concurrent requests targeting the same resource must be serialized or safely resolved
- Lock expiry must not silently discard committed work or permit conflicting writes
- Key expiry or eviction must not silently permit re-execution of a completed operation
- Stored responses, request fingerprints, and key metadata must not leak across actors or tenants

## Build or change safely
1. Confirm product decisions before relying on framework or provider defaults for idempotency.
2. Follow existing key-storage, locking, versioning, logging, monitoring, and test conventions.
3. Bind every key to the authoritative actor, tenant, operation, version, and request fingerprint at creation.
4. Enforce duplicate detection, payload-mismatch rejection, and lock acquisition at the write boundary.
5. Make retries and replays safe by returning stored results without re-executing effects.
6. Keep key-store, lock-state, operation-result, and audit-record inconsistency visible and repairable.
7. Add the core 20 tests.
