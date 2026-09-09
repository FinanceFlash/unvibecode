---
name: test-api-credential-lifecycle
description: Design, implement, or review tests for API Credential Lifecycle Management. Use when complete normal, invalid, boundary, authorization, concurrency, expiry, rotation, revocation, dependency, recovery, security, and misuse scenarios are needed.
---

# Test API Credential Lifecycle

Cover:
1. Authorized credential creation
2. Unauthorized credential creation
3. Invalid scope during creation
4. Credential activation
5. Duplicate credential creation
6. First successful credential use
7. Expired credential rejection
8. Credential nearing expiry
9. Planned credential rotation
10. Controlled temporary overlap during rotation
11. Old credential invalidation after rotation
12. Concurrent rotation attempts
13. Credential revocation
14. Use after revocation
15. Emergency revocation of compromised credential
16. Credential-generation dependency failure
17. Partial rotation failure
18. Retry after incomplete lifecycle operation
19. Lifecycle change succeeds but audit recording fails
20. Recovery and final-state reconciliation

For each scenario write Given, When, expected response and authoritative lifecycle state changes, forbidden outcomes, test level, fixtures, controlled dependency behavior, and cleanup.