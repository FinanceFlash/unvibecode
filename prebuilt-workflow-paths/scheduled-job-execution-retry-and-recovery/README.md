# Scheduled Job Execution, Checkpoint, Retry, and Recovery

Starts when an enabled schedule makes a bounded job run due or an authorized operator requests an equivalent manual run. Ends when one run completes, safely records no work, remains partially failed with repair work, exhausts retries, or is cancelled—with its lease, input window, outputs, checkpoint, alerts, and audit state consistent.

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
- schedule, timezone, daylight-saving behavior, misfire, catch-up, manual trigger, and run identity
- claim, lease, heartbeat, overlap prevention, input window, checkpoint, pagination, batching, and item outcomes
- business effects, idempotency, timeout, cancellation, retry, backoff, dead letter, rerun, and repair
- tenant isolation, secrets, monitoring, alerts, run history, retention, reconciliation, and audit

## Excluded
- general queue-consumer acknowledgement and poison-message lifecycle
- domain-specific external-system synchronization rules
- model feature, inference, and threshold-decision logic
- business meaning of the job's domain records beyond safe execution

The five `*_SKILL.md` files are self-contained.

