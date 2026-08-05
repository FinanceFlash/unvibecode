# Testing Guide

Check authoritative proof, tenant mapping, records, checkpoints, downstream handoff, recovery, and audit—not only responses.

## 1. Incremental sync advances safely

**Given:** A valid connection has changes after the committed checkpoint

**When:** The run fetches and applies all required changes

**Expect:** Records update once and the checkpoint advances to the safe boundary

**Must not happen:** A record is skipped or applied repeatedly

**Best test levels:** Integration and end-to-end.

## 2. No-change run is a no-op

**Given:** The source reports no eligible changes after the checkpoint

**When:** The sync completes

**Expect:** No destination data changes and run status is complete

**Must not happen:** Checkpoint or records mutate without source change

**Best test levels:** Integration.

## 3. Authorized deletion propagates

**Given:** A valid tombstone targets an existing mapped record under deletion policy

**When:** The record is processed

**Expect:** The destination deletes, archives, or deactivates exactly as specified

**Must not happen:** Another record is removed or history disappears unexpectedly

**Best test levels:** Integration.

## 4. Sync definition is incomplete

**Given:** Tenant, connection, source, destination, entity, filter, mapping, or checkpoint configuration is missing

**When:** Validation runs

**Expect:** The sync fails before reading or writing records

**Must not happen:** A default global scope is used

**Best test levels:** Unit and API.

## 5. Source record is malformed

**Given:** A record violates schema, type, precision, encoding, required field, or size limits

**When:** Mapping runs

**Expect:** It is rejected or quarantined with explicit run status

**Must not happen:** Malformed data corrupts the destination

**Best test levels:** Unit and integration.

## 6. Connection lacks permission

**Given:** Credentials cannot read the source scope or write the destination fields

**When:** The run starts

**Expect:** Authorization fails without partial unauthorized access

**Must not happen:** Broader fallback credentials are used

**Best test levels:** Authorization and security.

## 7. Stale source record conflicts

**Given:** A source update is older than current authoritative destination state

**When:** Conflict logic runs

**Expect:** Source-of-truth and version policy preserve or explicitly resolve state

**Must not happen:** Newer data is overwritten silently

**Best test levels:** Integration.

## 8. Identity and values normalize consistently

**Given:** External ids, enums, nulls, timezones, decimals, or names use variant representations

**When:** Mapping runs

**Expect:** One documented mapping creates the intended canonical record

**Must not happen:** Variants create duplicates or change meaning

**Best test levels:** Unit and property.

## 9. Two sync runs overlap

**Given:** Two runs use the same tenant, connection, entity, and starting checkpoint

**When:** Both execute

**Expect:** Lease or idempotency policy prevents conflicting application and checkpoint changes

**Must not happen:** Runs duplicate records or move checkpoint inconsistently

**Best test levels:** Concurrency integration.

## 10. Change occurs at checkpoint boundary

**Given:** Source changes are created before, at, and after the watermark

**When:** Incremental selection runs

**Expect:** Inclusive or exclusive plus overlap policy captures each required change

**Must not happen:** A boundary record is skipped permanently

**Best test levels:** Unit with controlled source.

## 11. Page response is lost

**Given:** The source page may have been fetched or records may have applied

**When:** The page retries

**Expect:** Stable page and record identities make replay safe

**Must not happen:** Records duplicate or checkpoint skips ahead

**Best test levels:** Integration.

## 12. Batch or run is replayed

**Given:** A completed page, record, or run identity is delivered again

**When:** Processing repeats

**Expect:** Applied records no-op or update idempotently and checkpoint remains safe

**Must not happen:** Business effects repeat

**Best test levels:** Worker integration.

## 13. Sync scope is excessive

**Given:** One run requests unbounded history, pages, records, fields, or retries

**When:** Limits and rate policy run

**Expect:** Load, duration, memory, provider quota, and cost remain bounded

**Must not happen:** A sync monopolizes systems or loops forever

**Best test levels:** Load and resilience.

## 14. Records apply but checkpoint fails

**Given:** Destination changes commit while the checkpoint remains old

**When:** Recovery reruns from the earlier boundary

**Expect:** Already-applied records are idempotent and remaining changes complete

**Must not happen:** Replay duplicates effects or operators advance manually past failures

**Best test levels:** Integration and operations.

## 15. External provider times out

**Given:** Source fetch or destination API returns uncertain status

**When:** Failure handling runs

**Expect:** The run and record remain explicit and retry is bounded

**Must not happen:** Uncertainty becomes success or blind duplicate write

**Best test levels:** Provider contract and integration.

## 16. Checkpoint commits but response is lost

**Given:** The run may have safely advanced while scheduler sees failure

**When:** The run repeats

**Expect:** Current checkpoint and record state prevent duplicate outcomes

**Must not happen:** A second run overwrites or duplicates data

**Best test levels:** Integration.

## 17. Cross-tenant connection is referenced

**Given:** A valid operator or job uses another tenant's source, destination, or mapping

**When:** The sync starts

**Expect:** Tenant and connection binding deny the run

**Must not happen:** Identifiers or caches mix customer data

**Best test levels:** Authorization and security.

## 18. Sync failure is logged

**Given:** The path contains credentials, source records, personal data, mappings, and provider errors

**When:** An error occurs

**Expect:** Diagnostics avoid secrets and unnecessary sensitive content

**Must not happen:** Tokens or protected records reach logs

**Best test levels:** Security and log inspection.

## 19. Delete arrives after newer update

**Given:** An out-of-order tombstone targets a record with a newer authoritative version

**When:** Processing runs

**Expect:** Version and deletion policy prevents stale removal

**Must not happen:** Current data is deleted

**Best test levels:** Integration.

## 20. Partial batch fails

**Given:** Some records succeed and others conflict, fail, or quarantine

**When:** Completion and checkpoint logic run

**Expect:** Per-record outcomes remain visible and checkpoint follows explicit safe policy

**Must not happen:** Run reports complete or skips failed work

**Best test levels:** Integration and operations.

