# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Authorized question returns cited answer | Unsupported claims or inaccessible sources appear |
| 2 | Insufficient evidence causes abstention | The model fills the gap with confident invention |
| 3 | Conflicting sources remain explicit | One source is silently selected as truth |
| 4 | Question or source scope is missing | A default global corpus is queried |
| 5 | Question or retrieved content is excessive | Resources are exhausted or evidence is truncated invisibly |
| 6 | Candidate source is unauthorized | Metadata, snippets, or conclusions leak |
| 7 | Document contains prompt injection | Document instructions control system behavior |
| 8 | Question normalization changes meaning | Normalization retrieves evidence for a different question |
| 9 | Index changes during request | Citations mix incompatible source versions |
| 10 | Freshness boundary is reached | Old content remains authoritative through clock ambiguity |
| 11 | Answer response is lost | Unauthorized or inconsistent cached content is returned |
| 12 | Cached request is replayed | Another user's or stale answer is reused |
| 13 | RAG queries are flooded | One user exhausts index or provider capacity |
| 14 | Retrieval succeeds but generation fails | A partial unsupported answer is returned |
| 15 | Retrieval or model provider times out | Timeout becomes empty evidence and fabricated answer |
| 16 | Answer succeeds but response is lost | Regeneration changes claims or reveals stale content silently |
| 17 | Cross-tenant result enters candidates | Its text, metadata, score, or conclusion affects the answer |
| 18 | RAG failure is logged | Protected knowledge enters logs or traces |
| 19 | Source permission changes mid-request | Revoked content is returned or cited |
| 20 | Citation mapping fails | A fabricated or broken citation reaches the user |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).

