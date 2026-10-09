# Idempotent Request Processing and Concurrency Control

Starts when a client submits a state-mutating request that carries an idempotency key or requires exactly-once execution semantics. Ends when the request is accepted and its effect applied exactly once, rejected as a validated duplicate returning the original result, or denied because the key, lock, or concurrency constraint cannot be satisfied, with the outcome, key state, and audit record stored consistently.

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
- idempotency-key acceptance, format validation, binding, storage, and lifecycle
- duplicate detection, original-result retrieval, and safe replay
- optimistic and pessimistic concurrency controls for state-mutating operations
- distributed lock acquisition, lease renewal, expiry, and release
- request fingerprinting, payload-mismatch detection, and replay prevention
- key expiry, eviction, garbage collection, and storage-pressure handling
- audit, observability, privacy, and abuse controls for idempotent operations

## Excluded
- domain-specific business logic executed inside the idempotent boundary (covered by the relevant workflow pack)
- payment authorization and capture idempotency (covered by checkout-payment-authorization-and-capture)
- message-queue deduplication and consumer offset management as its own workflow
- database transaction isolation level selection and tuning

The five `*_SKILL.md` files are self-contained.
