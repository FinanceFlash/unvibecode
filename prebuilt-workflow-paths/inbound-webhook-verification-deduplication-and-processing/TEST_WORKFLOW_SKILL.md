---
name: test-inbound-webhook
description: Design, implement, or review tests for Inbound Webhook Verification, Deduplication, and Processing. Use when complete authenticity, scope, duplicate, concurrency, ordering, failure, recovery, abuse, privacy, and operations coverage is needed.
---

# Test Inbound Webhook Processing

Cover:

1. Valid unique delivery is accepted
2. Body is malformed or too large
3. Required verification headers are missing
4. Signature does not match
5. Signature uses the original request body
6. Timestamp is outside the replay window
7. Secret rotation overlaps
8. Provider, endpoint, or tenant is not authorized
9. Event type or schema version is unsupported
10. Duplicate deliveries arrive concurrently
11. A completed delivery is replayed
12. Delivery identity has a different payload
13. Acknowledgement response is lost after durable acceptance
14. Inbox persistence fails before acknowledgement
15. Worker crashes after claim
16. Effect commits but completion recording fails
17. Related events arrive out of order
18. Delivery flood exceeds capacity
19. Sensitive delivery is logged or retained unsafely
20. Poison delivery exhausts retries

For each scenario specify Given, When, expected HTTP response, inbox and authoritative business state, allowed effects, `Must not happen`, test level, fixtures, controlled clock or provider behavior, failure injection, and cleanup. Assert durable state and effect counts, not only response codes or mocks.
