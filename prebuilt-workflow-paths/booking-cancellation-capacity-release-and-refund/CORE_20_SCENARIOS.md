# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Eligible cancellation releases capacity | The booking stays active or too much capacity is released |
| 2 | Refund request is created once | Refund requests duplicate or use another payment |
| 3 | Waitlist and notifications follow cancellation | Promotion occurs without capacity or messages contradict booking state |
| 4 | Required cancellation data is missing | An unowned cancellation enters operations |
| 5 | Cancellation input is malformed | Malformed data reaches refund, provider, waitlist, or logs |
| 6 | Booking is outside policy | A stale request releases completed capacity |
| 7 | Actor cannot cancel booking | A booking identifier grants destructive control |
| 8 | Cancellation policy crosses timezone | The customer is charged or denied by inconsistent clocks |
| 9 | Cancel races with check-in or reschedule | Capacity is both consumed and released |
| 10 | Request arrives at cut-off | Latency or client time changes the outcome unpredictably |
| 11 | Cancellation response is lost | Capacity, refund, or notification repeats |
| 12 | Cancellation operation is replayed | Booking and financial effects run again |
| 13 | Cancellation is abused | Capacity gaming, refund abuse, or message cost grows unchecked |
| 14 | Cancellation commits but release fails | Inventory is stranded silently |
| 15 | Provider cancellation times out | Uncertainty becomes false success or repeated provider cancellation |
| 16 | Cancellation commits but response is lost | Downstream effects duplicate |
| 17 | Cross-tenant booking is referenced | Identifiers cross customer or provider boundaries |
| 18 | Cancellation error is logged | Protected cancellation details enter unsafe logs |
| 19 | Late provider completion follows cancellation | The booking becomes both cancelled and completed without review |
| 20 | Refund handoff fails | Customer money or communication remains silently wrong |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

