---
name: understand-subscription-renewal-cancellation-code
description: Trace and explain Subscription Renewal, Cancellation, and Entitlement Release across an existing codebase. Use when locating entry points, authorization, state, provider calls, financial or access effects, retries, recovery, monitoring, and tests.
---

# Understand Subscription Renewal and Cancellation Code

Trace:
1. Renewal scheduler, manual renew, cancel, reverse, reactivate, grace, terminate, and provider-callback entry points
2. Actor, owner, tenant, account, plan, subscription-state, and permission checks
3. Billing timezone, period, price, currency, tax, invoice, and payment-method resolution
4. Renewal and cancellation models, idempotency, uniqueness, versioning, and concurrency controls
5. Payment request, provider status, timeout, retry handoff, and uncertain result
6. Subscription period, grace, cancellation, reactivation, and terminal-state transitions
7. Entitlement, seat, session, API key, data, invoice, and notification effects
8. Audit, privacy, monitoring, reconciliation, support tools, and tests

Explain actors, ownership, amounts or access, states, transitions, effects, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.

