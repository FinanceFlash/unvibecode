---
name: test-account-data-erasure
description: Design, implement, or review tests for Right-to-erasure and Account-data Deletion. Use when complete normal, invalid, boundary, authorization, replay, provider, recovery, privacy, compliance, and misuse scenarios are needed.
---

# Test Account-data Erasure

Cover:
1. Eligible request completes erasure
2. Lawful hold preserves only required data
3. Anonymization preserves non-personal record
4. Required request data is missing
5. Scope or identifier is malformed
6. Identity verification fails
7. Operator cannot approve or execute
8. Aliases resolve to one account safely
9. Duplicate requests execute together
10. Hold expires at boundary
11. Request response is lost
12. Deletion task is replayed
13. Deletion is abused
14. Restriction commits but jobs fail
15. Processor or datastore times out
16. Deletion commits but response is lost
17. Cross-tenant record is discovered
18. Deletion failure is logged
19. Late data arrives after completion
20. One mandatory system fails

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled dependency behavior, and cleanup.

