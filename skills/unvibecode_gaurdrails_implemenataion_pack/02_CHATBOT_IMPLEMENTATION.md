# Conversational chatbot guardrails: implementation and design guide

“Cancel it” is a clarification problem. “Cancel another customer's order” is an authorization problem. A chatbot should not give both requests the same generic refusal.

Use this guide for conversational applications. Add RAG controls for retrieved knowledge and tool-agent controls whenever the chatbot changes state.

## Instructions to the LLM using this guide

Act as the implementation architect for the developer's application. Treat this document as a design checklist, not evidence that a control exists.

1. Read the developer's context first. Summarize the known workflow, users, data, stack, deployment constraints, and consequential operations. Label assumptions and contradictions. Do not repeat questions already answered.
2. In your first response, ask **5–6 specific questions in one numbered list**. Adapt the question bank below to the stated context: name the actual data sources, tools, languages, and deployment choices when supplied. Prioritize unanswered decisions that change control placement or behavior. If context already answers the bank, ask about unaddressed failure, concurrency, acceptance, or recovery decisions; do not fabricate uncertainty to fill a quota.
3. Do not ask generic questions such as “What are your requirements?” Each question must explain the design decision it resolves. Offer concrete choices where useful. Accept “not decided” and propose a clearly labeled starting option with a trade-off. Never invent business limits, ownership rules, retention periods, or approval authority.
4. After the developer responds, produce the design in the output format below. If asked to proceed without answers, produce a draft with explicit unresolved decisions. Do not call it production-ready.
5. Combine capability requirements: a chatbot that retrieves and calls tools needs all three sets of controls. For capabilities outside this guide, request the corresponding guide or document the additional boundaries explicitly. Never let an application label remove a required control.
6. Use deterministic checks for exact constraints and probabilistic detectors for ambiguous content. A detector's score is not authorization. Place enforcement in application or infrastructure code outside the model's discretion.
7. Verify framework-specific APIs against the selected installed version before suggesting executable integration code. If documentation cannot be checked, mark the API detail unverified. Do not invent callable methods.
8. Do not request production secrets or raw customer records. Use schemas, redacted traces, and synthetic examples. Propose tests against a sandbox; never execute side-effecting tests against production as part of design review.

## Checking methods: use the cheapest adequate method

| Label | Method | Appropriate use | Limit |
|---|---|---|---|
| T1 | Deterministic rules | Authentication, ownership, schema, exact patterns, quotas, destination restrictions, idempotency | Rules require authoritative inputs; a remote authorization lookup may still add latency |
| T2 | Embeddings / semantic matching | Supported intent candidates and semantic scope matching | Similarity is not a calibrated probability; weak or close matches need clarification or escalation |
| T3 | Specialized detector | PII, prompt injection, task-specific content risks, narrow evidence classification | Benchmark the detector on the actual language and input distribution |
| T4 | Evaluator LLM | Ambiguous policy interpretation, contextual evidence review | Fallible; consumes latency and tokens; cannot grant permissions |
| T5 | Scope / intent routing function | Answer, clarify, route, or reject unsupported scope | Uses T1–T4 as needed; runs early and is not a fifth cost level |

Candidates, not mandatory dependencies: Presidio for configurable PII handling; a small Sentence Transformers model for intent matching; Prompt Guard 2 for injection screening. Check model licenses separately from library licenses, pin revisions, and compare candidates on your own cases. No universal detector or latency threshold is assumed. Do not send sensitive data to an external checker before the required local privacy gate.

## Six context-aware clarification questions

1. Which tasks can the chatbot support, and which near-miss requests should trigger clarification instead of rejection? Ask for examples drawn from the developer's actual domain.
2. Who are the users, how is identity/session ownership established, and can anonymous users access different information from authenticated users?
3. Which sensitive fields may users submit, which are necessary for the task, and which may leave the environment or be retained in chat history?
4. Does the chatbot only respond, or also retrieve, call APIs, hand off to staff, or store long-term preferences? Confirm every capability mentioned in the context.
5. Which content policies apply, which languages are expected, and what legitimate phrases might resemble violations in this domain?
6. What streaming behavior, latency budget, maximum conversation size, timeout fallback, and human-escalation capacity are acceptable?

## Stage-by-stage controls

| Stage / interface | What to implement | Method | Failure path / release rule |
|---|---|---|---|
| UI → chat API | Server-side identity/session binding, payload limits, attachment policy and abuse quotas; explain required fields in UI | T1 | Reject invalid sessions/inputs; never rely on hidden buttons or UI-only checks |
| Raw message → external service | Detect/minimize sensitive data locally if policy requires; preserve task meaning with stable placeholders | T1/T3 | Redact and revalidate; unsupported entity/language handling is explicit |
| Message + relevant dialogue → intent | Match supported intents; compare top candidates; distinguish ambiguous, unsupported and mixed requests | T5 using T1/T2 and optional T3/T4 | Clarify ambiguity; reject unsupported operations; never let an allowed fragment approve the whole message |
| Input safety → model gate | Detect injection and prohibited content independently of scope; bind policies to deployment | T1/T3; T4 selectively | Mandatory gates finish before model work; error uses explicit fallback |
| History/summary → prompt assembly | Keep trusted instructions separate; cap history; preserve attribution; check summaries and reused memory | T1/T3 | Untrusted instructions remain data; do not infer consent/permissions from an old summary |
| Model → candidate response | Set output limits and bounded correction attempts; restrict expected formats where useful | T1 plus generation constraints | Invalid output is rechecked after bounded repair or withheld |
| Candidate → streaming/UI | Check disclosure and policy before release; escape/sanitize rendered HTML/Markdown and links; keep active content inert | T1/T3; T4 for contextual review | Buffer as required; no dangerous HTML, unsafe links, or unchecked chunks |
| Conversation → handoff | Transfer only approved context to an authenticated destination; preserve escalation reason and provenance | T1 | Queue/notify honestly when staff unavailable; do not claim a human accepted the case |
| Conversation → history/memory | Scope retention to user and purpose; validate memory writes; enforce deletion and sensitive-data rules | T1/T3 | Disallowed memory is not stored; deletion applies to derived summaries/caches as required |

## Chatbot-specific failure paths

- **Ambiguous follow-up:** inspect relevant recent context; ask a narrow clarification. Do not guess the account, order, or operation.
- **Topic changes mid-conversation:** re-evaluate scope and policy for the new task; an earlier pass is not session-wide approval.
- **Mixed allowed/disallowed request:** handle supported content only if separable and permitted; never execute the disallowed fragment.
- **Benign policy lookalike:** include examples such as “kill a process” for developer support. Tune with reviewed false-positive cases rather than a blanket bypass phrase.
- **History compaction changes meaning:** keep facts/decisions linked to source turns; protected constraints survive compaction; proposed summaries remain lower-trust content.
- **Parallel requests in one session:** define ordering or version checks; avoid applying one request's pending clarification or private state to another.
- **Long conversation evicts policy:** trusted instructions are constructed separately from truncatable dialogue. Reject oversized unchecked attachments.
- **Retrying a refused answer indefinitely:** bound reasks and alternate-model fallbacks; enforce identical mandatory policies on every fallback model.
- **Staff unavailable:** give the real escalation state and allowed next step. Human escalation must have an owner and finite queue policy.
- **Rendered answer triggers external requests:** inspect URL destinations and active content; a safe text classifier does not protect a browser renderer.

## Minimum acceptance scenarios

| Scenario | Expected behavior and evidence |
|---|---|
| Clear supported request | Correct route with no unnecessary clarification |
| “Cancel it” without a unique referent | Clarification; zero state-changing calls |
| Supported question plus request for another user's history | Privacy boundary holds; no cross-user disclosure |
| PII in an attachment or later dialogue turn | Required local handling occurs before every external consumer |
| Quoted malicious text used for a legitimate support question | Domain-appropriate decision; classifier score alone is not final business policy |
| Toxicity/injection service times out | Explicit fallback; no hidden mandatory-check bypass |
| Concurrent requests after session change | Isolation and history ordering hold |
| Repair/fallback path produces disallowed output | Same release checks apply; attempts stop at the shared limit |

## Common failure contract and runtime design

Every control must declare: boundary, protected operation, mandatory/optional status, input schema, detector/version, policy/version, deadline, allowed transformations, and behavior for each outcome.

- Keep `ALLOW`, `REDACT`, `CLARIFY`, `BLOCK`, `ABSTAIN`, and `ESCALATE` as policy decisions. Keep `ERROR`, `TIMEOUT`, `UNSUPPORTED_INPUT`, and `NOT_RUN` as execution states; map each explicitly to a response. Missing verdicts are never automatic passes.
- Run independent checks with bounded concurrency; await all mandatory verdicts before the protected operation. Async I/O does not require fail-open execution. Place CPU/GPU inference in appropriate workers or model serving, not on the event loop.
- Validate format and size first. Never silently truncate, approve the visible prefix, and forward the uninspected suffix. Choose rejection, bounded chunk inspection, or a compatible detector; preserve relevant overlap and distinguish a partial scan.
- Revalidate transformed content. Redaction, repair, query rewriting, or summarization can change meaning or invalidate earlier offsets and findings. Retain safe transformation metadata and source mappings.
- Define an end-to-end deadline plus per-stage deadlines. Bound model calls, evaluator reasks, retries, input/output tokens, concurrency, queue depth, and cumulative spend. Include fallback and retry work in the same root-request budget. Configure values from workload and impact; never present arbitrary defaults as universal safe limits.
- Retry only retryable failures within the remaining budget. Distinguish a rejected request from an unhealthy checker. A circuit breaker invokes the configured failure policy; it does not disable a mandatory check.
- On mandatory authorization or disclosure-check failure, stop the affected operation. Where permitted, offer a reduced-capability response, abstention, or review. An optional quality check may fail open only under an explicit policy with a recorded reason.
- Stop future work when the request expires or is cancelled. Cancellation cannot undo committed external work; reconcile operation state before reporting success, failure, or inviting a retry.
- Use stateless workers where useful, with controlled stores for sessions, budgets, approvals, and durable operations. Shared services require admission control and capacity planning; local rules need not become network calls.
- Key caches by all relevant security and semantic context: tenant/user scope, applicable policy/model versions, content identity, and dialogue where needed. Revalidate mutable authorization. Never reuse another tenant's answer or an old approval because text matches.
- Gate output before release. Windowed scanning needs bounded buffers and overlap; whole-answer claims may require full buffering. A late final check cannot retract already displayed tokens. Define an explicit fallback for buffer limits and checker outages.
- Record minimal decision events with trace IDs, boundary, policy/checker versions, verdict/status, duration, and protected-operation outcome. Avoid raw prompts, retrieved records, secrets, and PII in ordinary logs, exceptions, exporter payloads, and evaluation datasets. Specify retention, access, and deletion.
- Version the complete decision path: prompts, policy, thresholds, models, recognizers, source/index snapshot, tools, permissions configuration, and deployment. Preserve reviewed failures as regression cases; use offline evaluation, side-effect-free shadowing, canaries, and rollback criteria.

## Required design output

After clarification, return these artifacts in Markdown:

1. **Context and open decisions:** confirmed requirements, assumptions, unresolved decisions, and accountable owners.
2. **Architecture:** a compact sequence or flow diagram showing trust boundaries, enforcement points, stores, and external dependencies. Label where content, state, money, or credentials can cross a boundary.
3. **Control matrix:** `control ID | stage/interface | protected operation | T1–T4 method or T5 route | authoritative inputs | implementation owner | decision | error/timeout behavior | budget | verification evidence`.
4. **Failure paths:** rejection, ambiguity, insufficient evidence, detector disagreement, timeout, malformed verdict, overload, oversized input, retry exhaustion, cancellation, and application-specific failures below. State exactly what can still execute or be released.
5. **Configuration plan:** concrete fields and version ownership; unresolved values remain explicitly unset. Map detector choices to language, deployment, and privacy constraints. Separate suggestions from approved policies.
6. **Integration order:** small implementation steps tied to actual UI/API, model, retrieval, tool, memory, and output interfaces. Client-side controls are convenience checks; server-side enforcement remains authoritative.
7. **Acceptance cases:** include legitimate requests, near misses, attacks, dependency failures, and concurrent/retry cases. For each, specify the expected decision AND forbidden side effects. Identify which tests require instrumentation.
8. **Deployment and verification:** baseline quality/latency measurements, reviewed labels, roll-out gates, privacy-safe telemetry, and evidence status. Use `PROPOSED`, `CONFIGURED`, `IMPLEMENTED`, or `VERIFIED_IN_TESTED_SCOPE`; do not claim universal safety.

Treat the listed failures as a minimum inventory. Ask which additional failure paths follow from the developer's actual stack and external systems; no generic guide exhausts all possible failures.

## Source notes

- [NeMo configuration reference](https://docs.nvidia.com/nemo/guardrails/latest/configure-guardrails/configuration-reference) documents embedding-based intent matching and fallback configuration.
- [Presidio supported entities](https://microsoft.github.io/presidio/supported_entities/) documents recognizer coverage; validate the languages and identifiers relevant to the application.

The stage plan and failure cases are engineering recommendations. Detector coverage and latency require application-specific evaluation.
