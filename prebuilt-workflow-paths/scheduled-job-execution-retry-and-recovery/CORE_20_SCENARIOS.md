# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Due job runs once | The occurrence is missed or executed by multiple effective owners |
| 2 | No-work run records truthful outcome | No work is confused with failure or a cursor skips unseen data |
| 3 | Missed occurrence follows catch-up policy | Every missed time floods the system or required work disappears silently |
| 4 | Required job data is missing | The runner guesses a window, tenant, or credential |
| 5 | Schedule or checkpoint is malformed | Malformed values create an unbounded or incorrect run |
| 6 | Paused job does not run | A stale trigger bypasses current job state |
| 7 | Operator cannot trigger or alter job | Knowledge of a job name grants operational control |
| 8 | Timezone and DST are deterministic | A run duplicates or disappears because hosts interpret local time differently |
| 9 | Two schedulers claim one run | Both workers create duplicate business effects |
| 10 | Item lies on window boundary | A boundary record is skipped or processed twice |
| 11 | Claim response is lost | A lost response creates two effective owners |
| 12 | Completed run is replayed | Completed effects and checkpoint advancement repeat |
| 13 | Retries threaten shared capacity | Retries synchronize and amplify the dependency outage |
| 14 | Outputs commit but checkpoint fails | Effects duplicate or the checkpoint advances without evidence |
| 15 | External dependency times out | Timeout is assumed to be a clean failure or success |
| 16 | Checkpoint commits but response is lost | The next window or effects are duplicated |
| 17 | Cross-tenant job data is supplied | A global job key mixes tenant state |
| 18 | Job failure is logged | Secrets or sensitive records appear in logs, alerts, or run consoles |
| 19 | Lease expires while worker continues | The stale worker overwrites the replacement or advances the cursor |
| 20 | Partial batch is recovered | The whole batch is marked successful or one bad item blocks all future runs forever |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

