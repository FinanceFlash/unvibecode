---
name: test-external-sync
description: Design, implement, or review tests for External-system Synchronization and Checkpointing. Use when complete normal, invalid, boundary, authorization, replay, ordering, provider, recovery, privacy, and misuse scenarios are needed.
---

# Test External-system Synchronization and Checkpointing

Cover:
1. Incremental sync advances safely
2. No-change run is a no-op
3. Authorized deletion propagates
4. Sync definition is incomplete
5. Source record is malformed
6. Connection lacks permission
7. Stale source record conflicts
8. Identity and values normalize consistently
9. Two sync runs overlap
10. Change occurs at checkpoint boundary
11. Page response is lost
12. Batch or run is replayed
13. Sync scope is excessive
14. Records apply but checkpoint fails
15. External provider times out
16. Checkpoint commits but response is lost
17. Cross-tenant connection is referenced
18. Sync failure is logged
19. Delete arrives after newer update
20. Partial batch fails

For each scenario write Given, When, expected response and authoritative state changes, forbidden outcomes, test level, fixtures, controlled provider behavior, and cleanup.

