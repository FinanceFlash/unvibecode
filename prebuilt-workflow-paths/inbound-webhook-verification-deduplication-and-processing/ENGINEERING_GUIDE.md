# Engineering Guide

## Trace the implementation

1. Locate public endpoints, provider-specific routes, reverse-proxy rewrites, internal event adapters, and manual replay commands.
2. Identify endpoint, provider account, environment, tenant, event type, schema version, and secret configuration resolution.
3. Follow the raw request bytes from the server boundary through size checks, signature and timestamp verification, replay protection, and parsing.
4. Trace inbox or idempotency writes, uniqueness constraints, payload digests, acknowledgement responses, queue publication, and transaction boundaries.
5. Follow event routing, ordering keys, worker claims, leases, fencing, business commands, external effects, and completion markers.
6. Locate retry classification, backoff, rate limiting, dead-letter or quarantine handling, reconciliation, redrive, and operator permissions.
7. Review payload storage, encryption, log redaction, metrics, alerts, audit, retention, deletion, and access to support tooling.
8. Read tests for valid, forged, duplicate, replayed, concurrent, partial, timeout, out-of-order, and recovery paths.

## Rules the code should protect

- Verify the original body before JSON parsing, normalization, decompression, or business work.
- Bind every delivery to an allowed provider, account, endpoint, environment, tenant, event type, and schema version.
- Use constant-time signature comparison, bounded timestamp windows, and explicit secret-rotation rules.
- Store a durable delivery identity and payload digest before returning an acknowledgement that stops provider retries.
- Make uniqueness and conflict handling a storage-level rule, not only an in-memory check.
- Keep acknowledgement, queue ownership, business effects, completion state, and audit state consistent with documented transaction boundaries.
- Fence expired workers so a replacement cannot be overwritten by a stale worker.
- Make provider retries, lost responses, repeated queue messages, and completed-event replays idempotent.
- Keep ordering and version rules explicit; never let arrival order silently define business truth.
- Bound body size, processing time, queue depth, attempts, concurrency, and downstream request rate.
- Treat payloads, headers, signatures, credentials, and error details as sensitive data.

## Safe implementation sequence

1. Confirm the provider contract, delivery identity, signature bytes, timestamp tolerance, tenant mapping, and acknowledgement meaning.
2. Reuse the application's existing authentication, validation, persistence, queue, transaction, logging, metrics, and authorization patterns.
3. Reject invalid, oversized, stale, unknown, or unauthorized requests before durable business effects.
4. Persist the inbox record with a unique key and payload digest; handle duplicate and changed-payload conflicts explicitly.
5. Publish or claim work only from durable state, with bounded leases and a clear completion transition.
6. Apply effects through existing idempotency or transactional-outbox mechanisms; do not invent a second effect ledger.
7. Classify failures, retry only safe transient cases, and preserve uncertain outcomes for reconciliation.
8. Add tests for all core scenarios and document provider-specific decisions and remaining limits.

## State and evidence to require

For every conclusion, identify the endpoint or event entry point, the provider and tenant binding, the exact verification input, the delivery or idempotency key, the state transition, the effect boundary, the retry decision, and the test or operational evidence. A workflow pack describes controls to verify; it is not evidence that an application implements them.
