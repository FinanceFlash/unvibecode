---
name: write-rag-cited-answer-spec
description: Write or review a product specification for RAG Question Answering with Evidence and Citations. Use when defining actors, states, authorization, model or evidence rules, edge cases, acceptance criteria, recovery, or business risks.
---

# Write a RAG Question Answering with Evidence Specification

Use application-native terms. Decide:
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

Write scope, actors, objects, states, paths, user outcomes, permissions, validation, recovery, privacy, misuse, acceptance criteria, and unanswered decisions.

