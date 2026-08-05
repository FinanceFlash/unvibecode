# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Incremental sync advances safely | A record is skipped or applied repeatedly |
| 2 | No-change run is a no-op | Checkpoint or records mutate without source change |
| 3 | Authorized deletion propagates | Another record is removed or history disappears unexpectedly |
| 4 | Sync definition is incomplete | A default global scope is used |
| 5 | Source record is malformed | Malformed data corrupts the destination |
| 6 | Connection lacks permission | Broader fallback credentials are used |
| 7 | Stale source record conflicts | Newer data is overwritten silently |
| 8 | Identity and values normalize consistently | Variants create duplicates or change meaning |
| 9 | Two sync runs overlap | Runs duplicate records or move checkpoint inconsistently |
| 10 | Change occurs at checkpoint boundary | A boundary record is skipped permanently |
| 11 | Page response is lost | Records duplicate or checkpoint skips ahead |
| 12 | Batch or run is replayed | Business effects repeat |
| 13 | Sync scope is excessive | A sync monopolizes systems or loops forever |
| 14 | Records apply but checkpoint fails | Replay duplicates effects or operators advance manually past failures |
| 15 | External provider times out | Uncertainty becomes success or blind duplicate write |
| 16 | Checkpoint commits but response is lost | A second run overwrites or duplicates data |
| 17 | Cross-tenant connection is referenced | Identifiers or caches mix customer data |
| 18 | Sync failure is logged | Tokens or protected records reach logs |
| 19 | Delete arrives after newer update | Current data is deleted |
| 20 | Partial batch fails | Run reports complete or skips failed work |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

