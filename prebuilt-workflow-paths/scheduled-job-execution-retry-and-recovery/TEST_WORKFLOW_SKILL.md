---
name: test-scheduled-job-recovery
description: Design, implement, or review tests for Scheduled Job Execution, Checkpoint, Retry, and Recovery. Use when complete normal, invalid, boundary, authorization, replay, dependency, concurrency, recovery, privacy, and misuse scenarios are needed.
---

# Test Scheduled Job Execution and Recovery

Cover:
1. Due job runs once
2. No-work run records truthful outcome
3. Missed occurrence follows catch-up policy
4. Required job data is missing
5. Schedule or checkpoint is malformed
6. Paused job does not run
7. Operator cannot trigger or alter job
8. Timezone and DST are deterministic
9. Two schedulers claim one run
10. Item lies on window boundary
11. Claim response is lost
12. Completed run is replayed
13. Retries threaten shared capacity
14. Outputs commit but checkpoint fails
15. External dependency times out
16. Checkpoint commits but response is lost
17. Cross-tenant job data is supplied
18. Job failure is logged
19. Lease expires while worker continues
20. Partial batch is recovered

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled time and dependency behavior, and cleanup.

