# Engineering Guide

## Trace the implementation
1. Generation, preview, regenerate, validate, repair, cache, and support entry points
2. Requester, account, tenant, feature, quota, data-source, and context authorization checks
3. Input normalization, size, attachment, personal-data, secret, and prompt-injection boundaries
4. System instruction, prompt template, version, context ordering, model, parameters, token budget, and provider request
5. Provider client, streaming, timeout, cancellation, finish reason, usage, and uncertain result
6. Raw-response handling, structured parsing, schema and business validation, moderation, and bounded repair
7. Accepted-output persistence, downstream handoff, cache, notification, and idempotency
8. Audit, privacy, cost, latency, monitoring, support tools, and tests

## Rules the code should protect
- Only authorized tenant-scoped context may enter a generation request
- Untrusted input must not override protected instructions or permissions
- Only schema-valid and business-valid output may reach downstream consumers
- Safety, refusal, truncation, timeout, and uncertainty must remain explicit states
- Retry and repair must be bounded and version-aware
- Repeated requests must not duplicate expensive or material downstream effects unintentionally
- Usage, validation, safety, version, latency, and cost must remain observable
- Prompts, outputs, secrets, personal data, and credentials must remain protected

## Build or change safely
1. Confirm product decisions before relying on model, retrieval, framework, or provider defaults.
2. Follow existing authorization, validation, storage, logging, monitoring, and test conventions.
3. Bind every action to the authoritative actor, tenant, source or prompt, version, state, and scope.
4. Enforce permission, current-state, schema, evidence, uniqueness, and limit rules before material use.
5. Make retries and replays safe after partial failure and lost responses.
6. Keep invalid output, missing evidence, cost, and downstream inconsistency visible and repairable.
7. Add the core 20 tests.

