# Product and Business Guide

## Boundary
Starts when an initial transactional notification attempt has a recorded retryable or uncertain failure. Ends when the message is delivered once, expires, is suppressed, reaches a bounded final failure, or is escalated for explicit operational handling.

## People and systems
- Intended recipient
- Notification retry scheduler and worker
- Channel-selection and policy service
- Email, SMS, push, or in-app providers
- Preference, consent, identity, and tenant services
- Operations or customer-support responder
- Security, privacy, finance, and audit teams

## Things created or changed
- Original notification and business-event key
- Failed or uncertain delivery attempt
- Failure classification and retry eligibility
- Retry job, attempt number, due time, backoff, and expiry
- Fallback plan, channel, destination, and adapted content
- Provider reference, callback, final outcome, and audit record

## Stages
- Message: initial failure → retry scheduled → retrying → delivered, fallback pending, final failed, suppressed, or expired
- Attempt: due → claimed → submitted → accepted, delivered, failed, or uncertain
- Fallback: unavailable → eligible → scheduled → delivered or failed
- Operational case: absent → created → resolved or closed

## Product decisions
- Which provider errors are retryable, permanent, suppressed, or uncertain
- Maximum attempts, total duration, backoff, jitter, and provider circuit-breaker policy
- Message expiry and whether late delivery still has business value
- Whether an accepted or delivered callback cancels scheduled work
- Fallback channel order and verified-destination requirements
- Consent, preference, purpose, quiet-hours, and content rules per fallback channel
- Whether content must be shortened, redacted, or re-rendered for fallback
- Idempotency key across attempts, providers, and channels
- When to dead-letter, alert, open a support case, or require manual action
- Rate, cost, provider failover, monitoring, and retention limits

## Happy paths
- A transient initial failure succeeds on a bounded retry without duplicate delivery
- The primary channel reaches its allowed limit and one eligible fallback channel delivers
- A permanent or expired failure ends visibly without unsafe retry

## Negative paths
- Failure type, original message, recipient, attempt, or retry metadata is missing or invalid
- A permanent, suppressed, delivered, or expired message is selected for retry
- Fallback destination lacks verification, permission, or allowed content
- A stale job or callback targets a newer message state

## Edge cases
- Two workers claim the same retry together
- Delivery occurs exactly at message expiry or quiet-hours boundary
- A provider callback arrives while a retry or fallback is in flight
- Primary channel delivers after fallback has been scheduled
- Recipient preference, destination, tenant, or account eligibility changes between attempts

## Acceptance criteria
1. Only a current retryable or uncertain failure may create a retry attempt
2. Attempt number, due time, expiry, message, recipient, tenant, and channel must remain bound
3. Maximum attempts, duration, backoff, jitter, rate, and cost limits must be enforced
4. A delivered, suppressed, expired, cancelled, or finally failed message must not retry
5. Fallback must recheck verified destination, purpose, preference, consent, quiet hours, and content policy
6. Concurrent workers and replayed jobs must not cause duplicate recipient-visible delivery
7. Late callbacks must reconcile monotonically and cancel obsolete scheduled work
8. Uncertain provider outcomes must not cause blind resend
9. Final failure must remain visible and trigger explicit operational policy
10. Destinations, message content, tokens, provider responses, and credentials must remain protected

## Business risks
| Risk | Business consequence |
|---|---|
| Duplicate delivery | Concurrent workers, replayed jobs, or uncertain outcomes send the same notice repeatedly |
| Notification spam | Unbounded attempts or fallback channels harass recipients and increase cost |
| Missing critical notice | A retryable failure is lost, expires silently, or is marked final incorrectly |
| Wrong fallback channel | Consent, preference, verification, purpose, or content rules are bypassed |
| Late harmful delivery | An expired password, payment, booking, or security message arrives after it is useful |
| Infinite retry or provider cost | Backoff, attempt, duration, or circuit-breaker controls fail |
| Stale-status conflict | Late callbacks and active retries disagree and move the message backward |
| Secret or personal-data exposure | Fallback adaptation, provider errors, and diagnostics reveal protected content |

