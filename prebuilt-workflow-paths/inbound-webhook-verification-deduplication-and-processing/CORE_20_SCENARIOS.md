# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Valid unique delivery is accepted | An authentic delivery is rejected or processed before it is durably owned |
| 2 | Body is malformed or too large | Parser work or unbounded resource use begins from invalid input |
| 3 | Required verification headers are missing | The endpoint accepts an unauthenticated request by falling back to defaults |
| 4 | Signature does not match | A forged or tampered payload reaches the inbox or business effect |
| 5 | Signature uses the original request body | Re-encoding or parsing changes the bytes being authenticated |
| 6 | Timestamp is outside the replay window | An old captured request is accepted as a new delivery |
| 7 | Secret rotation overlaps | A valid delivery fails during planned key rotation or an expired secret remains trusted forever |
| 8 | Provider, endpoint, or tenant is not authorized | One provider, environment, or tenant can address another scope |
| 9 | Event type or schema version is unsupported | Unknown data is silently treated as a known command |
| 10 | Duplicate deliveries arrive concurrently | Two workers apply the same business effect |
| 11 | A completed delivery is replayed | A completed effect is charged, granted, sent, or recorded again |
| 12 | Delivery identity has a different payload | A provider or routing conflict overwrites the first payload silently |
| 13 | Acknowledgement response is lost after durable acceptance | The retry creates a second durable delivery or effect |
| 14 | Inbox persistence fails before acknowledgement | The endpoint tells the provider to stop retrying work it never owned |
| 15 | Worker crashes after claim | A lease holder blocks recovery or a replacement duplicates work |
| 16 | Effect commits but completion recording fails | Recovery repeats an uncertain external effect without reconciliation |
| 17 | Related events arrive out of order | A stale event reverses a newer authoritative state |
| 18 | Delivery flood exceeds capacity | Retries or accepted traffic exhaust workers, queues, storage, or provider quota |
| 19 | Sensitive delivery is logged or retained unsafely | Secrets or personal data become visible beyond the approved audience or period |
| 20 | Poison delivery exhausts retries | The system loops forever, hides the failure, or redrives without authorization |

Full Given/When/Expect guidance is in [TESTING_GUIDE.md](TESTING_GUIDE.md).
