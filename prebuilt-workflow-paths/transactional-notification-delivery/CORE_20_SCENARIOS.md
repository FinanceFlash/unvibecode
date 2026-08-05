# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Valid event sends one message | The event sends to another recipient or creates duplicate messages |
| 2 | Correct template and locale render | Fallback text, another locale, or another customer's data appears unexpectedly |
| 3 | Provider status is recorded | Accepted is falsely treated as delivered or status moves backward |
| 4 | Recipient or template data is missing | Blank or incomplete content is sent |
| 5 | Payload or destination is malformed | Malformed data reaches the provider, renderer, or logs unsafely |
| 6 | Channel is suppressed or ineligible | Purpose or preference rules are silently bypassed |
| 7 | Recipient resolves outside tenant | An identifier alone redirects protected content |
| 8 | Equivalent destinations or event keys differ | Formatting bypasses deduplication or destination policy |
| 9 | Duplicate events arrive together | Both workers send before detecting duplication |
| 10 | Send occurs at expiry or quiet-hours boundary | Client clocks or races change eligibility unpredictably |
| 11 | Notification request response is lost | Retries multiply messages or provider attempts |
| 12 | Business event is replayed | Recipient-visible content and audit effects repeat |
| 13 | Notification trigger is flooded | Unbounded messages, cost, or harassment occurs |
| 14 | Message commits but provider call fails | The system reports delivery or loses the notification silently |
| 15 | Provider times out with uncertain outcome | Blind retry sends duplicates or uncertainty becomes success |
| 16 | Provider accepts but response is lost | A second recipient-visible message is sent |
| 17 | Template variable contains unauthorized data | Cross-customer or excessive data is delivered |
| 18 | Delivery failure is logged | Secrets or full protected messages are exposed |
| 19 | Late callback follows failure handoff | A stale callback moves state backward or ignores an already delivered result |
| 20 | Provider succeeds but local status fails | The application loses evidence or resends the message |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

