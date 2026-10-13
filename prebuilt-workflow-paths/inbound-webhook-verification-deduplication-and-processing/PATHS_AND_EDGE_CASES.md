# Paths and Edge Cases

## Supported paths

- Valid unique delivery accepted synchronously into a durable inbox
- Valid delivery acknowledged after safe queue publication
- Duplicate delivery acknowledged without repeated work
- Known no-op event recorded truthfully
- Transient processing failure retried with backoff
- Poison delivery quarantined, reconciled, repaired, and redriven by an authorized operator

## Denied paths

- Oversized, malformed, unsigned, tampered, stale, or future-dated requests
- Unknown endpoint, provider account, environment, tenant, event type, or schema version
- Valid signature with insufficient event or tenant authority
- Existing delivery identity with a different payload digest
- Manual replay without current authorization, validation, reason, and audit

## Timing and boundary paths

- Timestamp exactly inside, on, and outside the replay tolerance
- Delivery signed during current/previous-secret rotation overlap
- Acknowledgement lost before or after the inbox transaction commits
- Provider retry arrives before the original request returns
- Lease expires while the first worker is still running
- Retention or deletion deadline occurs while a delivery is quarantined

## Ordering and concurrency paths

- Two identical requests race to create the inbox record
- The queue redelivers while the first worker owns a lease
- An older state event follows a newer version or terminal event
- Two unrelated events for the same aggregate may execute concurrently
- Provider and local sequence numbers disagree or have gaps

## Partial-failure paths

- Inbox commits but queue publication fails
- Queue publication succeeds but the response is lost
- Domain write commits but completion or audit recording fails
- External side effect times out with an unknown outcome
- Quarantine succeeds but alerting fails

Cover valid, invalid, duplicate, conflicting, stale, concurrent, replayed, out-of-order, partially completed, unauthorized, overloaded, and recovered outcomes.
