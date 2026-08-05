---
name: implement-subscription-renewal-cancellation
description: Implement or modify Subscription Renewal, Cancellation, and Entitlement Release. Use when adding or changing validation, authorization, state transitions, financial or access effects, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement Subscription Renewal and Cancellation

Confirm:
- Automatic-renewal eligibility and required advance notice
- Authoritative billing timezone, date, period start, and period end
- Immediate versus period-end cancellation
- Grace length, product access, payment retry, and dunning handoff
- Which cancellation or renewal actions require owner or administrator permission
- Price, tax, currency, invoice, and payment-method source at renewal
- Entitlement, seat, API key, data, export, and session behavior at termination
- Cancellation reversal and reactivation rules
- Provider cancellation and local subscription status precedence
- Rate, abuse, audit, notification, retention, and support policy

Follow project conventions and protect:
- One subscription period must produce at most one successful renewal
- Cancellation and renewal must bind the intended account, tenant, subscription, and version
- Trusted time must determine renewal, grace, and cancellation boundaries
- Paid access must remain until the written effective boundary
- Terminated access must be released consistently across all entitlement surfaces
- Uncertain payment must not cause duplicate billing or premature termination
- Concurrent and replayed actions must converge on one subscription state
- Billing and personal data must remain protected

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

