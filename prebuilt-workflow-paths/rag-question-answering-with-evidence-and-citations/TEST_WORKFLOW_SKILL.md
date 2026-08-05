---
name: test-rag-cited-answer
description: Design, implement, or review tests for RAG Question Answering with Evidence and Citations. Use when complete normal, invalid, boundary, injection, authorization, replay, provider, recovery, privacy, and misuse scenarios are needed.
---

# Test RAG Question Answering with Evidence

Cover:
1. Authorized question returns cited answer
2. Insufficient evidence causes abstention
3. Conflicting sources remain explicit
4. Question or source scope is missing
5. Question or retrieved content is excessive
6. Candidate source is unauthorized
7. Document contains prompt injection
8. Question normalization changes meaning
9. Index changes during request
10. Freshness boundary is reached
11. Answer response is lost
12. Cached request is replayed
13. RAG queries are flooded
14. Retrieval succeeds but generation fails
15. Retrieval or model provider times out
16. Answer succeeds but response is lost
17. Cross-tenant result enters candidates
18. RAG failure is logged
19. Source permission changes mid-request
20. Citation mapping fails

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled provider or source behavior, and cleanup.

