# Product and Business Guide

## Boundary
Starts when a customer has an eligible resource or service request, with any required quote or temporary hold. Ends when one reservation is rejected, committed and confirmed, or remains explicitly uncertain with capacity, payment, provider calendar, and customer communication reconciled.

## People and systems
- Customer or authorized booker
- Resource owner or service provider
- Booking and capacity service
- Pricing, policy, and payment services
- Provider calendar or external reservation system
- Notification and reminder services
- Support, finance, security, and operations teams

## Things created or changed
- Booking request, quote, and terms
- Customer, account, tenant, attendee, or party
- Resource, service, provider, location, slot, timezone, and capacity units
- Temporary hold and expiry
- Booking, confirmation number, idempotency key, and version
- Payment, calendar, reminder, and notification references
- Capacity movement and audit record

## Stages
- Request: eligible → confirming → rejected, confirmed, or uncertain
- Hold: active → converted, expired, released, or invalid
- Booking: absent → committing → confirmed, pending, failed, or cancelled by compensation
- Capacity: available or held → committed
- External calendar: pending → accepted, rejected, uncertain, or repaired

## Product decisions
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

## Happy paths
- A valid active hold converts into one confirmed booking
- An allowed direct booking commits available capacity once
- Provider calendar, payment reference, confirmation, and reminders bind to the same booking

## Negative paths
- Customer, resource, provider, slot, timezone, party size, terms, or required reference is missing or invalid
- Hold, quote, slot, or terms have expired or changed
- Capacity is unavailable under policy
- The actor cannot book for the customer, tenant, provider, or resource

## Edge cases
- Two customers confirm the last capacity together
- Hold conversion occurs exactly at expiry
- Timezone, daylight-saving, midnight, or date-boundary conversion changes the slot
- Provider accepts but the local response is lost
- Payment, provider rejection, or capacity change arrives after local confirmation

## Acceptance criteria
1. Only an eligible current request may create a booking
2. Customer, tenant, provider, resource, location, slot, timezone, duration, party size, terms, and price must bind to one booking
3. One hold or idempotency key must not create duplicate bookings
4. Committed capacity must not exceed policy under concurrency
5. Expired, released, consumed, or mismatched holds cannot confirm
6. Payment prerequisites must follow explicit booking-confirmation policy
7. Booking, capacity, payment, provider calendar, reminder, and confirmation must converge
8. Repeated or lost-response execution must return one authoritative booking outcome
9. Customer, attendee, contact, payment, and provider data must remain protected
10. Partial failure must remain visible, auditable, and repairable

## Business risks
| Risk | Business consequence |
|---|---|
| Double booking | Concurrent confirmations commit the same exclusive capacity |
| Wrong slot or resource | Timezone, identity, or mapping errors confirm a different service |
| Booking–capacity divergence | The customer is confirmed without capacity or capacity is consumed without a booking |
| Payment–booking divergence | Money moves without a reservation or a booking confirms without required payment |
| Stale hold or quote | Expired terms, price, or capacity is committed |
| Unauthorized booking | Another account or tenant controls customer, provider, or resource |
| False confirmation | The customer receives success while provider or capacity commitment is missing |
| Personal-data exposure | Contact, attendee, schedule, payment, or provider data reaches unsafe logs |

