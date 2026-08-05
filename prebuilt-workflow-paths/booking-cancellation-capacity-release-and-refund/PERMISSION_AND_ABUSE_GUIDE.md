# Permission and Abuse Guide

## Permission boundaries
- Only an authorized actor may cancel a current eligible booking
- Cancellation policy must use trusted booking state, time, timezone, and version
- Capacity release must equal unused committed capacity and happen exactly once
- Refund request must bind one cancellation, payment, customer, and policy basis
- Cancellation must not undo completed, checked-in, or superseded service outside explicit policy

## Misuse paths
- Unauthorized cancellation — Another account or tenant destroys a valid booking
- Capacity not released — Cancelled inventory remains unavailable and revenue is lost
- Excess capacity release — Duplicate cancellation or stale jobs oversell the slot
- Duplicate or wrong refund — Repeated handoff or wrong policy creates financial loss
- Incorrect penalty — Timezone or cut-off errors charge or deny the customer unfairly
- Booking–provider divergence — Local cancellation and external reservation disagree
- Cancellation after service — Stale action reverses a completed or checked-in booking
- Personal-data exposure — Schedule, customer, reason, payment, or provider data reaches unsafe logs

Protect actor identity, tenant scope, booking and capacity records, financial data, provider proof, support tools, and audit records. Deny uncertain ownership or permission.

