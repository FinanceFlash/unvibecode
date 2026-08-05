---
name: test-checkout-payment
description: Design, implement, or review tests for Checkout Payment Authorization and Capture. Use when complete normal, invalid, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test Checkout Payment Authorization and Capture

Cover:
1. Valid checkout is captured once
2. Authorization is captured before expiry
3. Customer authentication resumes payment
4. Required payment input is missing
5. Amount or currency is malformed
6. Provider declines payment
7. Actor cannot pay for order
8. Minor-unit boundary is calculated
9. Two payments arrive together
10. Authorization expires at boundary
11. Payment response is lost
12. Idempotency key is replayed with changed payload
13. Payment attempts are flooded
14. Authorization succeeds but local write fails
15. Provider times out uncertainly
16. Capture succeeds but response is lost
17. Cross-tenant order reference is supplied
18. Payment error is logged
19. Late capture follows cancellation
20. Capture succeeds but order update fails

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled time or provider behavior, and cleanup.

