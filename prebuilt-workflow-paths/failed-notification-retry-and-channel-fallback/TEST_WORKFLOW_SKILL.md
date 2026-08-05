---
name: test-notification-retry-fallback
description: Design, implement, or review tests for Failed Notification Retry and Channel Fallback. Use when complete normal, invalid, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test Notification Retry and Channel Fallback

Cover:
1. Transient failure succeeds on retry
2. Eligible fallback channel delivers
3. Permanent failure ends visibly
4. Retry metadata is missing
5. Provider error is malformed or unknown
6. Permanent error is selected for retry
7. Fallback permission is absent
8. Equivalent attempt identities differ
9. Two workers claim one retry
10. Attempt occurs at expiry boundary
11. Retry scheduling response is lost
12. Retry job is replayed
13. Provider outage triggers many retries
14. Failure records but enqueue fails
15. Retry provider times out
16. Delivery succeeds but response is lost
17. Cross-tenant retry job is altered
18. Retry error is logged
19. Late primary callback follows fallback
20. Fallback delivers but local status fails

For each scenario write Given, When, expected response and state or security changes, forbidden outcomes, test level, fixtures, controlled time or dependency behavior, and cleanup.

