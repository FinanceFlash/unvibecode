---
name: test-fraud-risk-decision
description: Design, implement, or review tests for Fraud-risk Scoring, Step-up, Block, and Case Creation. Use when complete normal, invalid, boundary, concurrency, replay, failure, recovery, permission, privacy, and misuse scenarios are needed.
---

# Test Fraud-risk Decision and Step-up

Cover:
1. Low-risk action is allowed
2. Step-up passes and resumes action
3. High-risk action is blocked and cased
4. Required risk data is missing
5. Signal or feature is malformed
6. Signals or model are stale
7. Reviewer cannot override
8. Identity and device formats differ
9. Duplicate decisions run together
10. Score reaches threshold boundary
11. Decision response is lost
12. Risk event is replayed
13. Fraud endpoint is probed or flooded
14. Decision commits but challenge fails
15. Model or feature service times out
16. Block commits but response is lost
17. Cross-tenant signals are supplied
18. Fraud failure is logged
19. Late challenge follows terminal decision
20. Decision and enforcement disagree

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled time or dependency behaviour, and cleanup.

