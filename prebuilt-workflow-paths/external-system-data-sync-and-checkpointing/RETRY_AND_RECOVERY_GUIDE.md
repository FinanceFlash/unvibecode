# Retry and Recovery Guide

## Partial failures
- Some records apply but a later record or page fails
- Records apply but checkpoint commit fails
- Checkpoint commits but run summary or audit fails
- Source returns a page but the response is lost
- Destination updates one system but a dependent projection fails
- Deletion applies locally but source acknowledgement or reconciliation fails

## Recovery rules
- Keep run, configuration, connection, entity, checkpoint, page, record, and destination identities correlated.
- Re-read current destination version and authoritative source state before retrying changes.
- Do not advance checkpoint beyond unresolved required work.
- Make replay safe for already-applied records and pages.
- Reconcile source, destination, checkpoint, per-record results, drift, metrics, and audit.

