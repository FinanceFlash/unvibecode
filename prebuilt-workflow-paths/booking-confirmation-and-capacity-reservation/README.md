# Booking Confirmation and Capacity Commitment

Starts when a customer has an eligible resource or service request, with any required quote or temporary hold. Ends when one reservation is rejected, committed and confirmed, or remains explicitly uncertain with capacity, payment, provider calendar, and customer communication reconciled.

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
- customer, provider, resource, service, location, slot, party size, and eligibility validation
- quote, terms, hold, payment prerequisite, booking id, idempotency, and commit
- capacity commitment, provider-calendar handoff, confirmation, reminder setup, and audit
- concurrency, timezone, expiry, provider failure, privacy, retry, reconciliation, and misuse

## Excluded
- availability publishing and schedule administration
- availability search, booking quote, and temporary hold creation
- booking reschedule and cancellation
- check-in, attendance, and service completion

The five `*_SKILL.md` files are self-contained.

