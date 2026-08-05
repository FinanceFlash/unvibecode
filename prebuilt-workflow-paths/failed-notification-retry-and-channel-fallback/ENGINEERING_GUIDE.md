# Engineering Guide

## Trace the implementation
1. Initial-failure handoff and retry eligibility entry points
2. Failure normalization, retryable/permanent/uncertain classification, and provider-specific mapping
3. Retry job, attempt number, due time, backoff, jitter, expiry, uniqueness, and claim locking
4. Current message, recipient, tenant, preference, consent, verification, suppression, and quiet-hours checks
5. Fallback policy, channel ordering, content adaptation, template version, and destination resolution
6. Provider client, idempotency, timeout, reference, callback, and uncertain-outcome reconciliation
7. Final failure, dead-letter, alert, support case, manual replay, and repair tools
8. Rate, cost, privacy, retention, metrics, audit, and tests

## Rules the code should protect
- Only current retryable or uncertain failures may be attempted
- Delivered, suppressed, expired, cancelled, or finally failed messages must not retry
- Each attempt must bind one message, recipient, tenant, channel, number, and due time
- Attempts, duration, backoff, jitter, rate, and cost must remain bounded
- Fallback must recheck all destination and content permissions
- Concurrent claims, replays, and callbacks must not duplicate visible delivery
- Status transitions must be monotonic across provider and local state
- Secrets, provider credentials, destinations, and personal content must remain protected

## Build or change safely
1. Confirm the product decisions before relying on framework or provider defaults.
2. Follow existing authorization, state, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, object, version, state, and scope.
4. Enforce permission, current-state, uniqueness, ordering, and time rules at the write.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep downstream inconsistency visible and repairable.
7. Add the core 20 tests.

