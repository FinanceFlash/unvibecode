---
name: test-subscription-renewal-cancellation
description: Design, implement, or review tests for Subscription Renewal, Cancellation, and Entitlement Release. Use when complete normal, invalid, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test Subscription Renewal and Cancellation

Cover:
1. Due subscription renews once
2. Period-end cancellation releases on time
3. Immediate cancellation follows policy
4. Required subscription data is missing
5. Period or price is malformed
6. Subscription is ineligible
7. Actor cannot manage subscription
8. Billing boundary handles calendar rules
9. Renewal and cancellation race
10. Payment completes at grace boundary
11. Cancellation response is lost
12. Renewal job is replayed
13. Renewal or cancellation is flooded
14. Payment succeeds but period update fails
15. Provider times out during renewal
16. Renewal commits but response is lost
17. Cross-tenant subscription is referenced
18. Billing failure is logged
19. Late payment follows termination
20. Entitlement release fails

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled time or provider behavior, and cleanup.

