---
name: understand-booking-confirmation-code
description: Trace and explain Booking Confirmation and Capacity Commitment across an existing codebase. Use when locating entry points, authorization, state, provider calls, capacity or financial effects, retries, recovery, monitoring, and tests.
---

# Understand Booking Confirmation and Capacity Commitment Code

Trace:
1. Confirm, direct-book, provider-accept, status, compensation, and support entry points
2. Customer, account, tenant, provider, resource, attendee, and permission checks
3. Slot, timezone, duration, party size, capacity, quote, terms, hold, and expiry validation
4. Booking model, confirmation number, idempotency, uniqueness, versioning, transaction, and concurrency controls
5. Capacity hold conversion or direct commitment
6. Payment prerequisite, provider calendar request, timeout, and uncertain result
7. Confirmation, reminder, notification, ledger, and operational effects
8. Audit, privacy, abuse, monitoring, reconciliation, support tools, and tests

Explain actors, ownership, states, transitions, quantities or money, effects, failures, retries, security boundaries, monitoring, tests, and areas needing verification. Cite files and symbols.

