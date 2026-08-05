# Order Placement and Confirmation

Starts when a checkout is ready to place with an authoritative customer, item snapshot, price, address, and payment policy. Ends when one immutable order is rejected, committed and confirmed, or remains explicitly uncertain with payment, inventory, fulfilment, and customer communication reconciled.

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
- checkout eligibility, customer or guest identity, item and price snapshot, address, terms, and totals
- order id, line items, financial snapshot, idempotency, commit, and confirmation
- payment-result and inventory-reservation handoffs without owning those separate workflows
- fulfilment request, receipt or confirmation, audit, privacy, concurrency, retry, and recovery

## Excluded
- shopping-cart construction and merge
- product price quoting and promotion calculation
- payment authorization and capture
- pick, pack, shipment, return, and refund

The five `*_SKILL.md` files are self-contained.

