# Retry and Recovery Guide

## Failure points

- Request arrives but verification, inbox storage, or acknowledgement fails
- Inbox commits but queue publication or wake-up fails
- Provider receives no response and retries an accepted delivery
- Worker claim, business write, external effect, completion marker, audit, or alert fails
- Delivery is authentic but its schema, order, or downstream dependency prevents safe processing

## Retry classification

| Failure | Default treatment |
|---|---|
| Invalid signature, tenant, event type, or schema | Permanent rejection or quarantine; no automatic retry |
| Body conflict under an existing identity | Quarantine and alert; never overwrite |
| Storage, queue, or downstream unavailability | Bounded retry with backoff and jitter |
| Rate limit | Honor retry guidance and preserve the same delivery identity |
| External timeout with unknown outcome | Reconcile authoritative state before retrying the effect |
| Deterministic business validation failure | Permanent failure or domain-specific review |

## Recovery rules

1. Correlate provider, tenant, delivery identity, payload digest, inbox record, attempt, lease, business command, effect idempotency key, and audit event.
2. Re-read durable inbox and authoritative business state before every retry or redrive.
3. Use the same idempotency identity across provider retries, queue redelivery, worker replacement, and operator redrive.
4. Fence expired workers and reject stale completion writes.
5. Do not infer failure from a timeout when the external effect may have completed.
6. Move exhausted or unsafe work to an explicit quarantine state with reason, owner, and next action.
7. Revalidate current configuration, authorization, schema, retention, and business preconditions before redrive.

## Reconciliation

Compare provider delivery history, local inbox state, queue state, business records, external effect records, completion markers, and audit history. Report missing, duplicate, conflicting, stuck, uncertain, and out-of-order deliveries separately.

## Operator controls

- Preview the target tenant, provider, event, payload digest, previous attempts, expected effect, and current authoritative state.
- Require a reason and least-privilege permission for ignore, repair, mark-complete, retry, or redrive.
- Preserve the original delivery and append operator actions; do not rewrite evidence.
- Make bulk redrive bounded, cancellable, observable, and safe under repeated submission.
