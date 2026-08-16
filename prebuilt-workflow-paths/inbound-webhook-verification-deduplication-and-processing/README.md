# Inbound Webhook Verification, Deduplication, and Processing

Starts when a provider, partner, or trusted internal system sends an HTTP webhook delivery to a configured endpoint. Ends when the delivery is rejected before side effects, durably accepted for processing, completed with an auditable result, or placed in an explicit recoverable failure state.

The primary outcome is to authenticate the intended delivery and apply its business effect no more than the provider contract and application policy allow.

| Task | File |
|---|---|
| Product and business | [PRODUCT_AND_BUSINESS_GUIDE.md](PRODUCT_AND_BUSINESS_GUIDE.md) |
| Engineering | [ENGINEERING_GUIDE.md](ENGINEERING_GUIDE.md) |
| Testing | [TESTING_GUIDE.md](TESTING_GUIDE.md) |
| Core 20 | [CORE_20_SCENARIOS.md](CORE_20_SCENARIOS.md) |
| Paths and edge cases | [PATHS_AND_EDGE_CASES.md](PATHS_AND_EDGE_CASES.md) |
| Permissions and misuse | [PERMISSION_AND_ABUSE_GUIDE.md](PERMISSION_AND_ABUSE_GUIDE.md) |
| Retry and recovery | [RETRY_AND_RECOVERY_GUIDE.md](RETRY_AND_RECOVERY_GUIDE.md) |
| Write a product specification | [WRITE_PRODUCT_SPEC_SKILL.md](WRITE_PRODUCT_SPEC_SKILL.md) |
| Review business risk | [REVIEW_BUSINESS_RISK_SKILL.md](REVIEW_BUSINESS_RISK_SKILL.md) |
| Understand existing code | [UNDERSTAND_CODE_SKILL.md](UNDERSTAND_CODE_SKILL.md) |
| Implement the workflow | [IMPLEMENT_WORKFLOW_SKILL.md](IMPLEMENT_WORKFLOW_SKILL.md) |
| Test the workflow | [TEST_WORKFLOW_SKILL.md](TEST_WORKFLOW_SKILL.md) |

## Included

- provider and tenant endpoint resolution, event and delivery identity, raw-body preservation, content limits, and schema versions
- signature, timestamp, replay-window, secret-rotation, permission, and provider-account checks
- durable inbox recording, acknowledgement policy, idempotency, duplicate handling, ordering, asynchronous workers, and leases
- retries, backoff, rate limits, dead-letter or quarantine handling, reconciliation, redrive, audit, metrics, and retention

## Excluded

- outgoing webhook delivery, subscription registration, and provider dashboard configuration
- OAuth authorization callbacks and account linking
- polling, cursor-based external-system synchronization, and bulk data import
- domain-specific payment, order, booking, notification, or entitlement lifecycles after the webhook is accepted

The five `*_SKILL.md` files are self-contained.
