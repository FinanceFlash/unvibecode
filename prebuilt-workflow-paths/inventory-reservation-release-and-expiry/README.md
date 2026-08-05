# Inventory Reservation, Release, and Expiry

Starts when an eligible order or demand requests a quantity of a specific sellable resource. Ends when an exactly-once reservation is active, converted to committed consumption, released, expired, rejected, or visibly requires reconciliation while inventory quantities remain conserved.

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
- item, variant, location, quantity, availability, owner, and reservation eligibility
- atomic reservation, multi-line policy, partial allocation, backorder, and oversell controls
- reservation lifetime, extension, expiry, release, cancellation, and conversion
- concurrency, idempotency, scheduler, reconciliation, monitoring, audit, privacy, and abuse

## Excluded
- product search and availability display
- order placement and payment
- procurement and replenishment
- picking, packing, shipping, returns, and restock

The five `*_SKILL.md` files are self-contained.

