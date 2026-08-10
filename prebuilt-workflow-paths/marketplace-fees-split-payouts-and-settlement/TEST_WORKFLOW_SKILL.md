---
name: test-marketplace-settlement
description: Design, implement, or review tests for Commission, Fee, Split Payout, and Seller Settlement. Use when complete normal, invalid, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test Marketplace Split Payout and Settlement

Cover:
1. Eligible transaction settles once
2. Multi-party split balances
3. Small balance carries forward
4. Required settlement data is missing
5. Financial input is invalid
6. Transaction is ineligible or held
7. Actor cannot trigger settlement
8. Currency and rounding reach boundary
9. Two workers settle same transaction
10. Eligibility changes at boundary
11. Settlement response is lost
12. Transaction event is replayed
13. Payout or bank change is abused
14. Ledger posts but provider submission fails
15. Payout provider times out
16. Provider pays but response is lost
17. Cross-tenant payee is supplied
18. Settlement error is logged
19. Late refund or dispute follows settlement
20. Provider pays but ledger update fails

For each scenario write Given, When, expected response and authoritative financial state changes, forbidden outcomes, test level, fixtures, controlled time or provider behaviour, and cleanup.

