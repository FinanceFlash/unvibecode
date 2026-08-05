---
name: test-support-ticket
description: Design, implement, or review tests for Customer Support Ticket Lifecycle. Use when complete normal, invalid, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test Support Ticket Lifecycle

Cover:
1. Valid issue creates one ticket
2. Ticket is acknowledged and assigned
3. Agent resolves and closes correctly
4. Required intake data is missing
5. Attachment is malformed or unsafe
6. Duplicate issue is submitted
7. Unauthorized person accesses ticket
8. Requester identity formats differ
9. Two agents update ownership together
10. SLA action occurs at deadline
11. Ticket-create response is lost
12. Inbound message is replayed
13. Support intake is flooded
14. Ticket commits but acknowledgement fails
15. External support provider times out
16. Resolution response is lost
17. Cross-tenant ticket reference is used
18. Sensitive message or attachment causes error
19. Customer replies after closure
20. Promised linked action fails

For each scenario write Given, When, expected response and state or security changes, forbidden outcomes, test level, fixtures, controlled time or dependency behavior, and cleanup.

