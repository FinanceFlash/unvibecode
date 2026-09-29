# Multi-agent guardrails: implementation and design guide

A supervisor can approve a plan while a specialist executes an unauthorized action. Every delegation boundary needs an explicit contract.

Use this guide for manager–worker systems, peer handoffs, parallel specialists and agents invoking other agents as tools. Each tool-using agent also needs the controls in the tool-agent guide; this document includes the critical shared requirements.

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

1. What agents exist, who can delegate to whom, and does the system use handoffs, agents-as-tools, parallel tasks or dynamic spawning? Ask for the actual topology.
2. What permissions, credentials, tools and data scope does each agent receive, and which delegation boundaries must preserve or reduce that scope?
3. What context crosses each boundary—full history, summaries, retrieved documents, memory or typed task fields—and which parts contain sensitive/untrusted data?
4. Which agent can authorize or execute side effects, and how are user identity, approvals, idempotency and resource ownership preserved end to end?
5. How are global token/spend/time limits, delegation depth, fan-out, retries and concurrency enforced across workers? What happens when one child fails or the parent cancels?
6. Who resolves conflicting results and partial completion, and which evidence establishes correctness? What should the user see if some tasks succeed and others fail?

## Stage-by-stage controls

| Stage / interface | What to implement | Method | Failure path / release rule |
|---|---|---|---|
| User/event → root coordinator | Authenticate, route scope, check privacy/injection; establish root trace and budget | T1/T3; T5 via T2–T4 | Reject/clarify before launching children |
| Coordinator → task planner | Allowlisted agent graph, roles and supported operations; classify consequential tasks | T1; T4 only as advisory review | Unsupported delegation/operation is rejected, not improvised |
| Planner → child dispatch | Typed task envelope: root/parent IDs, task, origin, tenant/user, data scope, policy version, deadline and reserved budget | T1 | Missing/conflicting context blocks dispatch; caller cannot invent authority |
| Context → receiving agent | Minimize history; retain provenance/trust labels; screen untrusted content and secrets | T1/T3 | Do not promote a peer's summary to system policy; reject oversized or uninspectable context |
| Child → further delegation | Enforce allowed edges, delegation depth and total work; propagate restricted authority and remaining budget | T1 | Block cycles/unauthorized delegation; a new child cannot reset counters |
| Any agent → tool executor | Independently validate tool, args, ownership, destination, business constraints and bound approval | T1 | Central or per-tool backend enforcement denies unauthorized actions regardless of sender |
| Parallel workers → shared state | Reserve budget atomically; isolate sessions; use resource concurrency control and durable idempotency | T1 | Prevent overspend, cross-task contamination and duplicate/conflicting writes |
| Child result → coordinator | Typed result/status with source evidence, operation receipts and unresolved gaps; verify provenance and schema | T1/T3; T4 for semantic checks | A confident narrative is not proof of success; malformed/unsupported results remain unresolved |
| Conflicting results → adjudication | Apply source authority and validation rules; bounded independent review | T1/T4 | No automatic majority-is-truth rule; escalate/abstain when evidence conflicts |
| Coordinator → final answer | Check combined grounding, completeness, privacy, and honest partial-operation status | T1/T3/T4 | Gate final release; retain success/failure per operation rather than claiming global success |
| Shared memory → future runs | Scope by tenant/task/purpose; approve writes; retain source and expiry; recheck reads | T1/T3 | No untrusted instruction shared as policy; no cross-agent privilege accumulation |

## Multi-agent-specific failure paths

- **A delegates to B, B delegates to A:** cap delegation depth, total invocations and time; track repeated task signatures with context so legitimate repetition is not automatically blocked.
- **Parallel budget race:** allocate reservations from a shared ledger before dispatch; reconcile actual use after completion. Local per-agent caps alone cannot enforce a root cap.
- **Late result after cancellation:** reject stale task results and prevent new commits using an active-run check or fencing at the executor. Do not assume cancelling the parent stops remote workers.
- **Manager grants its credentials to a worker:** issue scoped capabilities for the assigned task; enforce boundaries at backend tools. A text instruction to “stay in scope” is insufficient.
- **Peer text claims human approval:** approval must come from the trusted approval store bound to the operation, not from a message or summary.
- **Supervisor retries a failed child that already committed:** reconcile durable operation IDs before restarting; preserve idempotency across parent and child retries.
- **Two workers take conflicting actions:** use transactions, conditional updates or a designated commit owner. Do not resolve committed conflicts by choosing the best-written summary.
- **One child fails after others succeed:** record per-task status; allow partial answer only if policy permits. Compensation requires explicit authorization and supported semantics.
- **Agents agree on the same bad source:** agreement is correlated evidence, not independent verification. Validate source applicability and material claims.
- **Handoff loses provenance or user identity:** receiver rejects incomplete envelopes or fetches trusted identity context; it must not reconstruct authority from natural language.
- **Policy changes during long-running work:** define snapshot versus mandatory revocation behavior; enforce urgent permission revocations at execution even for an older plan.
- **Unbounded adjudication:** disagreements consume the same review and root budgets. Stop with an unresolved result when limits are reached.

## Minimum acceptance scenarios

| Scenario | Expected behavior and evidence |
|---|---|
| Specialist receives valid bounded task | Only permitted data/tools; trace links root, parent, child and policy |
| Child requests an unapproved specialist/tool | Delegation or execution denied outside the permitted graph |
| Worker repeats a forged “approved by user” message | No action without trusted approval record |
| Parallel tasks exhaust shared budget | Atomic admission stops further work; no per-child budget reset |
| Worker responds after parent cancellation | Late content is not published; executor blocks stale new actions |
| Two workers submit the same refund | Exactly one logical backend operation under durable idempotency |
| Children disagree on a policy date | Authority/evidence checked; no majority-vote shortcut |
| A → B → A loop | Bounded termination with causal trace and unresolved task status |
| One task succeeds and one fails | Final output reports accurate partial status; no whole-workflow replay |

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

## Framework integration note

Do not assume agent-level guards execute at every handoff. OpenAI documents first-agent input guards, final-agent output guards, and per-invocation guards on guarded function tools. Inspect the deployed framework's handoff and context-transfer behavior explicitly. [SDK guardrails](https://openai.github.io/openai-agents-python/guardrails/) · [Handoffs](https://openai.github.io/openai-agents-python/handoffs/)

The shared budget, authority, state and cancellation contracts above are application-level requirements, not guarantees supplied merely by using multiple agents.
