# Product and Business Guide

## Boundary

Starts when an inbound HTTP delivery reaches a configured webhook endpoint. Ends when the delivery is rejected before business effects, durably accepted and acknowledged for processing, completed with a truthful result, or isolated for explicit repair. The endpoint's acknowledgement must reflect durable ownership, not merely that a process received bytes.

## People and systems

- Provider, partner, or trusted internal event producer
- Customer, tenant, provider account, and endpoint administrator
- Edge proxy, webhook endpoint, signature verifier, and event router
- Inbox or delivery store, queue, worker, idempotency store, and business service
- Secret or key management, schema registry, rate limiter, observability, and audit services
- Support, security, compliance, and operations teams handling replay or repair

## Things created or changed

- Endpoint, provider account, tenant binding, subscribed event type, secret version, and configuration version
- Raw delivery, headers, provider delivery ID, event ID, event type, schema version, received time, and authenticity decision
- Inbox record, deduplication key, payload digest, acknowledgement state, lease, attempt, and processing state
- Domain commands, records, external effects, outbox messages, retry schedule, quarantine item, and reconciliation result
- Metrics, alerts, audit events, retention status, operator action, and redrive history

## Stages

- Delivery: received → size/content checked → authenticated → authorized → parsed → classified
- Inbox: absent → stored → duplicate or conflict → acknowledged → queued
- Processing: queued → claimed → executing → completed, ignored, retryable failure, or quarantined
- Recovery: retry scheduled → retried → exhausted → repaired, redriven, or permanently rejected

## Product decisions

- Which provider, account, tenant, endpoint, event types, schema versions, and environments are allowed
- Which raw bytes and headers are required for verification and how long they are retained
- Signature algorithm, timestamp tolerance, replay policy, current and previous secret overlap, and rotation procedure
- Whether an acknowledgement means durable inbox storage, queue publication, or completed business processing
- Delivery identity and deduplication scope; behavior when the same identity has a different payload digest
- Unknown event, malformed payload, unsupported version, out-of-order event, and provider retry policy
- Synchronous versus asynchronous effects, ordering key, concurrency limit, lease duration, timeout, and cancellation behavior
- Retryable errors, maximum attempts, backoff and jitter, dead-letter or quarantine ownership, and redrive authorization
- Tenant isolation, payload minimization, encryption, log redaction, audit retention, and deletion obligations

## Happy paths

- A valid unique delivery is verified, stored once, acknowledged, processed, and marked complete.
- A valid duplicate is recognized from durable identity and acknowledged without repeating the effect.
- A valid event whose business action is intentionally ignored is recorded with a truthful no-op result.
- A transient downstream failure is retried within policy and eventually completes or remains repairable.

## Negative paths

- The request is too large, malformed, unsigned, tampered with, stale, or addressed to an unknown endpoint.
- The provider account, tenant, event type, schema version, or secret is not authorized.
- The same delivery identity arrives with a different payload, indicating a provider or routing conflict.
- The inbox, queue, business effect, or completion record cannot be durably written.

## Edge cases

- Current and previous secrets overlap during rotation.
- Provider retries arrive concurrently, after a lost response, or after local completion.
- Related events arrive out of order or with an old schema version.
- A worker loses its lease while a replacement worker starts.
- A business effect succeeds while the response, completion marker, or audit write fails.
- A provider floods the endpoint, sends duplicate IDs across tenants, or includes sensitive fields unexpectedly.

## Acceptance criteria

1. Authenticity is checked against the original request body before parsing or side effects.
2. Endpoint, provider account, tenant, event type, schema, and environment are bound explicitly.
3. A durable uniqueness rule prevents duplicate processing for the documented delivery identity.
4. A changed payload under an existing identity is rejected or quarantined as a conflict.
5. Acknowledgement, queue state, business state, and audit state have documented commit semantics.
6. Retries, lost responses, worker replacement, and out-of-order events remain safe and visible.
7. Rate, size, time, concurrency, retry, retention, and payload exposure limits are bounded.
8. Operators can inspect, reconcile, authorize, and redrive failed deliveries without bypassing tenant or permission checks.

## Business risks

| Risk | Business consequence |
|---|---|
| Forged or tampered delivery | Unauthorized state changes, access grants, refunds, or messages |
| Replay or duplicate processing | Duplicate charge, fulfilment, entitlement, or notification |
| Wrong tenant or provider binding | One customer's event changes another customer's data |
| False acknowledgement | Provider stops retrying while the event was never durably owned |
| Ambiguous timeout | A completed external effect is repeated or incorrectly marked failed |
| Out-of-order event | A stale state transition overwrites a newer business outcome |
| Poison payload or flood | Workers, queues, storage, or provider quotas are exhausted |
| Payload exposure | Secrets, personal data, or regulated content enters logs or long-lived storage |
