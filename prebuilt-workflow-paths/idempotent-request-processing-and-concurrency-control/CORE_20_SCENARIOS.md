# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | New request with valid key is processed once | The effect is applied more than once or the key is left unbound |
| 2 | Duplicate request returns original stored result | The operation re-executes or returns a different result |
| 3 | Retried request after transient failure replays safely | Retry creates a second effect or loses the original outcome |
| 4 | Idempotency key is missing or empty | The request proceeds without idempotency protection |
| 5 | Key format is invalid or exceeds length limit | A malformed key is silently accepted and stored |
| 6 | Key is reused with a different payload | The changed payload executes under the original key |
| 7 | Key is reused by a different actor or tenant | A foreign key controls another actor's operation |
| 8 | Two requests with the same key arrive simultaneously | Both execute the effect before duplicate detection completes |
| 9 | Lock is acquired for a contested resource | A second requester proceeds without waiting or is silently ignored |
| 10 | Lock holder crashes before releasing | The lock remains held indefinitely and blocks all subsequent requests |
| 11 | Optimistic concurrency check detects a conflict | The stale write overwrites the concurrent update and loses data |
| 12 | Key-store becomes unavailable during processing | All state-mutating requests fail catastrophically without degradation |
| 13 | Key expires while a legitimate retry is in flight | Expiry permits silent re-execution of the completed operation |
| 14 | Stored response is evicted before client retries | Retry creates a second effect because the original proof is lost |
| 15 | Operation succeeds but response storage fails | The client retries, finds no stored result, and the effect doubles |
| 16 | Downstream effect partially fails after key is bound | Partial state persists with the key marked as completed |
| 17 | Lock lease is renewed by a slow operation | Lease renewal extends beyond the maximum permitted hold time |
| 18 | Concurrent optimistic writes target the same version | Both writes succeed, producing a lost update or inconsistent state |
| 19 | Request fingerprint contains sensitive data | Personal data, credentials, or secrets persist in fingerprint storage |
| 20 | Key garbage collection runs during peak traffic | Collection latency or lock contention degrades live request processing |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).
