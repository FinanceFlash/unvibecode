---
name: test-provider-onboarding
description: Design, implement, or review tests for Seller or Service-provider Onboarding and Eligibility. Use when complete normal, invalid, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test Seller or Service-provider Onboarding

Cover:
1. Eligible provider becomes active
2. Information request is resubmitted
3. Ineligible application is rejected
4. Required application data is missing
5. Evidence is malformed or unsafe
6. Provider is ineligible
7. Actor cannot change application
8. Duplicate identity is detected
9. Approve and reject arrive together
10. Evidence expires at decision boundary
11. Submission response is lost
12. Verification callback is replayed
13. Applications are flooded or forged
14. Application commits but verification fails
15. Verification provider times out
16. Approval commits but response is lost
17. Cross-tenant application is referenced
18. Sensitive evidence causes an error
19. Stale approval follows withdrawal
20. Approved account provisioning fails

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled time or dependency behavior, and cleanup.

