---
name: implement-inbound-webhook
description: Implement or modify Inbound Webhook Verification, Deduplication, and Processing. Use when changing endpoint verification, durable acceptance, idempotency, event processing, retries, recovery, privacy, observability, or tests.
---

# Implement Inbound Webhook Processing

Before editing, confirm the provider contract for exact signature bytes, headers, timestamp tolerance, delivery identity, retry behavior, acknowledgement deadline, event ordering, and schema versions. Then:

1. Reuse existing route, configuration, secret management, storage, queue, transaction, authorization, logging, metrics, and test patterns.
2. Enforce request limits and verify the original body before parsing or side effects.
3. Bind the authenticated delivery to the intended provider account, environment, endpoint, tenant, event type, and schema.
4. Persist one immutable inbox record using a storage uniqueness rule and payload digest conflict check before acknowledging durable ownership.
5. Process through existing idempotency and transaction or outbox mechanisms; fence worker leases and preserve ordering policy.
6. Classify failures, bound retries, reconcile uncertain effects, quarantine exhausted work, and authorize redrive.
7. Redact sensitive data, limit retention and access, emit useful metrics and audit, and add the core 20 tests.

Summarize decisions, changed files, state transitions, transaction and effect boundaries, verification performed, remaining provider-specific limits, and any assumptions needing product approval.
