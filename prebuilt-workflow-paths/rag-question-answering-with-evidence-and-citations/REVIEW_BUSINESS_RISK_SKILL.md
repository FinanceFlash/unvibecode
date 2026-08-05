---
name: review-rag-cited-answer-risk
description: Review customer, accuracy, privacy, cost, and operational risks in RAG Question Answering with Evidence and Citations. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review RAG Question Answering with Evidence Risk

Review entry, authorization, prompt or source, versions, validation or evidence, provider behavior, retry, recovery, privacy, cost, and downstream paths. Prioritize:
- Unauthorized source disclosure — Retrieval or citations reveal content outside the requester's permissions
- Unsupported answer — The model states a conclusion not established by selected evidence
- Fabricated or wrong citation — A citation points to a source that does not support the claim
- Document prompt injection — Source text manipulates instructions, data access, or answer behavior
- Cross-tenant contamination — Index, cache, conversation, or filters mix customer knowledge
- Stale answer — Deleted, superseded, or restricted sources remain authoritative
- False confidence — Insufficient or conflicting evidence is presented without qualification
- Sensitive-data exposure — Queries, documents, answers, embeddings, or credentials reach unsafe logs

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition.

