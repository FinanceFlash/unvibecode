# Product and Business Guide

## Boundary
Starts when an authorized actor requests cancellation of an existing booking. Ends when cancellation is denied or becomes authoritative, unused capacity is released once, any refund request is created once, and provider, waitlist, payment, and customer communication are reconciled.

## People and systems
- Customer or authorized booking manager
- Service provider or resource owner
- Booking and capacity services
- Cancellation-policy and pricing services
- Payment and refund services
- External provider calendar or reservation system
- Waitlist, notification, support, and operations teams

## Things created or changed
- Booking, customer, tenant, provider, resource, slot, and status
- Cancellation request, actor, reason, request time, and idempotency key
- Cut-off, fee, penalty, refund eligibility, and refund amount basis
- Capacity release and availability update
- Refund request and payment reference
- Provider cancellation and waitlist-promotion handoff
- Notification and audit record

## Stages
- Booking: confirmed → cancellation requested → cancelled or retained
- Cancellation: requested → evaluating → denied, effective, uncertain, or exception
- Capacity: committed → released or retained
- Refund request: absent → created, not eligible, pending, or failed
- Provider booking: active → cancelled, uncertain, or exception

## Product decisions
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

## Happy paths
- An eligible cancellation changes the booking once and releases exact unused capacity
- A refund-eligible cancellation creates one refund request with the correct basis
- Provider and customer notifications and waitlist handoff reflect the same cancellation

## Negative paths
- Booking, actor, reason, status, or required cancellation data is missing or invalid
- Cancellation is outside the allowed cut-off or the service already started or completed
- The actor cannot cancel the booking
- The booking is already cancelled, rescheduled, refunded, or owned elsewhere

## Edge cases
- Cancellation races with reschedule, check-in, completion, or provider acceptance
- Request arrives exactly at the cancellation cut-off
- Two actors cancel the same booking together
- Provider cancellation succeeds but the local response is lost
- Late provider or payment events arrive after cancellation

## Acceptance criteria
1. Only an authorized actor may cancel an eligible current booking
2. Cancellation must bind the intended customer, tenant, provider, booking, slot, version, and policy
3. Trusted time and timezone must determine cut-off, fee, and refund eligibility
4. One cancellation must release unused capacity at most once
5. Refund handoff must be created at most once using the authoritative cancellation basis
6. Cancelled, completed, no-show, or superseded bookings cannot be cancelled again outside explicit policy
7. Provider, booking, capacity, waitlist, payment, refund, and notifications must converge
8. Repeated or simultaneous actions must return one cancellation outcome
9. Customer, schedule, payment, reason, and provider data must remain protected
10. Partial failure must remain visible, auditable, and repairable

## Business risks
| Risk | Business consequence |
|---|---|
| Unauthorized cancellation | Another account or tenant destroys a valid booking |
| Capacity not released | Cancelled inventory remains unavailable and revenue is lost |
| Excess capacity release | Duplicate cancellation or stale jobs oversell the slot |
| Duplicate or wrong refund | Repeated handoff or wrong policy creates financial loss |
| Incorrect penalty | Timezone or cut-off errors charge or deny the customer unfairly |
| Booking–provider divergence | Local cancellation and external reservation disagree |
| Cancellation after service | Stale action reverses a completed or checked-in booking |
| Personal-data exposure | Schedule, customer, reason, payment, or provider data reaches unsafe logs |

