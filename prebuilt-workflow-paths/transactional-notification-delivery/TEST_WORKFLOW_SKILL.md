---
name: test-transactional-notification-delivery
description: Design, implement, or review tests for Transactional Email, SMS, Push, or In-app Delivery. Use when complete normal, invalid, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test Transactional Notification Delivery

Cover:
1. Valid event sends one message
2. Correct template and locale render
3. Provider status is recorded
4. Recipient or template data is missing
5. Payload or destination is malformed
6. Channel is suppressed or ineligible
7. Recipient resolves outside tenant
8. Equivalent destinations or event keys differ
9. Duplicate events arrive together
10. Send occurs at expiry or quiet-hours boundary
11. Notification request response is lost
12. Business event is replayed
13. Notification trigger is flooded
14. Message commits but provider call fails
15. Provider times out with uncertain outcome
16. Provider accepts but response is lost
17. Template variable contains unauthorized data
18. Delivery failure is logged
19. Late callback follows failure handoff
20. Provider succeeds but local status fails

For each scenario write Given, When, expected response and state or security changes, forbidden outcomes, test level, fixtures, controlled time or dependency behavior, and cleanup.

