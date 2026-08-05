---
name: write-transactional-notification-delivery-spec
description: Write or review a product specification for Transactional Email, SMS, Push, or In-app Delivery. Use when defining actors, states, permissions, policy decisions, normal paths, edge cases, acceptance criteria, recovery, or business risks.
---

# Write a Transactional Notification Delivery Specification

Use application-native terms. Decide:
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

Write scope, actors, objects, states, paths, customer outcomes, permissions, recovery, privacy, misuse, acceptance criteria, and unanswered decisions.

