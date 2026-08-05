# RAG Question Answering with Evidence and Citations

Starts when an authorized user asks a question against approved knowledge sources. Ends when the system returns a grounded answer with traceable citations, explicitly abstains, requests clarification, escalates, or fails without leaking inaccessible source content.

| Task | File |
|---|---|
| Product and business | [PRODUCT_AND_BUSINESS_GUIDE.md](PRODUCT_AND_BUSINESS_GUIDE.md) |
| Engineering | [ENGINEERING_GUIDE.md](ENGINEERING_GUIDE.md) |
| Testing | [TESTING_GUIDE.md](TESTING_GUIDE.md) |
| Core 20 | [CORE_20_SCENARIOS.md](CORE_20_SCENARIOS.md) |
| Paths and edge cases | [PATHS_AND_EDGE_CASES.md](PATHS_AND_EDGE_CASES.md) |
| Permissions and misuse | [PERMISSION_AND_ABUSE_GUIDE.md](PERMISSION_AND_ABUSE_GUIDE.md) |
| Retry and recovery | [RETRY_AND_RECOVERY_GUIDE.md](RETRY_AND_RECOVERY_GUIDE.md) |

## Included
- question validation, source and tenant authorization, query transformation, retrieval, ranking, and snapshot selection
- document-injection defense, evidence sufficiency, answer generation, claim support, citation mapping, and abstention
- freshness, conflicting sources, source version, cache, feedback, audit, privacy, retry, and recovery
- cost, latency, cross-tenant retrieval, deleted source, permission change, and provider failure

## Excluded
- general LLM content generation without evidence grounding
- document import, extraction, and indexing lifecycle
- search product user interface as a standalone workflow
- model training and evaluation

The five `*_SKILL.md` files are self-contained.

