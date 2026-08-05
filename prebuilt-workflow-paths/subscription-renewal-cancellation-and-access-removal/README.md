# Subscription Renewal, Cancellation, and Entitlement Release

Starts at an automatic renewal boundary or an authorized cancellation request. Ends when the subscription is renewed, enters an explicit past-due or grace state, is scheduled to cancel, terminates, or is restored with billing and product access reconciled.

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
- renewal eligibility, billing period, payment attempt, grace, retry handoff, and notices
- immediate or period-end cancellation, reversal, reactivation, and termination
- entitlement continuation, grace access, release, session consequences, and data policy
- provider state, concurrency, idempotency, privacy, monitoring, retry, and recovery

## Excluded
- initial subscription purchase and activation
- plan upgrade, downgrade, and proration
- standalone payment-method setup
- refund and dispute processing

The five `*_SKILL.md` files are self-contained.

