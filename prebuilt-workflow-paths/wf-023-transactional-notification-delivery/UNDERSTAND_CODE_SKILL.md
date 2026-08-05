---
name: understand-transactional-notification-delivery-code
description: Trace and explain Transactional Email, SMS, Push, or In-app Delivery across an existing codebase. Use when locating entry points, authorization, state, storage, external effects, retries, recovery, monitoring, and tests.
---

# Understand Transactional Notification Delivery Code

Trace:
1. Business-event producers and notification-request entry points
2. Event eligibility, deduplication, purpose, tenant, recipient, preference, consent, and suppression checks
3. Destination verification, channel selection, quiet-hours, expiry, and provider routing
4. Template lookup, version, locale, variables, escaping, redaction, links, and attachments
5. Message and attempt storage, transactions, uniqueness, and simultaneous-event handling
6. Provider client, credentials, timeouts, accepted result, and provider reference
7. Callback correlation, monotonic status, failure classification, and retry handoff
8. Audit, privacy, retention, monitoring, support tools, and tests

Explain actors, ownership, states, transitions, effects, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.

