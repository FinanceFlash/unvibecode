---
name: test-dispute-chargeback
description: Design, implement, or review tests for Payment Dispute and Chargeback Resolution. Use when complete normal, invalid, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test Payment Dispute and Chargeback Resolution

Cover:
1. Valid dispute opens against a captured payment
2. Complete evidence is submitted before the deadline
3. Low-value dispute is auto-accepted by policy
4. Authenticated transaction wins on liability shift
5. Required dispute fields are missing
6. Dispute amount or currency mismatches the payment
7. Actor without dispute-team access submits evidence
8. Evidence deadline is reached at a timezone boundary
9. Two dispute webhooks arrive together for one case
10. Provider retries the dispute-opened notification
11. Representment response from the network is lost
12. Case is escalated to pre-arbitration after resolution
13. Merchant chargeback ratio crosses the risk threshold
14. Cardholder withdraws the dispute after representment
15. Provisional debit succeeds but the ledger write fails
16. Dispute references another tenant's payment
17. Resolution arrives after the order was already refunded
18. Evidence bundle contains cardholder PAN or secrets
19. Final network outcome arrives after internal tracking expired
20. Case resolves but the order or customer record update fails

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled time or provider behavior, and cleanup.
