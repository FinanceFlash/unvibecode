# Paths and Edge Cases

## Supported paths
- Confirmation from an active temporary hold
- Direct booking without a hold where allowed
- Payment-required confirmation
- Provider-approval or external-calendar confirmation
- Multi-person or multi-capacity booking
- Rejected, expired, unavailable, or ineligible request
- Uncertain provider or payment outcome
- Compensation, reconciliation, and manual repair

## Normal paths
- A valid active hold converts into one confirmed booking
- An allowed direct booking commits available capacity once
- Provider calendar, payment reference, confirmation, and reminders bind to the same booking

## Denied paths
- Customer, resource, provider, slot, timezone, party size, terms, or required reference is missing or invalid
- Hold, quote, slot, or terms have expired or changed
- Capacity is unavailable under policy
- The actor cannot book for the customer, tenant, provider, or resource

## Timing, concurrency, and boundaries
- Two customers confirm the last capacity together
- Hold conversion occurs exactly at expiry
- Timezone, daylight-saving, midnight, or date-boundary conversion changes the slot
- Provider accepts but the local response is lost
- Payment, provider rejection, or capacity change arrives after local confirmation

Cover valid, invalid, duplicate, expired, stale, replayed, repeated, simultaneous, partially completed, unauthorized, and recovery outcomes.

