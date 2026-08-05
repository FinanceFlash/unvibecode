# Testing Guide

Check authoritative records, state transitions, permissions, external effects, recovery, and audit changes—not only HTTP responses or user-interface messages.

## 1. Valid event sends one message

**Given:** An eligible event has one authoritative recipient, verified destination, purpose, and approved template

**When:** Notification delivery starts

**Expect:** One local message and one initial provider attempt are created

**Must not happen:** The event sends to another recipient or creates duplicate messages

**Best test levels:** Integration and end-to-end.

## 2. Correct template and locale render

**Given:** The recipient has a supported locale and complete allowed variables

**When:** Content is rendered

**Expect:** The approved template version produces escaped recipient-scoped content

**Must not happen:** Fallback text, another locale, or another customer's data appears unexpectedly

**Best test levels:** Unit and integration.

## 3. Provider status is recorded

**Given:** The provider accepts the initial attempt and returns a message reference

**When:** The response and later callback are processed

**Expect:** The local message retains one correlated, monotonic status history

**Must not happen:** Accepted is falsely treated as delivered or status moves backward

**Best test levels:** Provider contract and integration.

## 4. Recipient or template data is missing

**Given:** The event lacks an authoritative destination, purpose, template, or required variable

**When:** Eligibility and rendering run

**Expect:** The message is rejected or recorded failed before provider submission

**Must not happen:** Blank or incomplete content is sent

**Best test levels:** Unit and API.

## 5. Payload or destination is malformed

**Given:** The destination, variables, markup, link, header, attachment, or payload size is invalid

**When:** Validation runs

**Expect:** Unsafe input is rejected before provider submission

**Must not happen:** Malformed data reaches the provider, renderer, or logs unsafely

**Best test levels:** Unit, API, and security.

## 6. Channel is suppressed or ineligible

**Given:** The destination is unverified, opted out where applicable, blocked, or unavailable for the purpose

**When:** Channel selection runs

**Expect:** Policy suppresses the message or selects an explicitly permitted channel

**Must not happen:** Purpose or preference rules are silently bypassed

**Best test levels:** Policy integration.

## 7. Recipient resolves outside tenant

**Given:** The event references a valid identity or destination belonging to another account or tenant

**When:** Recipient resolution runs

**Expect:** Ownership and tenant checks deny or correct the send

**Must not happen:** An identifier alone redirects protected content

**Best test levels:** Authorization and security.

## 8. Equivalent destinations or event keys differ

**Given:** Address casing, phone format, provider token format, or deduplication representation varies

**When:** Canonicalization and uniqueness run

**Expect:** One written normalization rule is used consistently

**Must not happen:** Formatting bypasses deduplication or destination policy

**Best test levels:** Unit and integration.

## 9. Duplicate events arrive together

**Given:** Two workers receive the same eligible event and deduplication key concurrently

**When:** Both create and send

**Expect:** Trusted uniqueness produces one recipient-visible message

**Must not happen:** Both workers send before detecting duplication

**Best test levels:** Concurrency integration.

## 10. Send occurs at expiry or quiet-hours boundary

**Given:** The event is evaluated immediately before, at, and after a timing boundary

**When:** The server selects send, defer, suppress, or expire

**Expect:** One explicit trusted-time rule is applied

**Must not happen:** Client clocks or races change eligibility unpredictably

**Best test levels:** Unit with controlled time.

## 11. Notification request response is lost

**Given:** The local message may already exist but the producer received no result

**When:** The producer retries

**Expect:** The existing outcome is returned or one message is created safely

**Must not happen:** Retries multiply messages or provider attempts

**Best test levels:** API and integration.

## 12. Business event is replayed

**Given:** An event key already produced a message

**When:** The event is delivered again

**Expect:** It maps to the existing message or is safely rejected

**Must not happen:** Recipient-visible content and audit effects repeat

**Best test levels:** Integration.

## 13. Notification trigger is flooded

**Given:** One actor or event source generates repeated expensive sends

**When:** Frequency and abuse limits are reached

**Expect:** Provider traffic is bounded while legitimate critical paths remain available

**Must not happen:** Unbounded messages, cost, or harassment occurs

**Best test levels:** Security and load.

## 14. Message commits but provider call fails

**Given:** The send intent is authoritative but no accepted provider attempt exists

**When:** Failure handling runs

**Expect:** A retryable or final failure is recorded without recreating the message

**Must not happen:** The system reports delivery or loses the notification silently

**Best test levels:** Integration.

## 15. Provider times out with uncertain outcome

**Given:** The provider call returns no reliable acceptance or rejection

**When:** Recovery evaluates the attempt

**Expect:** The state remains uncertain and is reconciled or safely handed off

**Must not happen:** Blind retry sends duplicates or uncertainty becomes success

**Best test levels:** Provider contract and integration.

## 16. Provider accepts but response is lost

**Given:** The provider may have accepted the message while the local caller sees failure

**When:** The operation is retried or reconciled

**Expect:** Provider idempotency, lookup, or callback establishes one outcome

**Must not happen:** A second recipient-visible message is sent

**Best test levels:** Integration.

## 17. Template variable contains unauthorized data

**Given:** The event includes a field from another user, tenant, or disallowed business object

**When:** Rendering and policy checks run

**Expect:** The field is excluded or the message is denied

**Must not happen:** Cross-customer or excessive data is delivered

**Best test levels:** Security and integration.

## 18. Delivery failure is logged

**Given:** The path contains destinations, message content, links, tokens, and provider responses

**When:** An error or diagnostic event occurs

**Expect:** Logs remain useful without credentials, reusable links, or unnecessary personal content

**Must not happen:** Secrets or full protected messages are exposed

**Best test levels:** Security and log inspection.

## 19. Late callback follows failure handoff

**Given:** The initial attempt is marked retryable and a delayed accepted or delivered callback arrives

**When:** Status reconciliation runs

**Expect:** Current attempt and retry state converge without duplicate visible delivery

**Must not happen:** A stale callback moves state backward or ignores an already delivered result

**Best test levels:** Integration.

## 20. Provider succeeds but local status fails

**Given:** The provider accepted or delivered while the local status or audit write did not commit

**When:** Reconciliation runs

**Expect:** The provider reference repairs the local outcome without another send

**Must not happen:** The application loses evidence or resends the message

**Best test levels:** Integration and operations.

