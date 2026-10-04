# Testing Guide

Verify the response, durable inbox, authoritative business state, external effects, retry state, and audit record. A successful HTTP response alone is not proof of correct processing.

## 1. Valid unique delivery is accepted

**Given:** A configured provider sends a correctly signed, current, supported event with a new delivery identity

**When:** The endpoint receives and processes it

**Expect:** One inbox record is stored, the provider receives the documented acknowledgement, and the intended effect completes once

**Must not happen:** The request is acknowledged before durable ownership or processed more than once

**Best test levels:** API and integration.

## 2. Body is malformed or too large

**Given:** The body is invalid JSON, truncated, incorrectly encoded, compressed unexpectedly, or over the configured limit

**When:** Boundary validation runs

**Expect:** The request is rejected with bounded work and no inbox or business effect

**Must not happen:** Parsing or buffering consumes unbounded resources

**Best test levels:** Unit, API, and resilience.

## 3. Required verification headers are missing

**Given:** Signature, timestamp, delivery ID, event type, or provider-account headers required by the contract are absent

**When:** Verification begins

**Expect:** The request is rejected and the missing field is recorded without exposing secrets

**Must not happen:** Defaults turn an unauthenticated request into a trusted event

**Best test levels:** API and security.

## 4. Signature does not match

**Given:** The body or signature was altered, or the request was signed with an unrelated secret

**When:** Constant-time verification runs

**Expect:** The request is rejected before parsing-dependent routing or effects

**Must not happen:** A forged delivery reaches the inbox or business service

**Best test levels:** Unit, API, and security.

## 5. Signature uses the original request body

**Given:** A valid body contains whitespace, Unicode, numeric formatting, or key order that changes when re-serialized

**When:** Signature verification runs

**Expect:** Verification uses the exact received bytes and succeeds only for those bytes

**Must not happen:** Parsed or normalized content replaces the authenticated input

**Best test levels:** Unit and framework integration.

## 6. Timestamp is outside the replay window

**Given:** A correctly signed delivery timestamp is older or farther in the future than policy allows

**When:** Replay validation runs with controlled time

**Expect:** The request is rejected or quarantined according to provider policy

**Must not happen:** A captured request is accepted as a new event

**Best test levels:** Unit and API with a controlled clock.

## 7. Secret rotation overlaps

**Given:** The current and immediately previous secrets are valid during a bounded rotation window

**When:** Deliveries signed with current, previous, unknown, and expired secrets arrive

**Expect:** Only policy-approved secrets verify, and use of the previous secret is observable

**Must not happen:** Rotation causes an outage or leaves an old secret trusted indefinitely

**Best test levels:** Integration and operations.

## 8. Provider, endpoint, or tenant is not authorized

**Given:** A validly signed event names the wrong provider account, environment, endpoint, or tenant

**When:** Scope binding runs

**Expect:** The event is denied before routing or business changes

**Must not happen:** Valid provider proof grants cross-tenant authority

**Best test levels:** Authorization and security.

## 9. Event type or schema version is unsupported

**Given:** An authentic delivery uses an unknown event type, incompatible schema version, or missing required field

**When:** Classification and schema validation run

**Expect:** The event is explicitly ignored, rejected, or quarantined according to policy

**Must not happen:** Unknown data is coerced into a known business command

**Best test levels:** Unit and integration.

## 10. Duplicate deliveries arrive concurrently

**Given:** Two requests with the same provider, tenant, delivery identity, and payload arrive simultaneously

**When:** Both attempt durable acceptance and processing

**Expect:** A storage uniqueness rule creates one inbox record and one effective processor

**Must not happen:** A check-then-insert race creates duplicate effects

**Best test levels:** Concurrency integration.

## 11. A completed delivery is replayed

**Given:** A delivery whose effect and completion state are committed is sent again

**When:** Deduplication runs

**Expect:** The endpoint returns the documented duplicate response and preserves the completed state

**Must not happen:** The completed charge, grant, message, or transition repeats

**Best test levels:** API and worker integration.

## 12. Delivery identity has a different payload

**Given:** An existing provider, tenant, and delivery identity arrives with a different raw-body digest

**When:** The duplicate record is compared

**Expect:** The delivery is treated as a conflict, alerted, and withheld from effects

**Must not happen:** The original evidence is overwritten or the changed payload is processed

**Best test levels:** Integration and security.

## 13. Acknowledgement response is lost after durable acceptance

**Given:** The inbox commit succeeds but the provider never receives the response

**When:** The provider retries the delivery

**Expect:** The retry resolves to the same inbox record and processing result

**Must not happen:** Response loss creates a second durable delivery or effect

**Best test levels:** API integration with injected connection loss.

## 14. Inbox persistence fails before acknowledgement

**Given:** Storage is unavailable or the inbox transaction rolls back

**When:** A valid event arrives

**Expect:** The endpoint returns a retryable failure and no durable ownership is claimed

**Must not happen:** A success response tells the provider to discard unowned work

**Best test levels:** Integration and resilience.

## 15. Worker crashes after claim

**Given:** A worker claims a queued delivery and exits before completion

**When:** Its lease expires and recovery starts

**Expect:** A replacement resumes safely using the same delivery identity and fenced claim

**Must not happen:** The event remains stuck forever or both workers commit effects

**Best test levels:** Worker and concurrency integration.

## 16. Effect commits but completion recording fails

**Given:** A domain write or external effect succeeds but the completion marker is not stored

**When:** Retry or reconciliation runs

**Expect:** Current authoritative state is checked and the effect is not repeated blindly

**Must not happen:** An uncertain effect is duplicated or silently marked complete

**Best test levels:** Integration with failure injection and reconciliation.

## 17. Related events arrive out of order

**Given:** A newer version or terminal event is processed before an older related event

**When:** The older event arrives

**Expect:** Version, sequence, or authoritative-state policy ignores or reconciles it explicitly

**Must not happen:** Arrival order reverses a newer business outcome

**Best test levels:** Integration and property testing.

## 18. Delivery flood exceeds capacity

**Given:** Valid, invalid, or duplicate traffic exceeds normal request or worker capacity

**When:** Rate, queue, and concurrency limits engage

**Expect:** Work remains bounded, tenants are isolated, and retry responses follow provider policy

**Must not happen:** One source exhausts shared workers, storage, memory, or downstream quota

**Best test levels:** Load, abuse, and resilience.

## 19. Sensitive delivery is logged or retained unsafely

**Given:** Headers or payloads contain credentials, personal data, payment data, or regulated fields

**When:** success, failure, debugging, support, retention, and deletion paths run

**Expect:** Logs and metrics are redacted, access is authorized, and stored evidence follows retention policy

**Must not happen:** Sensitive content reaches broad logs, alerts, tickets, or indefinite storage

**Best test levels:** Security, privacy, and operations.

## 20. Poison delivery exhausts retries

**Given:** An authentic delivery fails deterministically through the maximum allowed attempts

**When:** Retry policy is exhausted and an operator reviews it

**Expect:** It moves to an explicit quarantine state and any redrive is authorized, audited, and idempotent

**Must not happen:** The delivery loops forever, disappears, or bypasses current validation during redrive

**Best test levels:** Worker integration and operations.
