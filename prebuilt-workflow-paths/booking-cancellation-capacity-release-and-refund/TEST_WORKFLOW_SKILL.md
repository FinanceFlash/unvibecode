---
name: test-booking-cancellation
description: Design, implement, or review tests for Booking Cancellation, Capacity Release, and Refund Request. Use when complete normal, invalid, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test Booking Cancellation and Capacity Release

Cover:
1. Eligible cancellation releases capacity
2. Refund request is created once
3. Waitlist and notifications follow cancellation
4. Required cancellation data is missing
5. Cancellation input is malformed
6. Booking is outside policy
7. Actor cannot cancel booking
8. Cancellation policy crosses timezone
9. Cancel races with check-in or reschedule
10. Request arrives at cut-off
11. Cancellation response is lost
12. Cancellation operation is replayed
13. Cancellation is abused
14. Cancellation commits but release fails
15. Provider cancellation times out
16. Cancellation commits but response is lost
17. Cross-tenant booking is referenced
18. Cancellation error is logged
19. Late provider completion follows cancellation
20. Refund handoff fails

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled time or dependency behavior, and cleanup.

