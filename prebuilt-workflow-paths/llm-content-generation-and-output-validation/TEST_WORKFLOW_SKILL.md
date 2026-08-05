---
name: test-llm-structured-generation
description: Design, implement, or review tests for LLM Content Generation and Structured-output Validation. Use when complete normal, invalid, boundary, injection, authorization, replay, provider, recovery, privacy, and misuse scenarios are needed.
---

# Test LLM Structured Content Generation

Cover:
1. Valid request returns schema-valid output
2. Allowed content passes safety validation
3. Malformed output is repaired within limit
4. Required input or schema is missing
5. Input or response is malformed or excessive
6. Requester lacks context permission
7. Prompt injection attempts override policy
8. Unicode and locale reach boundary
9. Equivalent requests run concurrently
10. Token or timeout boundary is reached
11. Generation response is lost
12. Completed request is replayed
13. Generation is flooded
14. Output validates but persistence fails
15. Provider times out uncertainly
16. Provider succeeds but response is lost
17. Cross-tenant context is referenced
18. Generation error is logged
19. Version changes during retry
20. Downstream consumer rejects accepted output

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled provider or source behavior, and cleanup.

