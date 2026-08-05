# Checkout Payment Authorization and Capture

Starts when a validated checkout has an authoritative payable amount. Ends when payment is declined, requires further customer action, is authorized or captured once, or remains explicitly uncertain with the order, ledger, and customer outcome recorded consistently.

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
- payable order validation, amount, currency, payer, and payment-attempt creation
- fraud or risk decision, customer authentication, authorization, capture, void, and decline
- provider idempotency, timeout, uncertain outcome, reconciliation handoff, and retries
- order-payment state, ledger or financial record, receipt, privacy, monitoring, and misuse

## Excluded
- payment-method setup and verification
- asynchronous provider callback reconciliation as its own workflow
- refunds, disputes, and chargebacks
- subscription renewal and cancellation

The five `*_SKILL.md` files are self-contained.

