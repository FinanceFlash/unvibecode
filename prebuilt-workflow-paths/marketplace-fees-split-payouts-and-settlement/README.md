# Commission, Fee, Split Payout, and Seller Settlement

Starts when a marketplace transaction is complete and eligible for settlement. Ends when gross value is conserved across fees, taxes, reserves, adjustments, and payee amounts and each payout is held, submitted, paid, failed, or reversed exactly once with ledger and transaction state reconciled.

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
- settlement eligibility, delay, reserve, completed value, currency, and version
- commission, fee, tax, withholding, adjustment, split, and rounding calculation
- seller or provider payee eligibility, payout method, batching, minimums, and provider submission
- ledger, payout status, callback, retry, reconciliation, privacy, audit, and misuse

## Excluded
- buyer payment authorization and capture
- escrow funding and conditional release
- marketplace dispute investigation
- refund and chargeback processing

The five `*_SKILL.md` files are self-contained.

