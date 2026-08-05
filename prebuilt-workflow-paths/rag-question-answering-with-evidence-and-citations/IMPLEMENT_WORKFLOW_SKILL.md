---
name: implement-rag-cited-answer
description: Implement or modify RAG Question Answering with Evidence and Citations. Use when adding or changing authorization, prompt or retrieval logic, validation, provider calls, output handling, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement RAG Question Answering with Evidence

Confirm:
- Who may query which tenants, collections, documents, fields, and source versions
- Conversation-memory and previous-answer authorization boundaries
- Query rewriting, filters, hybrid retrieval, reranking, top-k, threshold, and diversity policy
- Freshness, index version, source deletion, and permission-change policy
- How untrusted document instructions are isolated from system instructions
- Evidence sufficiency, conflict, confidence, clarification, abstention, and escalation rules
- Claim-to-source support and citation format requirements
- Model, prompt, context-window, token, latency, cost, and provider policy
- Cache key and whether results may be reused across users or permission changes
- Feedback, retention, logging, privacy, abuse, monitoring, and human-review policy

Follow project conventions and protect:
- Only authorized tenant-scoped evidence may enter the answer context
- Document text must not override protected instructions or permissions
- Material claims must map to accessible supporting evidence
- Citations must identify the exact source version and location used
- Insufficient, conflicting, stale, or unavailable evidence must remain explicit
- Cache and conversation state must respect current user, tenant, permissions, and source versions
- Retry and replay must not expose stale or unauthorized answers
- Questions, evidence, answers, embeddings, personal data, and credentials must remain protected

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

