# Paths and Edge Cases

## Supported paths
- Incremental pull sync
- Full snapshot sync
- Push or bidirectional sync where explicitly allowed
- No-change run
- Create and update mapping
- Deletion or tombstone propagation
- Partial batch, quarantine, resume, and targeted replay
- Credential failure, provider outage, reconciliation, and manual repair

## Normal paths
- An incremental sync applies all eligible changes once and advances the checkpoint
- A no-change run confirms source state without modifying records
- An authorized deletion or tombstone removes or deactivates the intended destination record

## Denied paths
- Sync definition, tenant, connection, entity, cursor, mapping, or credential is missing or invalid
- The source or destination is unauthorized or unavailable
- A record violates schema, ownership, version, or conflict policy
- A stale update or deletion would overwrite newer authoritative state

## Timing, concurrency, and boundaries
- Two sync runs overlap for the same scope
- A change occurs exactly at checkpoint or watermark boundary
- Source pages reorder, repeat, or change during pagination
- Records apply but checkpoint persistence fails
- Credential, schema, mapping, or source version changes mid-run

Cover valid, invalid, duplicate, stale, replayed, repeated, simultaneous, partially completed, unauthorized, out-of-order, and recovery outcomes.

