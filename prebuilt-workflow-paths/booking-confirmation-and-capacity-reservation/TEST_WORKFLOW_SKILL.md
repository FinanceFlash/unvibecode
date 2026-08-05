---
name: test-booking-confirmation
description: Design, implement, or review tests for Booking Confirmation and Capacity Commitment. Use when complete normal, invalid, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test Booking Confirmation and Capacity Commitment

Cover:
1. Active hold confirms one booking
2. Direct booking commits available capacity
3. Provider calendar binds same booking
4. Required booking data is missing
5. Slot or party data is malformed
6. Hold or capacity is no longer valid
7. Actor cannot create booking
8. Timezone crosses calendar boundary
9. Two customers request last capacity
10. Hold converts at expiry boundary
11. Confirmation response is lost
12. Idempotency key is replayed with changed slot
13. Booking attempts are flooded
14. Booking commits but capacity update fails
15. External provider times out
16. Booking commits but response is lost
17. Cross-tenant resource is referenced
18. Booking failure is logged
19. Late provider rejection follows confirmation
20. Confirmation or reminder fails

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled time or dependency behavior, and cleanup.

