# Retry and Recovery Guide

## Partial failures
- Retrieval succeeds but answer generation fails
- Answer generates but citation mapping or verification fails
- Some sources become unauthorized after retrieval
- Answer validates but response, cache, or feedback record fails
- Index lookup succeeds but source content is unavailable
- Provider returns output but usage or audit recording fails

## Recovery rules
- Keep user, tenant, permissions, collection, index, source versions, prompt, and model bound throughout the request.
- Recheck source permission before returning evidence or citations.
- Do not return an answer when citation or evidence validation fails under required policy.
- Invalidate cached answers when permission, source, index, or policy inputs change.
- Reconcile answer, citations, source access, cache, usage, cost, and audit state.

