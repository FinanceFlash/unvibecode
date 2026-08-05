# Testing Guide

Check authoritative context, permissions, versions, validation, evidence, downstream effects, recovery, and audit—not only displayed answers.

## 1. Valid request returns schema-valid output

**Given:** An authorized request has approved context, prompt version, model, and output schema

**When:** Generation and validation run

**Expect:** One accepted output satisfies schema and business rules

**Must not happen:** Raw or invalid model text reaches the consumer

**Best test levels:** Integration and end-to-end.

## 2. Allowed content passes safety validation

**Given:** A valid request asks for permitted content within product policy

**When:** The model and safety checks complete

**Expect:** The accepted output is useful and policy compliant

**Must not happen:** A safe answer is blocked silently or unsafe content bypasses checks

**Best test levels:** Integration.

## 3. Malformed output is repaired within limit

**Given:** The first response is parseable only after an allowed repair attempt

**When:** Repair runs

**Expect:** One validated output is accepted with repair history

**Must not happen:** Repairs loop indefinitely or change the requested meaning

**Best test levels:** Integration.

## 4. Required input or schema is missing

**Given:** The request lacks user input, context identity, prompt version, model, or required schema

**When:** Validation runs

**Expect:** The request fails before provider submission

**Must not happen:** The model is called with guessed policy or shape

**Best test levels:** Unit and API.

## 5. Input or response is malformed or excessive

**Given:** Text, attachment, encoding, token count, nesting, or schema complexity exceeds policy

**When:** Validation runs

**Expect:** Unsafe input or output is rejected explicitly

**Must not happen:** Resource limits, parsers, or logs are abused

**Best test levels:** Unit, API, and security.

## 6. Requester lacks context permission

**Given:** The user can invoke generation but cannot access a referenced document, tenant, field, or feature

**When:** Authorization runs

**Expect:** The context is excluded or the request is denied

**Must not happen:** Generation leaks inaccessible information

**Best test levels:** Authorization and security.

## 7. Prompt injection attempts override policy

**Given:** User input or attached content instructs the model to reveal secrets or ignore system rules

**When:** Prompt assembly and validation run

**Expect:** Protected authorization, privacy, and output rules remain effective

**Must not happen:** Untrusted text changes system authority

**Best test levels:** Security and adversarial.

## 8. Unicode and locale reach boundary

**Given:** Input contains mixed scripts, direction controls, unusual whitespace, locale formats, or normalization variants

**When:** Normalization and generation run

**Expect:** Meaning and validation follow one documented Unicode and locale policy

**Must not happen:** Hidden or equivalent text bypasses rules or schema checks

**Best test levels:** Unit and security.

## 9. Equivalent requests run concurrently

**Given:** Two workers receive the same permitted idempotent request

**When:** Both call or persist

**Expect:** Policy yields one reusable result or explicitly separate generations

**Must not happen:** Downstream effects or billing duplicate unexpectedly

**Best test levels:** Concurrency integration.

## 10. Token or timeout boundary is reached

**Given:** Prompt and output are tested just below, at, and above token, latency, or cost limits

**When:** Generation runs

**Expect:** One explicit truncate, reject, cancel, or fallback rule applies

**Must not happen:** Partial output is reported as complete

**Best test levels:** Controlled-limit integration.

## 11. Generation response is lost

**Given:** The provider or service may have completed but the caller sees no result

**When:** The client retries

**Expect:** Idempotency or explicit regeneration policy returns a safe outcome

**Must not happen:** Costs and downstream effects multiply silently

**Best test levels:** API and integration.

## 12. Completed request is replayed

**Given:** A request identity already produced an accepted or blocked result

**When:** The request is submitted again

**Expect:** The existing outcome is reused or a new generation is explicit

**Must not happen:** Replay bypasses policy version or duplicates effects

**Best test levels:** Integration.

## 13. Generation is flooded

**Given:** One actor sends large, repeated, concurrent, or adversarial requests

**When:** Quota and abuse controls run

**Expect:** Tokens, cost, concurrency, and provider traffic remain bounded

**Must not happen:** One user exhausts budget or service capacity

**Best test levels:** Security and load.

## 14. Output validates but persistence fails

**Given:** The accepted output exists in memory but storage or handoff does not commit

**When:** Recovery runs

**Expect:** The output is safely persisted once or the request remains incomplete

**Must not happen:** The service reports success while no usable artifact exists

**Best test levels:** Integration.

## 15. Provider times out uncertainly

**Given:** The LLM returns no reliable completion status

**When:** Failure handling runs

**Expect:** The request remains failed or uncertain under bounded retry policy

**Must not happen:** Timeout becomes accepted content or endless retry

**Best test levels:** Provider contract and integration.

## 16. Provider succeeds but response is lost

**Given:** The provider generated output while the service response failed

**When:** Retry or reconciliation runs

**Expect:** Recovered output is revalidated or regeneration is explicitly controlled

**Must not happen:** Unvalidated or duplicate output reaches downstream effects

**Best test levels:** Integration.

## 17. Cross-tenant context is referenced

**Given:** A valid requester supplies a context or cached result from another tenant

**When:** Generation runs

**Expect:** Tenant binding denies access

**Must not happen:** Identifiers or cache keys cross the data boundary

**Best test levels:** Authorization and security.

## 18. Generation error is logged

**Given:** The path contains prompts, documents, model output, personal data, and provider credentials

**When:** An error occurs

**Expect:** Diagnostics avoid secrets and unnecessary sensitive content

**Must not happen:** Raw protected prompts or credentials reach logs

**Best test levels:** Security and log inspection.

## 19. Version changes during retry

**Given:** Prompt, model, schema, or safety policy changes after the original attempt

**When:** The request retries

**Expect:** The original version is retained or a new run is explicit

**Must not happen:** One logical request mixes incompatible versions

**Best test levels:** Integration.

## 20. Downstream consumer rejects accepted output

**Given:** Local validation passes but a database, API, or business consumer rejects the output

**When:** Repair or reconciliation runs

**Expect:** The failure is visible and corrected without silently weakening validation

**Must not happen:** The product reports success or repeatedly triggers material effects

**Best test levels:** Integration and operations.

