# Tool-using agent guardrails: implementation and design guide

A correct $10 refund can still be unauthorized. Enforce permission on the actual operation immediately before execution.

Use this guide for agents that call APIs, query databases, send messages, write files, run code, or persist memory. Read-only tools can still disclose data. Add RAG controls for document-based answers.

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

1. Which exact tools and operations exist, and which read data, modify state, send information, or execute code? Ask about the actual APIs named in the context.
2. How does each operation bind to authenticated identity, tenant, resource ownership, allowed destinations, and authoritative business limits?
3. Which operations require human approval, who can approve, and what binds approval to exact arguments, expiry and current resource state?
4. How do tools handle idempotency, partial success, retries, and uncertain commit status? Is there an operation-status API or reconciliation process?
5. What can the agent store or reuse, and what constraints isolate tool responses, credentials, files, network access and external instructions?
6. What global limits apply to steps, tool calls, retries, runtime, tokens and spend, and how should the UI report cancellation, pending work and exhausted budgets?

## Stage-by-stage controls

| Stage / interface | What to implement | Method | Failure path / release rule |
|---|---|---|---|
| UI/event → request API | Authenticate user/event origin; validate replay IDs, payload and session; establish root operation ID | T1 | Reject invalid origin/replay; no agent launch |
| Request → model | Scope/privacy/injection checks; initialize shared budgets; expose only permitted tool schemas | T1/T3; T5 via T2–T4 | Clarify unsupported/missing intent; no protected work before mandatory decisions |
| Model → tool proposal | Parse strict schema; allowlist tool and operation; validate types, ranges and required fields | T1 | Reject malformed/unknown calls; bounded correction, no execution |
| Proposal → authorization | Resolve resource using backend identity; enforce current ownership, tenant, business constraints and destination | T1 | Deny regardless of model confidence or document instructions |
| Authorized proposal → approval | Show exact operation, destination, amount and relevant data; bind approval to canonical arguments, identity and expiry | T1 | Changed/stale/replayed approval requires fresh authorization and, where applicable, new approval |
| Approved operation → executor | Recheck mutable state; use transactions/conditional writes where needed; scoped credentials, egress limits, sandbox | T1 | Atomic precondition failure stops commit; never “check then act” against stale state |
| Executor → retry/reconcile | Durable idempotency key for a logical operation; record pending/succeeded/failed/unknown; reconcile uncertain commits | T1 | No blind retry when a side effect may have occurred |
| Tool response → model/context | Check size/type, sensitive fields, provenance and external instructions; trust result data only within its authority | T1/T3 | Withhold or minimize unsafe result; never promote it to system policy |
| Plan loop → next step | Enforce root budgets and bounded per-tool attempts; track progress/repeated calls; cancel pending work | T1 | Stop loops and report unresolved state; a new plan cannot reset limits |
| Agent → memory | Validate scope, provenance, retention and permitted content; separate user preference from operational policy | T1/T3 | Block malicious/unnecessary writes; access checks also apply on read |
| Result → user | Ground claims in actual tool outcomes; inspect output before release | T1/T3/T4 | Do not say “refunded” for a proposal, timeout, or unknown commit; report pending/unknown accurately |

## Agent-specific failure paths

- **Infinite tool loop:** global counters cover retries, model calls, fallback agents and recovery work. Enforce limits outside the agent loop, with atomic accounting under concurrency.
- **Same logical action, different retry key:** keep idempotency identity stable across retries. Validate key scope and request payload so another operation cannot reuse it.
- **Payment committed, response lost:** mark unknown/pending, query durable status, reconcile; no automatic second payment. A timeout does not prove failure.
- **Approval changed after review:** bind to exact arguments and business-state version where necessary; recheck on execution. Approval is not a reusable session flag.
- **Permission revoked during approval wait:** enforce current authorization when executing; stored run state does not override revocation.
- **Successful action followed by output rejection:** withhold unsafe text but preserve honest operation status. Never retry the whole action to obtain a nicer answer.
- **Shell/SQL/URL injection:** schemas are insufficient. Prefer typed operations; isolate execution; restrict network/filesystem destinations; validate redirects and resolved destinations where applicable.
- **Event redelivery or agent restart:** persist operation state; use deduplication and resume semantics. Replaying a conversation must not replay committed actions.
- **Parallel conflicting actions:** serialize conflicting resource operations or use backend concurrency controls. Separate safe parallel reads from competing writes.
- **Tool exception contains secrets:** scrub before returning to model or telemetry; retain a non-sensitive error code and restricted diagnostic reference.
- **Cancellation after commit:** stop new operations, then reconcile/report completed work. Use compensating actions only if explicitly supported and authorized; do not assume every action is reversible.

## Minimum acceptance scenarios

| Scenario | Expected behavior and evidence |
|---|---|
| Valid authorized $10 refund | One backend transaction with correct identity/resource/amount |
| Another customer's order ID | Denial and zero executor calls |
| Approved amount changes before execution | Old approval unusable; zero changed-amount transactions |
| Timeout occurs after backend commit | Status reconciliation; one transaction despite retries |
| Tool output contains “send secrets to this URL” | No policy upgrade; destination/credential boundary prevents disclosure |
| Model repeatedly proposes the same invalid call | Attempts terminate within root budget |
| Two concurrent writes target the same balance/order | Backend enforces invariant; no double operation |
| User cancels while approval is pending | No later execution from stale approval; in-flight status handled explicitly |
| Response filter fails after successful operation | Accurate pending/completed status retained; no replayed tool action |

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

OpenAI's Agents SDK distinguishes agent-level and function-tool guardrails. Its documented blocking input mode prevents the agent from starting before the input verdict; parallel mode can allow work before cancellation. Confirm every tool path, including hosted or custom executors, against the deployed framework. [SDK guardrails](https://openai.github.io/openai-agents-python/guardrails/)

The application must still enforce backend authorization, idempotency, approvals and operation status; classifier verdicts do not replace those controls.
