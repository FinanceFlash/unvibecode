---
name: understand-notification-retry-fallback-code
description: Trace and explain Failed Notification Retry and Channel Fallback across an existing codebase. Use when locating entry points, authorization, state, storage, external effects, retries, recovery, monitoring, and tests.
---

# Understand Notification Retry and Channel Fallback Code

Trace:
1. Initial-failure handoff and retry eligibility entry points
2. Failure normalization, retryable/permanent/uncertain classification, and provider-specific mapping
3. Retry job, attempt number, due time, backoff, jitter, expiry, uniqueness, and claim locking
4. Current message, recipient, tenant, preference, consent, verification, suppression, and quiet-hours checks
5. Fallback policy, channel ordering, content adaptation, template version, and destination resolution
6. Provider client, idempotency, timeout, reference, callback, and uncertain-outcome reconciliation
7. Final failure, dead-letter, alert, support case, manual replay, and repair tools
8. Rate, cost, privacy, retention, metrics, audit, and tests

Explain actors, ownership, states, transitions, effects, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.

