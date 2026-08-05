# Failed Notification Retry and Channel Fallback

Starts when an initial transactional notification attempt has a recorded retryable or uncertain failure. Ends when the message is delivered once, expires, is suppressed, reaches a bounded final failure, or is escalated for explicit operational handling.

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
- failure classification, retry eligibility, schedule, backoff, jitter, and attempt limits
- uncertain provider outcomes, callbacks, deduplication, and concurrency
- fallback-channel eligibility, content adaptation, quiet hours, expiry, and recipient policy
- final failure, dead-letter or manual review, reconciliation, audit, privacy, cost, and misuse

## Excluded
- creating the original business notification
- marketing campaign retry policy
- inbound message handling
- template-authoring administration

The five `*_SKILL.md` files are self-contained.

