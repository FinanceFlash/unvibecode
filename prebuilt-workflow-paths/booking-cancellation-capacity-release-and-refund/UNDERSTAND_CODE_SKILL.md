---
name: understand-booking-cancellation-code
description: Trace and explain Booking Cancellation, Capacity Release, and Refund Request across an existing codebase. Use when locating entry points, authorization, state, provider calls, capacity or financial effects, retries, recovery, monitoring, and tests.
---

# Understand Booking Cancellation and Capacity Release Code

Trace:
1. Cancel, provider-cancel, administrative cancel, status, compensation, and support entry points
2. Customer, account, tenant, provider, booking-owner, and permission checks
3. Booking status, version, slot, timezone, cut-off, reason, fee, penalty, and refund-basis evaluation
4. Cancellation model, idempotency, uniqueness, transaction, versioning, and concurrency controls
5. Exact capacity release, waitlist handoff, and stale-release protection
6. Refund-request creation and payment-reference binding
7. Provider cancellation, timeout, callback, customer and provider notification
8. Audit, privacy, abuse, monitoring, reconciliation, support tools, and tests

Explain actors, ownership, states, transitions, quantities or money, effects, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.

