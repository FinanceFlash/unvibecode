# Permission and Abuse Guide

## Permission boundaries
- One intended request or hold must create at most one booking
- Committed capacity must remain conserved and within policy
- Booking must bind the intended customer, tenant, provider, resource, slot, timezone, and party size
- Trusted time and current state must govern hold and quote validity
- Payment and provider prerequisites must follow explicit confirmation policy

## Misuse paths
- Double booking — Concurrent confirmations commit the same exclusive capacity
- Wrong slot or resource — Timezone, identity, or mapping errors confirm a different service
- Booking–capacity divergence — The customer is confirmed without capacity or capacity is consumed without a booking
- Payment–booking divergence — Money moves without a reservation or a booking confirms without required payment
- Stale hold or quote — Expired terms, price, or capacity is committed
- Unauthorized booking — Another account or tenant controls customer, provider, or resource
- False confirmation — The customer receives success while provider or capacity commitment is missing
- Personal-data exposure — Contact, attendee, schedule, payment, or provider data reaches unsafe logs

Protect actor identity, tenant scope, booking and capacity records, financial data, provider proof, support tools, and audit records. Deny uncertain ownership or permission.

