# External-system Synchronization and Checkpointing

Starts when a scheduled job, event, or authorized request begins synchronization for a defined source, destination, tenant, and scope. Ends when eligible changes are applied and the checkpoint advances safely, no changes are confirmed, or partial failure remains explicit and recoverable without silent loss or overwrite.

| Task | File |
|---|---|
| Product and business | [PRODUCT_AND_BUSINESS_GUIDE.md](PRODUCT_AND_BUSINESS_GUIDE.md) |
| Engineering | [ENGINEERING_GUIDE.md](ENGINEERING_GUIDE.md) |
| Testing | [TESTING_GUIDE.md](TESTING_GUIDE.md) |
| Core 20 | [CORE_20_SCENARIOS.md](CORE_20_SCENARIOS.md) |
| Paths and edge cases | [PATHS_AND_EDGE_CASES.md](PATHS_AND_EDGE_CASES.md) |
| Permissions and misuse | [PERMISSION_AND_ABUSE_GUIDE.md](PERMISSION_AND_ABUSE_GUIDE.md) |
| Retry and recovery | [RETRY_AND_RECOVERY_GUIDE.md](RETRY_AND_RECOVERY_GUIDE.md) |

## Included
- full or incremental sync, scope, source and destination authorization, cursor, checkpoint, paging, and batching
- schema mapping, identity mapping, creates, updates, deletions, tombstones, ordering, and conflict policy
- rate limits, retries, backoff, partial batches, idempotency, reconciliation, and checkpoint advancement
- credentials, privacy, tenant isolation, monitoring, audit, manual repair, and misuse

## Excluded
- single inbound webhook verification
- general data import from a user-uploaded file
- business-specific payment or notification reconciliation
- one-time data export delivery

The five `*_SKILL.md` files are self-contained.

