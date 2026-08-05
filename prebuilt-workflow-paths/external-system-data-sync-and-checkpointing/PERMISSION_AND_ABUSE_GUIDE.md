# Permission and Abuse Guide

## Permission boundaries
- Every sync operation must remain within its tenant, connection, entity, and field scope
- Stable source identity must map to one intended destination identity
- Checkpoint advancement must not skip unapplied required changes
- Replayed pages, records, and runs must be idempotent
- Version, conflict, source-of-truth, and deletion policy must protect newer state

## Misuse paths
- Missed records — Checkpoint advancement skips unapplied changes
- Duplicate records or effects — Replayed pages, unstable ids, or concurrent runs apply data repeatedly
- Destructive overwrite — Stale external data replaces newer authoritative destination state
- Wrong deletion — Out-of-order tombstones remove current records
- Cross-tenant synchronization — Connection, filter, id mapping, or cache mixes customer data
- Partial hidden success — Run reports complete despite failed records or destinations
- Runaway provider load — Paging, retries, or cursor loops consume quotas and cost
- Credential or data exposure — Tokens, source records, personal data, or errors reach unsafe logs

Protect actor identity, tenant scope, provider proof, connections, credentials, payloads or records, support tools, and audit history. Deny uncertain authenticity, ownership, or permission.

