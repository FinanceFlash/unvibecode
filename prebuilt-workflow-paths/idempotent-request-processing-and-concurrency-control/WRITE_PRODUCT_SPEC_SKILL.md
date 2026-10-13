---
name: write-idempotent-request-spec
description: Write or review a product specification for Idempotent Request Processing and Concurrency Control. Use when defining key policies, lock strategies, concurrency models, duplicate-detection rules, expiry, replay, recovery, or business risks.
---

# Write an Idempotent Request Processing and Concurrency Control Specification

Use application-native terms. Decide:
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

Write scope, actors, objects, states, paths, duplicate-detection outcomes, concurrency outcomes, permissions, recovery, privacy, misuse, acceptance criteria, and unanswered decisions.
