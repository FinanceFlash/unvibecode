# Engineering Guide

## Trace the implementation
1. Question, conversation, follow-up, feedback, citation-open, regenerate, and support entry points
2. User, account, tenant, role, collection, document, field, and conversation authorization checks
3. Question validation, normalization, query rewrite, filters, embeddings, index selection, and cache key
4. Search, vector, hybrid retrieval, reranking, thresholds, top-k, diversity, and source-version resolution
5. Post-retrieval permission filtering, freshness, deletion, conflict, and evidence sufficiency
6. Prompt assembly, document-instruction isolation, model request, timeout, usage, and uncertain result
7. Claim support, citation mapping, citation verification, abstention, clarification, and output validation
8. Audit, privacy, cost, latency, monitoring, feedback, support tools, and tests

## Rules the code should protect
- Only authorized tenant-scoped evidence may enter the answer context
- Document text must not override protected instructions or permissions
- Material claims must map to accessible supporting evidence
- Citations must identify the exact source version and location used
- Insufficient, conflicting, stale, or unavailable evidence must remain explicit
- Cache and conversation state must respect current user, tenant, permissions, and source versions
- Retry and replay must not expose stale or unauthorized answers
- Questions, evidence, answers, embeddings, personal data, and credentials must remain protected

## Build or change safely
1. Confirm product decisions before relying on model, retrieval, framework, or provider defaults.
2. Follow existing authorization, validation, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, tenant, source or prompt, version, state, and scope.
4. Enforce permission, current-state, schema, evidence, uniqueness, and limit rules before material use.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep invalid output, missing evidence, cost, and downstream inconsistency visible and repairable.
7. Add the core 20 tests.

