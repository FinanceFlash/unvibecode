# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Valid request returns schema-valid output | Raw or invalid model text reaches the consumer |
| 2 | Allowed content passes safety validation | A safe answer is blocked silently or unsafe content bypasses checks |
| 3 | Malformed output is repaired within limit | Repairs loop indefinitely or change the requested meaning |
| 4 | Required input or schema is missing | The model is called with guessed policy or shape |
| 5 | Input or response is malformed or excessive | Resource limits, parsers, or logs are abused |
| 6 | Requester lacks context permission | Generation leaks inaccessible information |
| 7 | Prompt injection attempts override policy | Untrusted text changes system authority |
| 8 | Unicode and locale reach boundary | Hidden or equivalent text bypasses rules or schema checks |
| 9 | Equivalent requests run concurrently | Downstream effects or billing duplicate unexpectedly |
| 10 | Token or timeout boundary is reached | Partial output is reported as complete |
| 11 | Generation response is lost | Costs and downstream effects multiply silently |
| 12 | Completed request is replayed | Replay bypasses policy version or duplicates effects |
| 13 | Generation is flooded | One user exhausts budget or service capacity |
| 14 | Output validates but persistence fails | The service reports success while no usable artifact exists |
| 15 | Provider times out uncertainly | Timeout becomes accepted content or endless retry |
| 16 | Provider succeeds but response is lost | Unvalidated or duplicate output reaches downstream effects |
| 17 | Cross-tenant context is referenced | Identifiers or cache keys cross the data boundary |
| 18 | Generation error is logged | Raw protected prompts or credentials reach logs |
| 19 | Version changes during retry | One logical request mixes incompatible versions |
| 20 | Downstream consumer rejects accepted output | The product reports success or repeatedly triggers material effects |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

