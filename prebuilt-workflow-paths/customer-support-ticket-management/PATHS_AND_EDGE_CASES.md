# Paths and Edge Cases

## Supported paths
- Web, mobile, API, email, or chat intake
- Automatic or manual triage and routing
- Agent assignment, transfer, return, and escalation
- Customer reply and waiting-for-customer
- Internal collaboration and specialist handoff
- Resolution, customer confirmation, auto-close, and reopen
- Duplicate merge, spam rejection, and out-of-scope routing
- Linked action, provider failure, retry, reconciliation, and manual repair

## Normal paths
- A valid customer issue becomes one acknowledged and correctly routed ticket
- An eligible agent owns, investigates, communicates, and resolves the issue
- A closed issue reopens within policy when the customer provides relevant new information

## Denied paths
- Required requester, account, contact, or issue details are missing or invalid
- Attachments are unsafe, unsupported, or excessive
- An unauthorized person attempts to view or update a ticket
- A duplicate, spam, or out-of-scope request is safely merged or rejected

## Timing, concurrency, and boundaries
- Two agents assign or update the ticket together
- A customer reply arrives exactly as the ticket auto-closes
- A reply arrives after closure or after the reopen window
- Tenant, customer, priority, or owner changes while work is active
- A linked refund or account correction succeeds while the support response is lost

Cover valid, invalid, duplicate, expired, stale, replayed, repeated, simultaneous, partially completed, unauthorized, and recovery outcomes.

