---
name: implement-booking-confirmation
description: Implement or modify Booking Confirmation and Capacity Commitment. Use when adding or changing validation, authorization, state transitions, capacity or financial effects, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement Booking Confirmation and Capacity Commitment

Confirm:
- Who may book for which customer, tenant, provider, resource, or attendee
- Whether a temporary hold is required before confirmation
- Authoritative timezone, slot boundaries, duration, party size, and capacity units
- Quote, terms, hold, and booking-request lifetime
- Payment authorization or capture prerequisite
- Atomicity across booking, capacity, payment, and external provider
- Overbooking, waitlist, partial capacity, and provider-approval policy
- Booking id, confirmation number, and idempotency policy
- Confirmation, reminder, calendar, and provider-notification timing
- Rate, bot, privacy, audit, monitoring, and manual-review policy

Follow project conventions and protect:
- One intended request or hold must create at most one booking
- Committed capacity must remain conserved and within policy
- Booking must bind the intended customer, tenant, provider, resource, slot, timezone, and party size
- Trusted time and current state must govern hold and quote validity
- Payment and provider prerequisites must follow explicit confirmation policy
- Retries and replays must not duplicate booking or capacity effects
- Booking, capacity, payment, provider, and communication must converge
- Customer and provider data must remain protected

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

