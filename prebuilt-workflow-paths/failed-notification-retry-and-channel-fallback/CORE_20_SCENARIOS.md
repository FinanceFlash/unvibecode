# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Transient failure succeeds on retry | The recipient receives duplicate messages |
| 2 | Eligible fallback channel delivers | Fallback bypasses purpose, preference, consent, or content rules |
| 3 | Permanent failure ends visibly | The system retries forever or hides the missing notice |
| 4 | Retry metadata is missing | An incomplete job sends to a guessed destination |
| 5 | Provider error is malformed or unknown | Unknown input becomes an unlimited retry |
| 6 | Permanent error is selected for retry | A permanent failure consumes more attempts or sends again |
| 7 | Fallback permission is absent | Protected content is sent through an unauthorized channel |
| 8 | Equivalent attempt identities differ | A representation change bypasses attempt uniqueness |
| 9 | Two workers claim one retry | Both workers send before updating state |
| 10 | Attempt occurs at expiry boundary | Queue delay or client time extends message life unpredictably |
| 11 | Retry scheduling response is lost | Duplicate jobs later send duplicate messages |
| 12 | Retry job is replayed | Attempt count and provider sends repeat |
| 13 | Provider outage triggers many retries | A retry storm worsens the outage |
| 14 | Failure records but enqueue fails | The notification remains silently stranded |
| 15 | Retry provider times out | Timeout is treated as failure and immediately duplicated |
| 16 | Delivery succeeds but response is lost | Retry or fallback sends another visible message |
| 17 | Cross-tenant retry job is altered | Job fields redirect a message across tenants |
| 18 | Retry error is logged | Provider secrets or full protected messages are exposed |
| 19 | Late primary callback follows fallback | Status moves backward or both channels continue blindly |
| 20 | Fallback delivers but local status fails | Additional channels send or operations report false failure |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

