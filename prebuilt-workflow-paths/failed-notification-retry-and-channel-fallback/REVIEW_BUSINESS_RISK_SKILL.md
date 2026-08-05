---
name: review-notification-retry-fallback-risk
description: Review customer, business, permission, privacy, and operational risks in Failed Notification Retry and Channel Fallback. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review Notification Retry and Channel Fallback Risk

Review entry, validation, authorization, state, timing, concurrency, external effects, retry, recovery, privacy, and support paths. Prioritize:
- Duplicate delivery — Concurrent workers, replayed jobs, or uncertain outcomes send the same notice repeatedly
- Notification spam — Unbounded attempts or fallback channels harass recipients and increase cost
- Missing critical notice — A retryable failure is lost, expires silently, or is marked final incorrectly
- Wrong fallback channel — Consent, preference, verification, purpose, or content rules are bypassed
- Late harmful delivery — An expired password, payment, booking, or security message arrives after it is useful
- Infinite retry or provider cost — Backoff, attempt, duration, or circuit-breaker controls fail
- Stale-status conflict — Late callbacks and active retries disagree and move the message backward
- Secret or personal-data exposure — Fallback adaptation, provider errors, and diagnostics reveal protected content

For each material risk, explain the trigger, current or expected behavior, business consequence, protection, decision or test, and acceptance condition.

