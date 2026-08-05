# Permission and Abuse Guide

## Permission boundaries
- Only authorized tenant-scoped evidence may enter the answer context
- Document text must not override protected instructions or permissions
- Material claims must map to accessible supporting evidence
- Citations must identify the exact source version and location used
- Insufficient, conflicting, stale, or unavailable evidence must remain explicit

## Misuse paths
- Unauthorized source disclosure — Retrieval or citations reveal content outside the requester's permissions
- Unsupported answer — The model states a conclusion not established by selected evidence
- Fabricated or wrong citation — A citation points to a source that does not support the claim
- Document prompt injection — Source text manipulates instructions, data access, or answer behavior
- Cross-tenant contamination — Index, cache, conversation, or filters mix customer knowledge
- Stale answer — Deleted, superseded, or restricted sources remain authoritative
- False confidence — Insufficient or conflicting evidence is presented without qualification
- Sensitive-data exposure — Queries, documents, answers, embeddings, or credentials reach unsafe logs

Protect actor identity, tenant scope, prompts, sources, outputs, provider credentials, support tools, and audit records. Deny uncertain ownership, evidence, or permission.

