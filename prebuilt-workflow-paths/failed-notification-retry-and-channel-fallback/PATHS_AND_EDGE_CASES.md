# Paths and Edge Cases

## Supported paths
- Same-provider transient retry
- Alternate-provider retry on the same channel
- Fallback from email to SMS, push, or in-app
- Fallback from SMS or push to another eligible channel
- Quiet-hours deferral and expiry
- Permanent failure or suppression without retry
- Dead-letter, operational alert, support case, and manual repair
- Late callback, uncertain outcome, reconciliation, and cancellation of obsolete jobs

## Normal paths
- A transient initial failure succeeds on a bounded retry without duplicate delivery
- The primary channel reaches its allowed limit and one eligible fallback channel delivers
- A permanent or expired failure ends visibly without unsafe retry

## Denied paths
- Failure type, original message, recipient, attempt, or retry metadata is missing or invalid
- A permanent, suppressed, delivered, or expired message is selected for retry
- Fallback destination lacks verification, permission, or allowed content
- A stale job or callback targets a newer message state

## Timing, concurrency, and boundaries
- Two workers claim the same retry together
- Delivery occurs exactly at message expiry or quiet-hours boundary
- A provider callback arrives while a retry or fallback is in flight
- Primary channel delivers after fallback has been scheduled
- Recipient preference, destination, tenant, or account eligibility changes between attempts

Cover valid, invalid, duplicate, expired, stale, replayed, repeated, simultaneous, partially completed, unauthorized, and recovery outcomes.

