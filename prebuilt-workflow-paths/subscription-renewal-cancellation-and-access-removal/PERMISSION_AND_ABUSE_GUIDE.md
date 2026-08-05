# Permission and Abuse Guide

## Permission boundaries
- One subscription period must produce at most one successful renewal
- Cancellation and renewal must bind the intended account, tenant, subscription, and version
- Trusted time must determine renewal, grace, and cancellation boundaries
- Paid access must remain until the written effective boundary
- Terminated access must be released consistently across all entitlement surfaces

## Misuse paths
- Duplicate renewal charge — Scheduler replay or concurrency bills one period more than once
- Premature access loss — Cancellation or partial failure removes paid entitlement too early
- Free continued access — Termination fails to release entitlement, seats, keys, or sessions
- Billing–access divergence — Payment, invoice, subscription, and entitlement disagree
- Unauthorized cancellation — Another user or tenant terminates a paid subscription
- Missed renewal — A valid due subscription is skipped or silently stranded
- Hidden or ineffective cancellation — The customer believes renewal stopped but billing continues
- Sensitive-data exposure — Billing, payment, cancellation, or account data reaches unsafe logs

Protect actor identity, tenant scope, authoritative business objects, financial data, provider proof, support tools, and audit records. Deny uncertain ownership or permission.

