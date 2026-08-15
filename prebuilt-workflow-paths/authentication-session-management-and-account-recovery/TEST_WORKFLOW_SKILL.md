---
name: test-multi-step-approval
description: Design, implement, or review tests for Multi-step Approval and Rejection. Use when complete normal, invalid, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test Multi-step Approval

Cover:
1. All sequential reviewers approve
2. Parallel stage reaches quorum
3. Authorized reviewer rejects
4. Required request evidence is missing
5. Decision input is malformed
6. Reviewer is no longer eligible
7. Requester attempts self-approval
8. Request changes after approval
9. Approve and reject arrive together
10. Decision arrives at deadline
11. Submission response is lost
12. Recorded decision is replayed
13. Approval actions are automated or flooded
14. Decision commits but notification fails
15. Policy or identity dependency times out
16. Final approval response is lost
17. Cross-tenant reviewer attempts action
18. Sensitive evidence causes an error
19. Late approval follows terminal action
20. Approved request downstream work fails

For each scenario write Given, When, expected response and state or security changes, forbidden outcomes, test level, fixtures, controlled time or dependency behavior, and cleanup.

