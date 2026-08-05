---
name: implement-notification-retry-fallback
description: Implement or modify Failed Notification Retry and Channel Fallback. Use when adding or changing validation, authorization, state transitions, external effects, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement Notification Retry and Channel Fallback

Confirm:
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

Follow project conventions and protect:
- Only current retryable or uncertain failures may be attempted
- Delivered, suppressed, expired, cancelled, or finally failed messages must not retry
- Each attempt must bind one message, recipient, tenant, channel, number, and due time
- Attempts, duration, backoff, jitter, rate, and cost must remain bounded
- Fallback must recheck all destination and content permissions
- Concurrent claims, replays, and callbacks must not duplicate visible delivery
- Status transitions must be monotonic across provider and local state
- Secrets, provider credentials, destinations, and personal content must remain protected

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

