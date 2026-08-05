# Paths and Edge Cases

## Supported paths
- Full eligible account erasure
- Partial erasure with lawful retention
- Irreversible anonymization
- Representative request
- Request denial or identity failure
- Legal hold and later release
- Third-party processor deletion
- Backup expiry, reappearance prevention, reconciliation, and manual repair

## Normal paths
- A verified eligible request deletes or anonymizes all in-scope data and closes with evidence
- A lawful retention exception preserves only required data with restricted purpose and recorded expiry
- Third-party processors acknowledge and complete their required deletion tasks

## Denied paths
- Requester, account, identity proof, authority, or scope is missing or invalid
- Identity verification fails or representative authority is insufficient
- A lawful hold or retention obligation blocks some or all deletion
- The request targets another account, tenant, shared record, or out-of-scope data

## Timing, concurrency, and boundaries
- Two deletion requests or account actions execute together
- Retention or legal hold expires exactly during deletion
- New data, messages, events, or backups appear after inventory snapshot
- A processor deletes data but acknowledgement is lost
- Account deletion overlaps payment, dispute, security investigation, or recovery

Cover valid, invalid, duplicate, stale, replayed, repeated, simultaneous, partially completed, unauthorized, expired, and recovery outcomes.

