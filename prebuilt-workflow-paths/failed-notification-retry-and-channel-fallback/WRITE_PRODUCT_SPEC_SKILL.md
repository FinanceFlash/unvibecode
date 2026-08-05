---
name: write-notification-retry-fallback-spec
description: Write or review a product specification for Failed Notification Retry and Channel Fallback. Use when defining actors, states, permissions, policy decisions, normal paths, edge cases, acceptance criteria, recovery, or business risks.
---

# Write a Notification Retry and Channel Fallback Specification

Use application-native terms. Decide:
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

Write scope, actors, objects, states, paths, customer outcomes, permissions, recovery, privacy, misuse, acceptance criteria, and unanswered decisions.

