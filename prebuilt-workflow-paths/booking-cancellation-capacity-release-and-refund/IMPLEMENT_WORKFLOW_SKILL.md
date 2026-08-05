---
name: implement-booking-cancellation
description: Implement or modify Booking Cancellation, Capacity Release, and Refund Request. Use when adding or changing validation, authorization, state transitions, capacity or financial effects, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement Booking Cancellation and Capacity Release

Confirm:
- Who may cancel for the customer, tenant, provider, or resource
- Cancellation cut-off, timezone, grace, no-show, and service-start rules
- Immediate versus provider-approved cancellation
- Fee, penalty, refund-eligibility, and amount-basis policy
- When capacity is released and whether waitlist promotion begins
- Whether payment settlement or provider state can block cancellation
- How cancellation interacts with reschedule, check-in, completion, and disputes
- Cancellation idempotency and reversal policy
- Customer, provider, waitlist, refund, and support notification timing
- Abuse, privacy, audit, monitoring, and manual exception policy

Follow project conventions and protect:
- Only an authorized actor may cancel a current eligible booking
- Cancellation policy must use trusted booking state, time, timezone, and version
- Capacity release must equal unused committed capacity and happen exactly once
- Refund request must bind one cancellation, payment, customer, and policy basis
- Cancellation must not undo completed, checked-in, or superseded service outside explicit policy
- Retries and replays must not duplicate release, refund, waitlist, or notification effects
- Booking, provider, capacity, payment, refund, and communication must converge
- Customer and provider data must remain protected

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

