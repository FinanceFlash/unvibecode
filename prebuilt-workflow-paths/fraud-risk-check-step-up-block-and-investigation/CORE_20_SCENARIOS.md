# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Low-risk action is allowed | Another action or stale score is allowed |
| 2 | Step-up passes and resumes action | Proof authorizes another action or bypasses rescoring policy |
| 3 | High-risk action is blocked and cased | The action proceeds or cases duplicate |
| 4 | Required risk data is missing | Missing data silently becomes low risk |
| 5 | Signal or feature is malformed | Bad values distort score or crash evaluation |
| 6 | Signals or model are stale | Stale risk state authorizes current action |
| 7 | Reviewer cannot override | A case identifier grants privileged control |
| 8 | Identity and device formats differ | Formatting fragments risk history or crosses accounts |
| 9 | Duplicate decisions run together | One allows while another blocks or cases duplicate |
| 10 | Score reaches threshold boundary | Floating-point or service differences change outcomes |
| 11 | Decision response is lost | Controls or business action duplicate |
| 12 | Risk event is replayed | Replay bypasses a block or repeats the transaction |
| 13 | Fraud endpoint is probed or flooded | Thresholds are learned or service capacity is exhausted |
| 14 | Decision commits but challenge fails | The action proceeds without proof |
| 15 | Model or feature service times out | Timeout silently becomes allow |
| 16 | Block commits but response is lost | Duplicate cases or contradictory allow occurs |
| 17 | Cross-tenant signals are supplied | Another customer's behavior affects decision |
| 18 | Fraud failure is logged | Personal data or threshold logic leaks |
| 19 | Late challenge follows terminal decision | Stale proof revives an action |
| 20 | Decision and enforcement disagree | System reports protection while fraud proceeds |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

