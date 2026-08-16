---
name: understand-idempotent-request-code
description: Trace and explain Idempotent Request Processing and Concurrency Control across an existing codebase. Use when locating key validation, duplicate detection, lock mechanisms, concurrency controls, response storage, expiry, recovery, monitoring, and tests.
---

# Understand Idempotent Request Processing and Concurrency Control Code

Trace:
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

Explain actors, ownership, key bindings, lock states, concurrency tokens, state transitions, effects, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.
