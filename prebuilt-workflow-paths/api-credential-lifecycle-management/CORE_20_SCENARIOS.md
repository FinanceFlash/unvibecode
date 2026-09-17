# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Authorized credential creation | An unauthorized or incorrectly scoped credential becomes active |
| 2 | Unauthorized credential creation | A requester without sufficient permission receives an active credential |
| 3 | Invalid scope during creation | A credential becomes active with permissions beyond the approved scope |
| 4 | Credential activation | A credential becomes usable before required authorization and activation checks complete |
| 5 | Duplicate credential creation | A retry creates multiple active credentials for one logical creation request |
| 6 | First successful credential use | A credential belonging to another owner, application, service, or scope is accepted |
| 7 | Expired credential rejection | An expired credential continues to authorize protected API access |
| 8 | Credential nearing expiry | A credential reaches expiry without the expected lifecycle transition or actionable renewal indication |
| 9 | Planned credential rotation | Rotation leaves the system without a valid authorized credential when continuity is required |
| 10 | Controlled temporary overlap during rotation | Temporary overlap becomes indefinite or creates an uncontrolled number of active credentials |
| 11 | Old credential invalidation after rotation | The previous credential remains usable after completed rotation when it should be invalidated |
| 12 | Concurrent rotation attempts | Concurrent operations leave contradictory active credentials or corrupt lifecycle metadata |
| 13 | Credential revocation | The system reports revocation while the credential remains authorized for protected API access |
| 14 | Use after revocation | A revoked credential continues to provide protected API access |
| 15 | Emergency revocation of compromised credential | A known compromised credential remains active because the normal lifecycle process is still pending |
| 16 | Credential-generation dependency failure | A dependency failure leaves a partially provisioned credential incorrectly marked active |
| 17 | Partial rotation failure | A failed rotation is reported as complete when the replacement is unusable or the previous credential was incorrectly invalidated |
| 18 | Retry after incomplete lifecycle operation | A retry creates duplicate credentials or conflicting lifecycle states |
| 19 | Lifecycle change succeeds but audit recording fails | A lifecycle operation silently loses required audit evidence while being presented as fully traceable |
| 20 | Recovery and final-state reconciliation | Recovery leaves contradictory states or marks a credential healthy without verifying its actual state |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).