---
name: test-idempotent-request
description: Design, implement, or review tests for Idempotent Request Processing and Concurrency Control. Use when complete normal, duplicate, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test Idempotent Request Processing and Concurrency Control

Cover:
1. New request with valid key is processed once
2. Duplicate request returns original stored result
3. Retried request after transient failure replays safely
4. Idempotency key is missing or empty
5. Key format is invalid or exceeds length limit
6. Key is reused with a different payload
7. Key is reused by a different actor or tenant
8. Two requests with the same key arrive simultaneously
9. Lock is acquired for a contested resource
10. Lock holder crashes before releasing
11. Optimistic concurrency check detects a conflict
12. Key-store becomes unavailable during processing
13. Key expires while a legitimate retry is in flight
14. Stored response is evicted before client retries
15. Operation succeeds but response storage fails
16. Downstream effect partially fails after key is bound
17. Lock lease is renewed by a slow operation
18. Concurrent optimistic writes target the same version
19. Request fingerprint contains sensitive data
20. Key garbage collection runs during peak traffic

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled time or concurrency behavior, and cleanup.
