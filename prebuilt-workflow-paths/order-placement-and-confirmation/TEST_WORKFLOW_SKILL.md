---
name: test-order-placement
description: Design, implement, or review tests for Order Placement and Confirmation. Use when complete normal, invalid, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test Order Placement and Confirmation

Cover:
1. Valid checkout creates one order
2. Order preserves accepted snapshot
3. Downstream references bind same order
4. Required checkout data is missing
5. Checkout value is malformed
6. Quote or hold is stale
7. Actor cannot place order
8. Totals reach rounding boundary
9. Two submissions arrive together
10. Hold expires during commit
11. Placement response is lost
12. Key is replayed with changed checkout
13. Order creation is flooded
14. Order commits but payment handoff fails
15. Dependency times out
16. Order commits but response is lost
17. Cross-tenant checkout is referenced
18. Order failure is logged
19. Late prerequisite follows rejection
20. Confirmation or fulfilment fails

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled time or dependency behavior, and cleanup.

