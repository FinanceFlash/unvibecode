# Booking Cancellation, Capacity Release, and Refund Request

Starts when an authorized actor requests cancellation of an existing booking. Ends when cancellation is denied or becomes authoritative, unused capacity is released once, any refund request is created once, and provider, waitlist, payment, and customer communication are reconciled.

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
- actor, booking, provider, status, cancellation eligibility, cut-off, reason, and fee policy
- authoritative cancellation and exact capacity release
- refund-request handoff without owning refund approval or payment execution
- provider cancellation, waitlist handoff, notification, audit, retry, recovery, privacy, and misuse

## Excluded
- booking creation and confirmation
- booking reschedule and atomic capacity move
- refund approval and payment issuance
- check-in, attendance, and service completion

The five `*_SKILL.md` files are self-contained.

