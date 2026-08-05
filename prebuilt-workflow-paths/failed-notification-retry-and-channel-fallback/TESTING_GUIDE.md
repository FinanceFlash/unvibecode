# Testing Guide

Check authoritative records, state transitions, permissions, external effects, recovery, and audit changes—not only HTTP responses or user-interface messages.

## 1. Transient failure succeeds on retry

**Given:** An initial attempt has a current retryable failure and remains within limits and expiry

**When:** The scheduled retry executes

**Expect:** One later attempt is accepted or delivered and obsolete jobs are cancelled

**Must not happen:** The recipient receives duplicate messages

**Best test levels:** Integration.

## 2. Eligible fallback channel delivers

**Given:** The primary channel exhausted policy and another verified permitted channel exists

**When:** Fallback runs

**Expect:** Adapted content is sent once through the selected fallback

**Must not happen:** Fallback bypasses purpose, preference, consent, or content rules

**Best test levels:** Integration and end-to-end.

## 3. Permanent failure ends visibly

**Given:** The provider reports a permanent address, suppression, or policy failure

**When:** Failure classification runs

**Expect:** No retry is scheduled and the final outcome follows operational policy

**Must not happen:** The system retries forever or hides the missing notice

**Best test levels:** Unit and integration.

## 4. Retry metadata is missing

**Given:** The job lacks message, recipient, tenant, channel, attempt, due time, or expiry binding

**When:** The worker claims it

**Expect:** The job is rejected or quarantined without sending

**Must not happen:** An incomplete job sends to a guessed destination

**Best test levels:** Unit and worker integration.

## 5. Provider error is malformed or unknown

**Given:** The provider returns an unexpected, excessive, or unparsable failure

**When:** Classification runs

**Expect:** The outcome remains safely uncertain or final according to explicit default policy

**Must not happen:** Unknown input becomes an unlimited retry

**Best test levels:** Unit and provider contract.

## 6. Permanent error is selected for retry

**Given:** The message has a non-retryable failure, suppression, cancellation, or final state

**When:** A stale job executes

**Expect:** Current state prevents provider submission

**Must not happen:** A permanent failure consumes more attempts or sends again

**Best test levels:** Worker integration.

## 7. Fallback permission is absent

**Given:** The alternate destination is unverified, opted out where applicable, disallowed for purpose, or unavailable

**When:** Fallback selection runs

**Expect:** The channel is skipped and final or alternate policy applies

**Must not happen:** Protected content is sent through an unauthorized channel

**Best test levels:** Policy and security.

## 8. Equivalent attempt identities differ

**Given:** Formatting or provider mapping produces equivalent message, destination, or attempt keys

**When:** Deduplication runs

**Expect:** Canonical identity prevents an additional visible send

**Must not happen:** A representation change bypasses attempt uniqueness

**Best test levels:** Unit and integration.

## 9. Two workers claim one retry

**Given:** Two workers select the same due attempt concurrently

**When:** Both try to execute

**Expect:** A lease, transaction, or unique claim permits one provider submission

**Must not happen:** Both workers send before updating state

**Best test levels:** Concurrency integration.

## 10. Attempt occurs at expiry boundary

**Given:** A retry is due immediately before, at, and after message expiry

**When:** The worker checks trusted time

**Expect:** One explicit boundary policy sends or expires the message

**Must not happen:** Queue delay or client time extends message life unpredictably

**Best test levels:** Unit with controlled time.

## 11. Retry scheduling response is lost

**Given:** The retry job may already exist but the scheduler sees failure

**When:** Scheduling is repeated

**Expect:** One due attempt exists and current status is returned

**Must not happen:** Duplicate jobs later send duplicate messages

**Best test levels:** Scheduler integration.

## 12. Retry job is replayed

**Given:** An attempt identifier already completed or is in flight

**When:** The same job is delivered again

**Expect:** It no-ops or returns the authoritative result

**Must not happen:** Attempt count and provider sends repeat

**Best test levels:** Worker integration.

## 13. Provider outage triggers many retries

**Given:** Many messages fail together against one provider

**When:** Backoff, jitter, rate, and circuit-breaker policy runs

**Expect:** Load and cost remain bounded and recovery is spread safely

**Must not happen:** A retry storm worsens the outage

**Best test levels:** Load and resilience.

## 14. Failure records but enqueue fails

**Given:** The initial failure is authoritative but no retry job exists

**When:** Repair or reconciliation runs

**Expect:** One eligible job is created or final failure becomes visible

**Must not happen:** The notification remains silently stranded

**Best test levels:** Integration and operations.

## 15. Retry provider times out

**Given:** The provider gives no reliable acceptance or rejection

**When:** The worker handles the outcome

**Expect:** The attempt remains uncertain and reconciliation precedes unsafe resend

**Must not happen:** Timeout is treated as failure and immediately duplicated

**Best test levels:** Provider contract and integration.

## 16. Delivery succeeds but response is lost

**Given:** The provider may have delivered while the worker sees failure

**When:** Callback, lookup, or reconciliation runs

**Expect:** The message reaches delivered once and obsolete work is cancelled

**Must not happen:** Retry or fallback sends another visible message

**Best test levels:** Integration.

## 17. Cross-tenant retry job is altered

**Given:** A job references a valid message but a destination, tenant, or account from elsewhere

**When:** The worker resolves current data

**Expect:** Ownership checks reject the mismatch

**Must not happen:** Job fields redirect a message across tenants

**Best test levels:** Authorization and security.

## 18. Retry error is logged

**Given:** The path contains destinations, content, provider tokens, error bodies, and credentials

**When:** An attempt fails

**Expect:** Diagnostics remain useful without reusable secrets or unnecessary personal data

**Must not happen:** Provider secrets or full protected messages are exposed

**Best test levels:** Security and log inspection.

## 19. Late primary callback follows fallback

**Given:** The primary provider reports delivery after fallback is scheduled or submitted

**When:** Reconciliation processes the callback

**Expect:** Written precedence and current state prevent further obsolete sends

**Must not happen:** Status moves backward or both channels continue blindly

**Best test levels:** Integration.

## 20. Fallback delivers but local status fails

**Given:** The alternate provider delivered while final local update or alert cancellation failed

**When:** Recovery runs

**Expect:** Provider reference repairs final state and cancels remaining jobs

**Must not happen:** Additional channels send or operations report false failure

**Best test levels:** Integration and operations.

