---
name: test-inventory-reservation
description: Design, implement, or review tests for Inventory Reservation, Release, and Expiry. Use when complete normal, invalid, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test Inventory Reservation, Release, and Expiry

Cover:
1. Available quantity is reserved once
2. Reservation converts once
3. Cancellation releases quantity
4. Required reservation data is missing
5. Quantity is invalid
6. Inventory is insufficient
7. Actor cannot control reservation
8. Equivalent item or unit representations differ
9. Two customers request last unit
10. Conversion occurs at expiry
11. Reservation response is lost
12. Reservation operation is replayed
13. Scarce inventory is hoarded
14. Reservation commits but expiry job fails
15. Inventory dependency times out
16. Conversion commits but response is lost
17. Cross-tenant reservation is referenced
18. Inventory error is logged
19. Late expiry follows conversion
20. Multi-line reservation partially fails

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled time or dependency behavior, and cleanup.

