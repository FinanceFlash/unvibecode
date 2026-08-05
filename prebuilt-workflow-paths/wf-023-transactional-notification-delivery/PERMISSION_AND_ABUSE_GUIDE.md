# Permission and Abuse Guide

## Permission boundaries
- Only eligible business events may create transactional notifications
- Recipient, destination, purpose, tenant, and channel must come from authoritative policy
- Rendered content must use an approved version and only allowed recipient-scoped data
- One deduplication key must not create repeated recipient-visible messages
- Provider acceptance must not be mistaken for confirmed delivery

## Misuse paths
- Wrong recipient — Account, tenant, destination, or identity resolution sends protected information elsewhere
- Ineligible channel — Preference, consent, verification, suppression, or purpose rules are bypassed
- Duplicate notification — Replayed events or lost responses send the same business message repeatedly
- Missing critical notice — The application records success although no provider attempt or recoverable handoff exists
- Unsafe rendering — Template variables, markup, links, or attachments expose data or enable injection
- False delivery state — Provider acceptance is recorded as final delivery or callbacks move status backward
- Message amplification — One event or attacker triggers unbounded provider traffic and cost
- Secret or personal-data exposure — Destinations, content, tokens, provider responses, or credentials reach unsafe logs

Protect actor identity, tenant scope, authoritative objects, sensitive content, external proof, support tools, and audit records. Deny uncertain ownership or permission.

