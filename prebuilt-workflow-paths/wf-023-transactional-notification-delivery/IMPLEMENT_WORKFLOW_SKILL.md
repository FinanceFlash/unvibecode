---
name: implement-transactional-notification-delivery
description: Implement or modify Transactional Email, SMS, Push, or In-app Delivery. Use when adding or changing validation, authorization, state transitions, external effects, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement Transactional Notification Delivery

Confirm:
- Which events require a transactional notification
- How the authoritative recipient and tenant are resolved
- Transactional-purpose, consent, preference, suppression, and legal rules
- Channel priority, availability, verified-destination, and quiet-hours policy
- Template version, locale, variable, escaping, redaction, and attachment rules
- What personal or confidential data each channel may contain
- Deduplication key and exactly-once business-notification policy
- Provider success, accepted, delivered, bounced, expired, and failed meanings
- Which initial failures hand off to retry and fallback
- Rate, frequency, cost, provider, monitoring, and retention limits

Follow project conventions and protect:
- Only eligible business events may create transactional notifications
- Recipient, destination, purpose, tenant, and channel must come from authoritative policy
- Rendered content must use an approved version and only allowed recipient-scoped data
- One deduplication key must not create repeated recipient-visible messages
- Provider acceptance must not be mistaken for confirmed delivery
- Status changes and callbacks must be correlated and monotonic
- Uncertain outcomes must not trigger blind duplicate sends
- Provider credentials, secrets, destinations, and personal content must remain protected

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

