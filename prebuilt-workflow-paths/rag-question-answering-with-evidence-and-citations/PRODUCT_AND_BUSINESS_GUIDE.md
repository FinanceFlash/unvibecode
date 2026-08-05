# Product and Business Guide

## Boundary
Starts when an authorized user asks a question against approved knowledge sources. Ends when the system returns a grounded answer with traceable citations, explicitly abstains, requests clarification, escalates, or fails without leaking inaccessible source content.

## People and systems
- Authorized questioner
- RAG orchestration service
- Source authorization and policy service
- Search, vector, keyword, or hybrid retrieval service
- Document store and source owner
- LLM and reranking providers
- Support, knowledge, security, privacy, and operations teams

## Things created or changed
- Question, conversation context, filters, and request identity
- User, account, tenant, role, and authorized source scope
- Retrieval query, embedding, index version, and search parameters
- Candidate chunk, score, source document, source version, location, and permission
- Selected evidence set and token budget
- Answer, claim, citation, abstention, confidence signal, and feedback
- Usage, cost, cache, audit, and diagnostic record

## Stages
- Question: received → validated → authorized → retrieving → answering → completed, abstained, clarified, escalated, failed, or uncertain
- Evidence: absent → retrieved → filtered → selected, insufficient, conflicting, or stale
- Answer: absent → draft → supported, unsupported, blocked, or rejected
- Citation: candidate → mapped → verified or invalid

## Product decisions
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

## Happy paths
- An authorized question returns an answer supported by precise accessible citations
- Insufficient evidence produces a clear abstention or clarification request
- Conflicting authoritative sources are represented or escalated instead of silently resolved

## Negative paths
- Question, source scope, index, or required context is missing or invalid
- The requester cannot access one or more candidate sources
- Retrieved documents contain instructions that attempt to control the model
- Evidence is insufficient, stale, deleted, conflicting, or cannot support the answer

## Edge cases
- Index or source changes during retrieval and generation
- Permission is revoked after retrieval but before response
- Question reaches token, latency, top-k, or source-size boundary
- Provider succeeds but the response is lost
- Citation target changes, moves, or becomes unavailable

## Acceptance criteria
1. Only authorized tenant-scoped sources may be retrieved, selected, quoted, or cited
2. Document content must be treated as evidence, not trusted system instruction
3. Every material answer claim must be supported by selected accessible evidence or clearly qualified
4. Citations must map to the exact source, version, and location used
5. Insufficient or conflicting evidence must trigger explicit abstention, qualification, clarification, or escalation
6. Deleted, stale, or newly restricted sources must follow explicit snapshot and response policy
7. Conversation memory and cache must not cross user, tenant, permission, or source-version boundaries
8. Repeated or lost-response execution must not expose stale or unauthorized cached answers
9. Queries, documents, answers, embeddings, provider credentials, and personal data must remain protected
10. Retrieval, ranking, evidence, prompt, answer, citation, latency, usage, and cost must remain auditable

## Business risks
| Risk | Business consequence |
|---|---|
| Unauthorized source disclosure | Retrieval or citations reveal content outside the requester's permissions |
| Unsupported answer | The model states a conclusion not established by selected evidence |
| Fabricated or wrong citation | A citation points to a source that does not support the claim |
| Document prompt injection | Source text manipulates instructions, data access, or answer behavior |
| Cross-tenant contamination | Index, cache, conversation, or filters mix customer knowledge |
| Stale answer | Deleted, superseded, or restricted sources remain authoritative |
| False confidence | Insufficient or conflicting evidence is presented without qualification |
| Sensitive-data exposure | Queries, documents, answers, embeddings, or credentials reach unsafe logs |

