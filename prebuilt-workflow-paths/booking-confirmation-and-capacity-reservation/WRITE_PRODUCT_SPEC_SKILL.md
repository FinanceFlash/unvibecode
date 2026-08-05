---
name: write-booking-confirmation-spec
description: Write or review a product specification for Booking Confirmation and Capacity Commitment. Use when defining actors, states, capacity or financial rules, policy decisions, edge cases, acceptance criteria, recovery, or business risks.
---

# Write a Booking Confirmation and Capacity Commitment Specification

Use application-native terms. Decide:
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

Write scope, actors, objects, states, paths, customer and business outcomes, permissions, recovery, privacy, misuse, acceptance criteria, and unanswered decisions.

