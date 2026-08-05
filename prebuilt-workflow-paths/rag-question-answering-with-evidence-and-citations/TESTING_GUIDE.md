# Testing Guide

Check authoritative context, permissions, versions, validation, evidence, downstream effects, recovery, and audit—not only displayed answers.

## 1. Authorized question returns cited answer

**Given:** An authorized user asks a clear question with sufficient accessible evidence

**When:** Retrieval and generation run

**Expect:** The answer's material claims map to exact supporting citations

**Must not happen:** Unsupported claims or inaccessible sources appear

**Best test levels:** Integration and end-to-end.

## 2. Insufficient evidence causes abstention

**Given:** Authorized retrieval finds no evidence above the required threshold

**When:** Answering runs

**Expect:** The system abstains, clarifies, or escalates explicitly

**Must not happen:** The model fills the gap with confident invention

**Best test levels:** Integration.

## 3. Conflicting sources remain explicit

**Given:** Two accessible authoritative sources disagree materially

**When:** Synthesis runs

**Expect:** The answer qualifies the conflict or escalates by policy

**Must not happen:** One source is silently selected as truth

**Best test levels:** Integration.

## 4. Question or source scope is missing

**Given:** The request lacks a question, tenant, collection, or required filter

**When:** Validation runs

**Expect:** The request fails before retrieval

**Must not happen:** A default global corpus is queried

**Best test levels:** Unit and API.

## 5. Question or retrieved content is excessive

**Given:** Input, conversation, filters, document count, chunk size, or token budget exceeds limits

**When:** Validation and selection run

**Expect:** The request is bounded or rejected explicitly

**Must not happen:** Resources are exhausted or evidence is truncated invisibly

**Best test levels:** Unit, API, and load.

## 6. Candidate source is unauthorized

**Given:** Search returns a high-scoring document outside current user permission

**When:** Post-retrieval filtering runs

**Expect:** The source is excluded and cannot influence answer or citation

**Must not happen:** Metadata, snippets, or conclusions leak

**Best test levels:** Authorization and security.

## 7. Document contains prompt injection

**Given:** Retrieved text instructs the model to ignore policy, reveal secrets, or use other sources

**When:** Prompt assembly and generation run

**Expect:** The text remains untrusted evidence only

**Must not happen:** Document instructions control system behavior

**Best test levels:** Security and adversarial.

## 8. Question normalization changes meaning

**Given:** The question contains Unicode, abbreviations, locale terms, negation, or ambiguous entity names

**When:** Rewrite and retrieval run

**Expect:** Original intent is preserved or clarification is requested

**Must not happen:** Normalization retrieves evidence for a different question

**Best test levels:** Unit and evaluation.

## 9. Index changes during request

**Given:** The selected index or source snapshot changes while retrieval and generation execute

**When:** The answer completes

**Expect:** One consistent version set is used or the request restarts explicitly

**Must not happen:** Citations mix incompatible source versions

**Best test levels:** Integration.

## 10. Freshness boundary is reached

**Given:** A source expires or becomes superseded immediately before, at, and after the policy boundary

**When:** Evidence selection runs

**Expect:** One explicit freshness rule applies

**Must not happen:** Old content remains authoritative through clock ambiguity

**Best test levels:** Unit with controlled time.

## 11. Answer response is lost

**Given:** The answer may have completed but the client sees no result

**When:** The client retries

**Expect:** A safe version-aware cache or explicit regeneration policy applies

**Must not happen:** Unauthorized or inconsistent cached content is returned

**Best test levels:** API and integration.

## 12. Cached request is replayed

**Given:** A prior question key is reused after user, permission, conversation, or source version changes

**When:** Cache lookup runs

**Expect:** The key includes all authorization and version inputs or misses safely

**Must not happen:** Another user's or stale answer is reused

**Best test levels:** Security and integration.

## 13. RAG queries are flooded

**Given:** One actor sends large, repeated, broad, or adversarial searches

**When:** Quota and abuse controls run

**Expect:** Retrieval, model usage, cost, and concurrency remain bounded

**Must not happen:** One user exhausts index or provider capacity

**Best test levels:** Security and load.

## 14. Retrieval succeeds but generation fails

**Given:** A valid evidence set exists but the model or output validation fails

**When:** Recovery runs

**Expect:** The request fails or retries within policy without losing evidence identity

**Must not happen:** A partial unsupported answer is returned

**Best test levels:** Integration.

## 15. Retrieval or model provider times out

**Given:** Search, embedding, reranking, source, or LLM service returns uncertain status

**When:** Failure handling runs

**Expect:** The outcome remains explicit and retries are bounded

**Must not happen:** Timeout becomes empty evidence and fabricated answer

**Best test levels:** Provider contract and integration.

## 16. Answer succeeds but response is lost

**Given:** The model generated and citations validated while delivery failed

**When:** Retry or cache recovery runs

**Expect:** Only the same authorized versioned answer is reused

**Must not happen:** Regeneration changes claims or reveals stale content silently

**Best test levels:** Integration.

## 17. Cross-tenant result enters candidates

**Given:** A query or cache key can match another tenant's source

**When:** Filtering and answer generation run

**Expect:** Tenant isolation excludes it completely

**Must not happen:** Its text, metadata, score, or conclusion affects the answer

**Best test levels:** Authorization and security.

## 18. RAG failure is logged

**Given:** The path contains questions, documents, answers, embeddings, citations, and credentials

**When:** An error occurs

**Expect:** Diagnostics avoid secrets and unnecessary sensitive content

**Must not happen:** Protected knowledge enters logs or traces

**Best test levels:** Security and log inspection.

## 19. Source permission changes mid-request

**Given:** A selected source is deleted or access is revoked before response

**When:** Final authorization runs

**Expect:** The source is removed, the answer is recomputed, or the request is denied by policy

**Must not happen:** Revoked content is returned or cited

**Best test levels:** Integration.

## 20. Citation mapping fails

**Given:** The answer is plausible but one citation cannot map to the exact source version or support the claim

**When:** Output validation runs

**Expect:** The claim is removed, qualified, repaired, or the answer is rejected

**Must not happen:** A fabricated or broken citation reaches the user

**Best test levels:** Integration and evaluation.

