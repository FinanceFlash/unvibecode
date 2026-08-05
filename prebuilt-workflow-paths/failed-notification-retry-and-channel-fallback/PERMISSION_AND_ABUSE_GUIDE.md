# Permission and Abuse Guide

## Permission boundaries
- Only current retryable or uncertain failures may be attempted
- Delivered, suppressed, expired, cancelled, or finally failed messages must not retry
- Each attempt must bind one message, recipient, tenant, channel, number, and due time
- Attempts, duration, backoff, jitter, rate, and cost must remain bounded
- Fallback must recheck all destination and content permissions

## Misuse paths
- Duplicate delivery — Concurrent workers, replayed jobs, or uncertain outcomes send the same notice repeatedly
- Notification spam — Unbounded attempts or fallback channels harass recipients and increase cost
- Missing critical notice — A retryable failure is lost, expires silently, or is marked final incorrectly
- Wrong fallback channel — Consent, preference, verification, purpose, or content rules are bypassed
- Late harmful delivery — An expired password, payment, booking, or security message arrives after it is useful
- Infinite retry or provider cost — Backoff, attempt, duration, or circuit-breaker controls fail
- Stale-status conflict — Late callbacks and active retries disagree and move the message backward
- Secret or personal-data exposure — Fallback adaptation, provider errors, and diagnostics reveal protected content

Protect actor identity, tenant scope, authoritative objects, sensitive content, external proof, support tools, and audit records. Deny uncertain ownership or permission.

