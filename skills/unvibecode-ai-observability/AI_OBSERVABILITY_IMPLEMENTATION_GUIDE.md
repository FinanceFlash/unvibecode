# AI Observability in Production

A practical implementation guide for developers building applications with model APIs.

## 1. Understand what happened to the user's task

An AI application can return a successful API response and still fail the person using it. It might retrieve an outdated policy, block a harmless question, repeat an external action, or deliver an offensive answer. The infrastructure dashboard can stay green throughout.

Observability connects that experience to the application's behavior. When a customer says, “This answer is wrong,” you should be able to locate the response, inspect the relevant evidence, identify the responsible step, and verify a repair. You should also know when the evidence is missing.

Start with task outcomes, connected operation records, and a deliberate evidence-retention policy. Collect enough information to make decisions without turning every conversation into copies scattered across logs, traces, and evaluation systems.

### What each signal actually proves

| Signal | What it proves | What it does **not** prove |
| --- | --- | --- |
| HTTP 200 | The request returned successfully | The answer was correct or useful |
| Model call succeeded | A provider returned output | Retrieval, tools, or the final task succeeded |
| Relevant passage retrieved | Evidence was found | That evidence reached the prompt or was used correctly |
| Guardrail passed | A specific check allowed the request/output | Every policy boundary was enforced at the right time |
| Judge score is high | One evaluator rated one response highly | The business action completed or the judge is correct |
| External receipt / state | The intended external action occurred | The generated explanation was correct |

**Observability rule:** connect technical execution to **task outcome**, then keep quality and business-state evidence separate.

## 2. Know the units

| Unit | Meaning | Example |
| --- | --- | --- |
| Event | Something that happened at a time | Approval received |
| Log | Diagnostic record | Refund API timed out |
| Span | One timed operation | Retrieval or model call |
| Observation | Platform-specific activity record | Generation or evaluation observation |
| Trace | Connected operations in an execution | Retrieve policy, inspect order, request approval |
| Session | Related interactions | Conversation across several requests |
| Task | Logical work, possibly spanning traces | Refund approved tomorrow |
| Metric | Aggregate measurement | Completion rate or latency distribution |
| Evaluation | Assessment against a criterion | Answer supported by supplied evidence |
| Feedback | User-reported experience | Wrong order; offensive answer |
| Confirmed outcome | Evidence of the intended result | Payment-provider refund receipt |

These are not stages. The stages are capture, connect, collect, monitor, evaluate, investigate, and improve. A successful span, positive judge score, and completed business action establish different things.

## 3. Define success and connect the records

Define completion evidence for each task. A generated report needs a saved artifact and requirement checks. A refund needs an external receipt. A coding change needs verification tied to the patch version. Question answering needs delivery status and a separate assessment of quality.

Keep lifecycle and quality separate: an answer can be delivered successfully and still be incorrect. Use explicit states for pending, running, awaiting input, completed, failed, blocked, and cancelled. Preserve uncertain external outcomes instead of guessing success or failure.

| Identifier | Purpose |
| --- | --- |
| `task_id` | Logical work across restarts |
| `trace_id`, `span_id` | Execution and individual operation |
| `session_id` | Conversation grouping |
| `response_id` | Exact answer version, including regeneration |
| `operation_id` | Intended external action across retries |
| `attempt_id` | Individual execution attempt |
| `release_id` | Application configuration |

Propagate identity through queues and background workers. Connect resumed traces with task IDs and trace links where appropriate. Never treat knowledge of an identifier as authorization to read its records.

Define denominators: quality among evaluated answers differs from completion among started tasks. For long-running work, distinguish overdue tasks from recently started work.

## 4. Implement a small observability pipeline

Use the existing application database for tasks, messages, feedback, and receipts; one telemetry backend for metrics and traces; and restricted object storage only when large evidence requires it. Run quality evaluation asynchronously unless a check must prevent an unsafe response or action.

~~~mermaid
flowchart TD
    A["Application"] --> B["Task + response records"]
    A --> C["Bounded telemetry export"]
    C --> D["Metrics + traces"]
    B --> E["Protected evidence"]
    B --> F["Async evaluation worker"]
    E --> F
    F --> D
    D --> G["Incident investigation"]
    E --> G

    classDef app fill:#e0f2fe,stroke:#0284c7,color:#111827;
    classDef record fill:#eef2ff,stroke:#6366f1,color:#111827;
    classDef telemetry fill:#fff7ed,stroke:#ea580c,color:#111827;
    classDef evidence fill:#f5f3ff,stroke:#7c3aed,color:#111827;
    classDef eval fill:#ecfdf5,stroke:#059669,color:#111827;
    classDef incident fill:#fef2f2,stroke:#dc2626,color:#111827;
    class A app;
    class B record;
    class C,D telemetry;
    class E evidence;
    class F eval;
    class G incident;
~~~

OpenTelemetry supplies conventions and collection components. Langfuse and LangSmith provide AI evaluation and trace workflows [1, 5, 6]. Your application still defines task success, permissions, and authoritative execution records.

### Capture each meaningful boundary

| Component | Record |
| --- | --- |
| Model and router | Every attempt, requested/returned model identity where available, fallback reason, usage, finish reason |
| Parsing and ingestion | Parser version, source version, extraction checks, index version and freshness |
| Retrieval and context | Retrieved IDs, selected passages, omitted evidence, access-filter outcome |
| Agent and memory | Assignment, handoff, termination reason, memory revisions, compaction version |
| Tool | Validated action reference, operation and attempt IDs, external receipt |
| Guardrail | Policy version, decision, execution status, enforcement result |
| Evaluation | Criterion, evaluator version, exact response ID, score and execution status |

Measure first-token, completed-response, and task-outcome latency separately. Aggregate task cost across retries, tools, checks, and evaluations. Label estimated costs; missing usage is unknown, not zero. Do not claim an immutable model revision when the provider exposes only an alias.

## 5. Production failures and how to detect them

Before reading individual cases, start with the failure class:

| Symptom | First place to inspect |
| --- | --- |
| “The answer is wrong” | source/version → retrieval → supplied context → model route |
| “The action happened twice” | operation ID → external receipt → retry/reconciliation path |
| “The agent says no data” | tool status → timeout/error → successful-empty distinction |
| “Everything is suddenly blocked” | guardrail policy version → fallback → benign-block sample |
| “Quality improved overnight” | evaluation coverage → judge/rubric version → missing failures |
| “Tracing looks healthy but users complain” | task outcome + exact response evidence, not span success alone |

### Infrastructure and telemetry

**The incident erases its own evidence.** A traffic spike fills exporter queues, dropping the traces needed for diagnosis. Monitor queue occupancy, oldest item, export failures, dropped records, disk capacity, and ingestion lag. Reconcile received traces against expected sampled volume. Test a backend outage under load. Persistent queues improve resilience but can still lose data through capacity exhaustion or retry expiry [2, 4].

**Background work disappears from the trace.** An HTTP request ends while an agent continues in another worker. Pass task identity and tracing context through the queue; link resumed execution explicitly. Test a worker restart and verify the complete task remains discoverable.

### Models and routing

**Fallback hides the failed attempts.** The final model succeeds, so the dashboard omits two earlier calls and understates cost. Record attempts separately and aggregate at task level. Force provider failure and verify that all attempts remain visible.

**Streaming looks fast but never finishes.** First-token latency is healthy while tools stall or the client disconnects. Track completion, cancellation, and continuing backend work. Test cancellation during a tool operation; a closed browser must not be interpreted as a cancelled external action.

### RAG and upstream data

**Ingestion succeeds with corrupted content.** A parser rearranges table columns or drops footnotes. File-level success hides downstream factual errors. Add extraction checks by document type and retain parser/source versions. Test a known difficult table or scan.

**Retrieval finds the answer, but the prompt loses it.** Reranking, truncation, or context assembly excludes the decisive passage. Compare retrieved and actually supplied evidence. Test by deliberately dropping a required passage after retrieval.

**Search returns an obsolete or inaccessible source.** A stale index or missing authorization filter produces plausible evidence. Record index freshness and source versions; enforce permissions before supplying content. Test source updates, deletion propagation, and cross-tenant isolation.

### Agents, tools, and memory

**Every worker succeeds while the task remains incomplete.** Researchers return sources and a writer produces fluent text, but a required question is unanswered. Evaluate against the original task contract. Test a deliberately omitted requirement.

**A timeout creates a duplicate action.** The external system commits before local confirmation. Keep a durable operation ID, use supported idempotency, and reconcile uncertain outcomes. Crash between remote success and local receipt; confirm one intended action, not two.

**Old memory survives a correction.** A background writer restores a superseded requirement. Record source revisions and reject obsolete writes. Race a correction against extraction and inspect the selected memory version.

### Guardrails

**An error is recorded as permission.** A check times out and the fallback allows execution. Separate allow, block, timeout, error, and skipped states; record fallback behavior. Test each failure mode on every relevant route.

**The check detects harm too late.** Offensive text is streamed or a file is sent before the checker finishes. Compare check completion with emission or action timing. Prevent consequential actions through pre-execution enforcement; later evaluation cannot undo them.

**Block rate rises while usefulness falls.** The policy rejects legitimate requests. Review benign blocks and harmful allowed outputs separately. Include nearby benign cases when testing a safety repair. NeMo exposes logs, traces, and metrics for examining these decisions [7].

### Evaluations and releases

**Quality improves because failures are missing.** Timeouts and failed evaluator jobs never receive scores. Report coverage, evaluation errors, and lag alongside quality. Inject evaluator failures and confirm they are not counted as passes.

**A new judge creates a fake improvement.** Scores change because the rubric or evaluator model changed. Version both and compare them on a fixed reviewed calibration set before joining trends.

**Offline tests pass in a contaminated environment.** An earlier trial created the required file or database row. Reset fixtures and verify actual outcomes. Test narration alone cannot establish agent success [9].

**Rollback restores code but breaks resumed work.** New checkpoints or index schemas are incompatible with the old application. Version state and data dependencies; test rollback with active tasks, not only fresh requests.

### Evidence and storage

**Masked prompts leak through another path.** Automatic tracing captures raw input before redaction, or the evaluator exports it again. Test the entire input-to-export path with synthetic sensitive markers. Apply masking before the relevant export boundary [8].

**Evidence expires before the complaint arrives.** Metadata cannot reconstruct the exact offensive answer. Match retention to reporting delays, record expiry explicitly, and provide a customer-supplied evidence path.

## 6. Retain evidence without duplicating conversations

Store the delivered answer once in the conversation or restricted evidence store. Reference it from traces, feedback, and evaluations. Keep raw model output separately only when needed to distinguish generation from postprocessing.

For streaming, retain emitted content and termination status where permitted. Emission does not prove what the browser rendered; client acknowledgments can strengthen delivery evidence. Hashes verify identity but cannot reconstruct missing text.

| Tier | Example policy | Access |
| --- | --- | --- |
| Operational metadata | 30 days searchable | Appropriate engineering roles |
| Conversation evidence | 7–14 days or existing product retention | Authorized support/investigators |
| Verbose diagnostics | Short retention; sampled | Restricted engineering access |
| Incident evidence | Defined investigation period with review | Assigned investigators |
| Aggregate metrics | Longer retention with bounded dimensions | Operational reporting |

These durations are planning examples. Choose an investigation window from customer reporting delays and applicable requirements. For zero-content-retention customers, rely on metadata and customer-submitted evidence. An incident flag must not silently override that agreement.

OpenTelemetry recommends opt-in capture for sensitive message content [1]. Redact unnecessary identifiers without erasing wording necessary for authorized investigation. Restrict and audit access. Propagate deletion to evaluator copies, exports, caches, and indexes; apply backup retention policies.

## 7. Handle a harmful-answer complaint

A complaint investigation should follow the evidence, not start by regenerating the answer.

~~~mermaid
flowchart TD
    A["Customer complaint"] --> B["Locate exact response_id"]
    B --> C{"Original evidence available?"}
    C -->|Yes| D["Inspect wording + context + sources"]
    C -->|No| E["Request customer evidence<br/>and record evidence gap"]
    D --> F["Check model route + source versions<br/>+ guardrail timing + fallback"]
    F --> G["Contain affected behavior"]
    G --> H["Repair responsible component"]
    H --> I["Add regression case + verify release"]
    E --> G

    classDef complaint fill:#fef2f2,stroke:#dc2626,color:#111827;
    classDef inspect fill:#e0f2fe,stroke:#0284c7,color:#111827;
    classDef decision fill:#fff7ed,stroke:#ea580c,color:#111827;
    classDef repair fill:#ecfdf5,stroke:#059669,color:#111827;
    class A complaint;
    class B,D,F inspect;
    class C,E decision;
    class G,H,I repair;
~~~

When a customer reports a racist answer, locate the exact response ID, including its regeneration version. Preserve the necessary available evidence under the customer's retention policy, with an owner and review deadline. Inspect the wording and relevant context: was the material generated, quoted, retrieved, or introduced during transformation? Check the model route, source versions, guardrail result, timeout fallback, and whether text was emitted before checking finished. A passed automated check does not invalidate the complaint.

Contain the affected behavior based on the evidence, repair the responsible component, and verify the result. If content has expired, request the message or screenshot and document the limitation. A fresh model response may support an investigation, but cannot prove what the user originally received.

## 8. Bound the cost and failure impact of logging

Estimate volume before increasing retention:

```text
Daily bytes ≈ requests × (metadata bytes + sampling fraction × diagnostic bytes)
              + retained evidence bytes
```

For example, 100,000 requests with 2 KB metadata produce approximately 200 MB/day before overhead. Sampling 1% with 100 KB diagnostics adds approximately 100 MB/day. Account separately for indexes, compression, replicas, and retention. These are arithmetic assumptions, not vendor sizing guarantees.

Use bounded queues, retry limits, payload limits, and tenant quotas. Batch ordinary exports asynchronously. Avoid document binaries and repeated prompts in spans. Index necessary metadata rather than every payload. Keep unique request IDs out of metric labels; use them in protected traces.

Define overflow behavior. Drop lower-priority diagnostics before exhausting application memory, and count the drops. Mandatory audit and transaction records need a separately designed durable path and explicit failure policy. OpenTelemetry documents queue, disk, retry, and collector failure limits [2].

Sample ordinary detailed traces and preferentially retain detected failures. Keep a representative sample for population estimates. Do not combine an oversampled incident cohort into the overall failure rate without appropriate weighting. Tail sampling can use later trace information, but cannot recover content discarded before a complaint days later [3]. If every answer must remain investigable during a defined window, retain those answers in the protected store and sample surrounding diagnostics.

## 9. Connect online evaluation, offline tests, and maintenance

Use exact checks for schemas, required fields, artifact existence, and confirmed outcomes. Use calibrated model judgments and human review for interpretation. Citation presence alone does not establish support.

Track the evaluation funnel:

~~~mermaid
flowchart LR
    A["Eligible"] --> B["Selected"]
    B --> C["Queued"]
    C --> D["Completed"]
    D --> E["Valid score"]
    E --> F["Reviewed failure"]
    C -. timeout / error .-> X["Evaluation failure"]
    D -. invalid result .-> X

    classDef stage fill:#e0f2fe,stroke:#0284c7,color:#111827;
    classDef score fill:#ecfdf5,stroke:#059669,color:#111827;
    classDef failure fill:#fef2f2,stroke:#dc2626,color:#111827;
    class A,B,C,D stage;
    class E,F score;
    class X failure;
~~~

Store request time and evaluation time separately. Show completeness and lag beside quality. Langfuse supports production filters and sampling rules [5]; version their configuration. Test judge length bias and attempts within evaluated content to override the rubric.

Maintain a stable regression dataset and a refreshed production dataset. Separate development from held-out cases, reset trial state, and repeat stochastic cases where variability affects decisions. Gate important task groups and critical failures separately from averages. Backtesting historical inputs requires deciding whether source versions should represent the original environment or current knowledge [6].

### What should become a regression test?

A confirmed failure should become a regression test when you can state the expected behavior and reproduce the conditions that exposed it. Preserve a sanitized input, necessary source or state versions, and a checkable outcome: a harmful answer must be blocked before emission, an outdated policy must be excluded, or a retried operation must not create a duplicate action. Include nearby legitimate cases when a repair could cause excessive blocking. Use a focused component test for a local defect and an end-to-end test when the failure crosses retrieval, memory, guardrails, tools, or delivery boundaries. If the original incident cannot be reproduced, retain it for investigation and create clearly identified representative cases; do not claim they reproduce the original failure. Keep production monitoring for recurrence after the test passes.

Attach release references for application, prompt, model configuration, routing, parser, index, memory policy, tools, guardrails, instrumentation, and evaluators. Record unavailable versions rather than claiming perfect reproducibility. Shadow runs must isolate external writes. Canary comparisons need comparable traffic and sufficient observation time.

Use a small set of dashboard views rather than one giant AI dashboard:

| View | Primary question |
| --- | --- |
| Task outcomes | Are users' tasks actually completing? |
| Quality / safety | Are answers supported, useful, and within policy? |
| Latency / cost | Where are time and money being spent? |
| Telemetry / evaluator health | Are we losing traces or silently missing scores? |
| Releases / incidents | Did behavior change with a model, prompt, parser, index, or policy release? |

Give alerts an owner, evidence link, severity, and response procedure. Escalate urgent harmful actions promptly; investigate slower quality trends without paging on every individual judge failure.

## 10. Implementation checklist

| Deliverable | Acceptance test |
| --- | --- |
| Task outcome contract | HTTP success does not imply verified task success |
| Connected identifiers | Resumed work remains linked to the original task |
| Boundary instrumentation | Forced fallback exposes every attempt |
| Protected evidence and complaint path | Authorized support finds the exact answer; other tenants cannot |
| Bounded export and retention | Backend outage does not exhaust memory; drops are visible |
| Evaluation coverage and calibration | Failed evaluations remain unknown, not passed |
| Versioned release gates | A deliberate regression blocks the relevant gate |
| Incident ownership | Confirmed failures become tests and verified repairs |

## 11. Frequently asked questions

**Should we store every prompt forever?** No. Define the investigation window and retain necessary evidence once. Keep routine telemetry lightweight.

**Can we investigate without content?** Metadata explains execution, but cannot establish expired wording. Request customer evidence and state the gap.

**Are traces sufficient for payments or approvals?** No. Sampled traces cannot replace durable business records.

**Should every answer receive a model judge score?** Only if justified. Begin with exact checks, representative sampling, and targeted risk cases; track coverage and evaluator errors.

**Can a judge be wrong?** Yes. Calibrate against reviewed examples and version the rubric and model. Scores inform investigation rather than deciding incidents automatically.

**Do we need Kafka immediately?** No. Begin with bounded export and suitable persistence. Dedicated queues improve some durability properties while introducing operating complexity [2].

**How do we attribute a model regression?** Compare controlled versions and traffic groups; inspect simultaneous retrieval, prompt, policy, and evaluator changes.

**What is the minimum useful setup?** Task outcomes, connected operation records, response evidence references, versions, a complaint path, and visible telemetry losses.

## References

1. OpenTelemetry. [Generative AI span conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md).
2. OpenTelemetry. [Collector resiliency](https://opentelemetry.io/docs/collector/resiliency/).
3. OpenTelemetry. [Sampling](https://opentelemetry.io/docs/concepts/sampling/).
4. OpenTelemetry. [Collector internal telemetry](https://opentelemetry.io/docs/collector/internal-telemetry/).
5. Langfuse. [Evaluate production traffic](https://langfuse.com/docs/evaluation/get-started/online).
6. LangSmith. [Evaluation types and backtesting](https://docs.langchain.com/langsmith/evaluation-types).
7. NVIDIA NeMo Guardrails. [Observability overview](https://docs.nvidia.com/nemo/guardrails/latest/observability/index.html).
8. Langfuse. [Masking](https://langfuse.com/docs/observability/features/masking).
9. Anthropic. [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents). January 9, 2026.
