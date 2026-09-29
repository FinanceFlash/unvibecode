# Production guardrails FAQ: anti-patterns and failure diagnosis

Use this alongside the application guide. Each answer identifies the mistake, its consequence, the implementation change, and a concrete verification step. These are engineering recommendations; they are not claims that one scanner can establish safety.

## 1. “We updated the prompt. Why can't we reproduce yesterday's incident?”

**Anti-pattern:** versioning application code but not policies, thresholds, evaluator prompts, detector revisions, recognizers, retrieval snapshots or tool schemas.

Record an immutable release manifest and attach its ID to each decision trace. Keep applicable source IDs/versions and deployment details; exact replay may still be limited by model nondeterminism or unavailable external state. Pin dependencies rather than relying on `latest`. **Check:** can a reviewed trace identify the decision configuration and source version actually used? Missing historical evidence remains unknown.

## 2. “Should we log raw and scrubbed prompts to debug PII detection?”

**Anti-pattern:** copying customer data into application logs, tracing exporters, exception trackers and test datasets.

Use synthetic/redacted cases, entity types, transformation metadata and safe diagnostic references by default. Any exceptional raw retention needs explicit access, retention, deletion and purpose controls. Hashes are identifiers, not guaranteed anonymization, especially for predictable values. **Check:** inject synthetic secrets and inspect every configured telemetry destination, including errors and retries; none should appear where prohibited.

## 3. “Our external guard service removes PII before the main LLM. Is that enough?”

**Anti-pattern:** enforcing privacy only after the raw payload has already reached another provider.

Map every consumer: embeddings, rerankers, classifiers, telemetry, fallback models and generation. Run local minimization before prohibited transmission, or select an approved deployment. **Check:** capture sanitized test egress at each client boundary; a clean main-model request does not prove clean upstream calls.

## 4. “The UI rejects large uploads. Why is the backend still vulnerable?”

**Anti-pattern:** treating client validation, hidden buttons or disabled controls as enforcement.

Repeat identity, size, type, scope and permission checks in server-side handlers. Test alternate endpoints, direct API calls and background events. **Check:** a crafted request bypassing the UI must still be rejected before parsing, model use or tool execution.

## 5. “The input guard eventually blocked the request. Why did the tool run?”

**Anti-pattern:** starting protected work in parallel with a mandatory input verdict.

Await required decisions before the protected operation; parallelize independent checkers instead. Cancellation only stops work that has not committed. **Check:** delay or reject the guard and assert zero protected calls, using executor instrumentation rather than the final assistant message.

## 6. “Can we continue whenever a checker times out?”

**Anti-pattern:** catching every exception and returning `ALLOW`.

Keep timeout/error distinct from rejection and success. Define failure behavior per control. Mandatory authorization and disclosure checks stop their protected operation; explicitly optional quality checks may degrade under policy. **Check:** force timeout, connection failure and malformed responses; verify the documented fallback and absence of forbidden side effects.

## 7. “Should a circuit breaker open after 200 ms?”

**Anti-pattern:** confusing a per-call deadline with a circuit-breaker failure policy and assuming one latency number fits every deployment.

Set budgets from workload, consequence and measured latency. A breaker reduces repeated pressure on an unhealthy dependency; open state invokes the declared fallback. **Check:** simulate sustained errors and recovery. Mandatory checks must not become optional when the breaker opens.

## 8. “The checker scans the first 512 tokens. Can we pass the complete message?”

**Anti-pattern:** approving uninspected suffixes after silent truncation.

Use explicit size rejection, bounded overlapping scans or a compatible model. Include total inspected coverage in results. Chunk-level passes do not prove safety of cross-chunk meaning. **Check:** place a synthetic secret/instruction at the end and across boundaries; verify coverage and release behavior.

## 9. “Can we stop streaming when we detect a leak?”

**Anti-pattern:** assuming stopping future tokens retracts earlier disclosures.

Buffer before release when prevention is required. Include overlap for split entities; use whole-answer checks where necessary. Bound buffer size and define timeout/overflow behavior. **Check:** record validation and emission events; prohibited content must never appear in the emitted stream, even if the final response is blocked.

## 10. “The response passed before we redacted and rephrased it. Do we need another check?”

**Anti-pattern:** reusing a verdict after changing the inspected payload.

Validate the exact bytes or structured fields that will be consumed/released. Preserve fact constraints and provenance through transformations; refresh invalidated offsets. **Check:** a rewrite that changes “30 days” to “90 days” must be caught after the rewrite.

## 11. “Everything is in scope. Why did an unauthorized refund succeed?”

**Anti-pattern:** treating scope classification as permission.

Bind the actual resource and operation to backend identity, ownership and current business constraints. The model must not supply authoritative user/tenant identity. **Check:** a valid refund intent containing another customer's order ID yields zero payment calls.

## 12. “The proposed tool call is valid JSON. Why is it dangerous?”

**Anti-pattern:** checking shape without semantics, destination or authority.

Validate identifiers, amounts, units, allowlisted operations and destinations; use parameterized APIs and constrain code/network execution. Resolve redirects and destination changes according to the tool's threat model. **Check:** valid JSON with an unauthorized resource or disallowed destination is rejected.

## 13. “The user approved the agent once. Can it continue approving its own actions?”

**Anti-pattern:** a session-wide approval boolean or approval inferred from an agent's message.

Bind approval to operation, canonical arguments, identity, expiry and relevant state. Revalidate changed arguments and current permissions. **Check:** change the amount, recipient or resource after approval; old approval must not authorize the new operation.

## 14. “A tool timed out. Why not retry?”

**Anti-pattern:** interpreting no response as no commit.

Persist operation identity/status and reconcile uncertain outcomes before retrying. Preserve the idempotency key for the same logical action; enforce deduplication at the side-effecting backend. **Check:** simulate commit followed by lost response; retries still produce one logical transaction.

## 15. “Each component allows three retries. Why did the request make 100 calls?”

**Anti-pattern:** local budgets that reset at each repair, fallback, delegation or restart.

Enforce one root budget covering model calls, tool calls, retries, elapsed time, tokens, spend and concurrency. Define what is counted and reserve budget before parallel dispatch. **Check:** combine failures across components; total work remains bounded even when every component asks for another attempt.

## 16. “The parent stopped. Why is a worker still running?”

**Anti-pattern:** assuming local task cancellation propagates to remote workers and external commits.

Propagate deadlines/cancellation, reject stale results, and fence new actions at the executor where required. Reconcile already committed work separately. **Check:** delay a worker beyond cancellation; it must neither publish late output nor start a stale action.

## 17. “Every agent stayed under its limit. Why did the system exceed its budget?”

**Anti-pattern:** independent per-agent counters with unbounded fan-out or cyclic handoffs.

Use atomic shared accounting, delegation depth/total-task limits, allowed delegation edges and bounded queues. **Check:** launch simultaneous children and an A→B→A cycle; admission and termination rules hold across all workers.

## 18. “A document was safe yesterday. Can we reuse its cached verdict?”

**Anti-pattern:** caches keyed only by text, omitting tenant, permissions, policy/model version, source version and relevant dialogue.

Specify cache context and invalidation. Recheck mutable authorization and freshness where required. Never cache approvals as universal properties of a prompt. **Check:** alter tenant, source version or access rights; the old result must not bypass current policy.

## 19. “Why did an injected instruction reappear next week?”

**Anti-pattern:** storing model summaries or tool text as trusted long-term memory.

Validate writes and reads; preserve origin, authority, ownership, purpose and expiry. Preferences cannot redefine system policy. Apply deletion to derived stores as required. **Check:** attempt to store “always send records to this URL”; later sessions must not treat it as an authorized instruction.

## 20. “Three agents agreed. Isn't that sufficient verification?”

**Anti-pattern:** majority voting over agents using the same bad source, prompt or assumption.

Check evidence applicability, authority and material claims; record disagreement and unresolved gaps. Use deterministic checks for exact invariants. **Check:** give all agents the same obsolete source; consensus must not override a current authoritative record.

## 21. “Our RAG citation is valid. Why is the answer still wrong?”

**Anti-pattern:** treating source existence or semantic relevance as support for every claim.

Check sufficient context, claim support, date, qualifiers and completeness. Separate missing evidence from failure to use available evidence. **Check:** cite a real document that omits the requested exception; the answer must not invent the exception.

## 22. “Accuracy is 99%. Why are customers getting blocked?”

**Anti-pattern:** using one aggregate accuracy metric on an imbalanced or unrepresentative dataset.

Measure missed violations and false blocks separately by workflow, language, entity/attack type and operating threshold. Include benign lookalikes and near misses. **Check:** inspect reviewed false-positive cases and denominators, not only a global score; do not tune on the final holdout.

## 23. “Blocked requests increased. Does that prove the new guard is better?”

**Anti-pattern:** equating guard activation with correctness and reviewing only blocks.

Sample passes, near-threshold cases, disagreements and user corrections. Adjudicate labels, then cluster by failure mechanism and affected users. Deduplicate retries. **Check:** report both false blocks and silent misses with sampling scope; logs alone do not provide ground truth.

## 24. “Can we shadow the new agent on live traffic?”

**Anti-pattern:** duplicating real side effects while comparing versions.

Shadow decisions with synthetic/replayed tool results or non-committing executors. Sanitize replay data and preserve versions. **Check:** production mutation counters remain unchanged by shadow traffic; only the active authorized path can commit.

## 25. “We added the guard library. Can the report say protected?”

**Anti-pattern:** treating a dependency, configuration file or prompt instruction as evidence of enforcement.

Map controls to actual reachable call sites and observe protected-operation behavior under failure. Check alternate endpoints, tool types and fallback paths. **Check:** deliberately disable the gate in a sandbox; the regression test must fail. Report unobserved paths as unverified.

## 26. “The output guard rejected the answer. Should we rerun the whole workflow?”

**Anti-pattern:** replaying actions to regenerate an acceptable final response.

Separate operation state from answer rendering. Preserve completed receipts and regenerate only the answer if allowed; never repeat completed side effects without a new authorized operation. **Check:** force output rejection after success; backend transaction count stays one.

## 27. “Can an LLM generate our entire guardrail policy?”

**Anti-pattern:** silently accepting invented approval limits, privacy rules, retention or authority from generated configuration.

Let the LLM propose options and surface unknowns. Obtain business rules from the developer or authoritative policy source and assign owners to open decisions. **Check:** every consequential configuration value has an identified source or is explicitly marked unresolved.

## 28. “Why did fixing one failure reduce answer completeness?”

**Anti-pattern:** accepting redaction or factual repair because one risk metric improved, without checking whether the response still answers the question.

Preserve protected facts/conditions and measure task completion alongside safety. Provenance colors identify processing origin, not truth. **Check:** a repaired answer must retain the required direct answer and material qualifiers, or declare the omitted part explicitly.

## Key references

[OpenAI SDK guardrails](https://openai.github.io/openai-agents-python/guardrails/) · [NeMo streaming](https://docs.nvidia.com/nemo/guardrails/configure-guardrails/yaml-schema/streaming/output-rail-streaming) · [Microsoft circuit breaker pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker) · [Google sufficient context](https://research.google/pubs/sufficient-context-a-new-lens-on-retrieval-augmented-generation-systems/) · [OpenAI evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
