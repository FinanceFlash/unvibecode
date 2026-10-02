# AI System Design — Part 2
## Serving, Cloud Architecture, and Production Reliability

## Scope

Part 1 explains how data, retrieval, structured facts, calculations, models, workflows, tools, and guardrails fit together.

Part 2 addresses the production question:

> **What must change before this architecture can safely serve real users?**

This guide covers API boundaries, cloud workloads, queues, storage, caching, scaling, provider dependencies, release controls, schema/index migrations, production failures, recovery, and readiness checks.

For deeper topic-specific implementation, use the dedicated [AI Observability](../unvibecode-ai-observability/AI_OBSERVABILITY_IMPLEMENTATION_GUIDE.md), [AI Operations](../unvibecode-ai-operations/AI_OPERATIONS_IMPLEMENTATION_GUIDE.md), [LLM Routing](../unvibecode-llm-routing/LLM_ROUTING_STRATEGY_GUIDE.md), and [Guardrails](../unvibecode_gaurdrails_implemenataion_pack/README.md) guides.

---

## 1. Production reference architecture

~~~text
                         USERS
                           ↓
                    CDN / WAF / Gateway
                           ↓
                Authentication + Quotas
                           ↓
                    Application API
                  ↙          ↓          ↘
              Cache      Orchestrator    Queue
                            ↓              ↓
                 ┌──────────┼────────┐   Workers
                 ↓          ↓        ↓      ↓
              Retrieval  SQL/API   Models  Parsing
                 ↓          ↓        ↓      ↓
              Vector DB  Data      LLMs   Indexing
                           ↓
                   Calculation Engine

                            ↓
                         Tools
                            ↓
                    External Systems

---------------------------------------------------------
          Logs / Traces / Metrics / Evaluation
---------------------------------------------------------
 IAM · Networking · Secrets · Encryption · Backups
 Reliability · Cost · Governance · Incident Controls
~~~

Do not deploy every component because the diagram contains it. Add infrastructure only when it solves a concrete task, scale, isolation, or reliability requirement.

---

## 2. API boundary

The API is a deterministic boundary around probabilistic behavior.

### Authentication and authorization

Production requirements:

- Authenticate every user or service.
- Map requests to tenant and identity.
- Authorize access to the actual resource.
- Use scoped service identities.
- Separate public, internal, and privileged/admin APIs.

Never treat identity written into a prompt as proof of identity.

---

## 3. Request validation and admission

Reject invalid or excessive work before it reaches expensive AI infrastructure.

Validate:

- request schema,
- input size,
- prompt length,
- upload size and type,
- number of documents,
- URLs,
- model/task eligibility,
- tool arguments,
- and workflow limits.

Typical explicit limits include:

~~~text
max_input_tokens
max_output_tokens
max_files
max_file_size
max_agent_steps
max_tool_calls
max_execution_time
max_cost
~~~

Provider limits are not a substitute for application limits.

---

## 4. Rate limits, concurrency, and quotas

Rate limiting protects both infrastructure and external provider capacity.

Possible dimensions:

- user,
- tenant,
- IP,
- endpoint,
- model,
- tokens per minute,
- concurrent workflows,
- and daily/monthly spend.

Expensive endpoints such as document ingestion, deep research, agents, OCR, or batch evaluation should not necessarily share the same quota as ordinary chat.

### Production failure to avoid

One customer launches a large batch and consumes the provider's shared concurrency, causing interactive traffic for every customer to time out.

---

## 5. Deadlines, retries, and cancellation

Give the complete request one overall deadline.

Example:

~~~text
Total request budget       20s
Retrieval                   2s
Structured lookup           2s
Model generation           10s
Validation                  2s
Remaining buffer            4s
~~~

Each dependency gets only part of the remaining budget.

### Retry rules

Use bounded retries with backoff and jitter for transient failures.

Do not repeatedly retry:

- authorization errors,
- invalid schemas,
- invalid tool arguments,
- oversized context,
- or deterministic business-rule failures.

Avoid retry multiplication across gateway, SDK, workflow, and worker layers.

### Cancellation

Distinguish:

- stopping display,
- cancelling generation,
- cancelling queued/background work,
- and reconciling actions already sent externally.

A closed browser connection does not automatically stop an external agent action.

---

## 6. Idempotency and reconciliation

Side effects need explicit operation identity.

Dangerous sequence:

~~~text
LLM → send invoice
             ↓
          timeout
             ↓
           retry
             ↓
      invoice sent again
~~~

Track:

~~~text
operation_id
user_id
tenant_id
resource_id
action
status
external_receipt
~~~

Before repeating an uncertain write, determine whether the previous attempt already succeeded.

Use this pattern for:

- payments,
- emails,
- orders,
- cancellations,
- provisioning,
- record updates,
- ticket creation,
- and notifications.

---

## 7. Long-running work and queues

Do not keep an ordinary request open for work that can take minutes.

Typical asynchronous jobs include:

- PDF/OCR processing,
- embedding generation,
- index rebuilds,
- large repository analysis,
- long research agents,
- and batch evaluation.

Use:

~~~text
API
 ↓
Durable queue
 ↓
Worker
 ↓
State / result store
 ↓
Status API / callback
~~~

Production requirements:

- bounded queue capacity,
- durable job identity,
- retry count,
- dead-letter handling,
- cancellation,
- expiration,
- and result retention policy.

---

## 8. Isolate workload classes

Separate interactive and heavy background work logically or physically.

Useful classes include:

~~~text
interactive inference
document ingestion
OCR / parsing
embedding / indexing
agent workflows
batch evaluation
background maintenance
~~~

A large parsing job should not consume the same worker pool needed to keep interactive requests responsive.

---

## 9. Autoscaling

Scale components using a signal related to their actual bottleneck.

| Component | Useful scaling signal |
| --- | --- |
| API server | requests / active concurrency |
| Queue worker | queue depth / job age |
| Streaming service | active connections |
| Parsing/OCR worker | backlog |
| Embedding worker | queued batches |
| Model proxy | active requests + provider quota |

CPU alone can be misleading for services mostly waiting on remote APIs.

Scaling must also respect downstream limits. Creating more workers does not help when the model provider quota is already exhausted.

---

## 10. Network boundaries

Keep internal services private where possible.

~~~text
Internet
   ↓
Gateway / Load balancer
   ↓
Application service
   ↓
Private services
   ├─ databases
   ├─ vector/index stores
   ├─ caches
   ├─ workflow services
   └─ internal tools
~~~

Control:

- internal service access,
- outbound internet access,
- allowed external destinations,
- private-address ranges,
- metadata endpoints,
- and callback/webhook URLs.

This becomes especially important when models can generate URLs.

---

## 11. Secrets and credentials

Do not place secrets in:

- prompts,
- repositories,
- model context,
- trace payloads,
- normal logs,
- or committed configuration.

Prefer:

- managed secret stores,
- short-lived credentials,
- workload identity,
- scoped tokens,
- separate development/staging/production credentials,
- and regular rotation.

A tool should receive only the permission required for that tool.

---

## 12. Storage architecture

AI applications usually have several state types.

| Store | Typical purpose |
| --- | --- |
| Object storage | Original documents/files |
| Relational DB | Users, jobs, workflow state, metadata |
| Vector/index store | Retrieval representation |
| Cache | Reusable stable results |
| Trace store | Observability |
| Evaluation store | Cases and results |
| Configuration registry | Model/prompt/index/schema versions |

Define backup, retention, deletion, and recovery requirements for each store separately.

A relational database backup does not automatically restore the vector index or source objects.

---

## 13. Caching

Caching can reduce latency and model spend but can also create stale or cross-tenant answers.

Possible caches include:

- parsed document output,
- embeddings,
- retrieval results,
- structured-data results,
- prompt prefixes,
- model answers,
- and tool/API responses.

A safe cache key may need:

~~~text
tenant
user/resource scope
query
source version
model version
prompt version
retrieval configuration
~~~

Do not use only query text for protected answers.

Every cache needs:

- TTL,
- invalidation strategy,
- version compatibility,
- permission re-checking where required,
- and a decision about whether the underlying data is safe to cache.

---

## 14. Production schema checklist for AI retrieval

Structured retrieval needs production controls beyond database connectivity.

### Schema semantics

- Use stable AI-facing names.
- Document meaning and type.
- Hide irrelevant or sensitive internal columns.
- Provide known relationships or semantic views.
- Keep ambiguous status codes and enums documented.

### Time semantics

Represent distinctions such as:

~~~text
event_time
effective_date
as_of_date
updated_at
~~~

“What is the balance?” is ambiguous if the system does not know “as of when.”

### Units

Avoid naked values such as:

~~~text
523.4
~~~

Prefer:

~~~yaml
value: 523.4
unit: USD_million
~~~

### Authority

Define the source of truth for each important field or metric.

### Metrics

Centrally define:

~~~text
metric_name
formula
required_inputs
unit
rounding_policy
formula_version
~~~

### Query controls

For model-generated or model-selected queries use:

- read-only accounts where possible,
- allowlisted tables/views,
- parser/AST validation,
- tenant filters,
- row limits,
- execution timeout,
- and audit records.

---

## 15. Model-provider abstraction

Avoid scattering provider-specific calls throughout the application.

Prefer an internal contract conceptually like:

~~~text
generate(
    task,
    messages,
    response_schema,
    deadline,
    policy
)
~~~

Provider adapters can handle:

- authentication,
- provider-specific request/response mapping,
- retryable errors,
- usage metadata,
- and routing metadata.

Do not hide meaningful capability differences. Tool calling, context limits, multimodality, schema behavior, and data-handling constraints can still vary by provider.

---

## 16. Provider failure strategy

Use a controlled progression:

~~~text
Primary route
     ↓
bounded retry
     ↓
qualified fallback
     ↓
degraded mode / queue / explicit failure
~~~

A fallback must still satisfy:

- task quality,
- context requirement,
- structured-output contract,
- tool support,
- data policy,
- and available capacity.

A model that returns HTTP 200 is not automatically an acceptable fallback.

---

## 17. Circuit breakers

When a dependency experiences sustained failure, continuing to send normal traffic can make the incident worse.

Apply circuit-breaker behavior to critical dependencies such as:

- model providers,
- web/search services,
- vector stores,
- OCR services,
- and external tools.

Use controlled probes before restoring full traffic.

---

## 18. Graceful degradation

Define degraded modes before an incident.

Examples:

### External search unavailable

Continue only with approved internal sources if the task contract permits it.

### Retrieval unavailable

If evidence is mandatory, abstain or defer instead of silently switching to unsupported model-only generation.

### Strong model unavailable

Use a smaller model only for task groups where it is already qualified.

### Action tool unavailable

Return information without performing the write, or queue the operation only when delayed execution is safe.

Graceful degradation means providing a smaller valid service, not pretending the dependency succeeded.

---

## 19. Cloud/API observability

Every request should carry a stable trace identity across:

~~~text
Gateway
 ↓
API
 ↓
Workflow
 ↓
Retrieval
 ↓
SQL / calculation
 ↓
Model
 ↓
Tool
 ↓
Response
~~~

Monitor at minimum:

- request volume,
- error rate,
- queue depth and job age,
- p50/p95/p99 latency,
- provider latency/errors,
- rate-limit responses,
- retry count,
- tool failures,
- fallback rate,
- tokens,
- and cost.

Operational success and AI quality are different dimensions. A service can return HTTP 200 while producing poor answers.

---

## 20. Deployment unit

Treat an AI deployment as a configuration bundle rather than only an application binary.

Example:

~~~yaml
release: support-assistant-2026-09-28
application: v1.8
model: model-A
prompt: support-v13
parser: parser-v4
embedding: embed-v5
index: policies-2026-09-27
retrieval_config: rag-v7
semantic_schema: finance-v3
calculation_library: metrics-v4
workflow: support-v9
guardrail: policy-v6
~~~

This makes incidents reproducible and rollback meaningful.

---

## 21. Progressive release

A useful release progression is:

~~~text
Development
    ↓
Offline evaluation
    ↓
Staging
    ↓
Shadow
    ↓
Limited canary
    ↓
Production
~~~

Define before the canary:

- acceptance criteria,
- serious/critical failures,
- evaluation version,
- rollback trigger,
- previous compatible configuration,
- and recovery owner.

Do not discover the rollback plan after a production regression.

---

## 22. Index and schema migrations

Treat retrieval/index changes as production migrations.

~~~text
Current index
     ↓
keep serving

Build new index separately
     ↓
validate parsing
     ↓
validate retrieval
     ↓
validate permissions
     ↓
switch versioned pointer
~~~

Do not destroy the active index before the replacement is qualified.

Apply the same principle to semantic-schema changes: prompts, queries, workflows, and calculation services must remain compatible during migration.

---

## 23. Production failure patterns

Most AI incidents are variations of a small number of system failures.

### 23.1 Stale state

Examples:

- stale index,
- old cache,
- obsolete document,
- old prompt against a new schema,
- old formula against current data.

**Control:** version important state and test compatibility/freshness.

### 23.2 Unbounded execution

Examples:

- agent loop,
- repeated search,
- runaway retries,
- unlimited token generation,
- tool recursion.

**Control:** cap steps, calls, retries, time, tokens, and cost.

### 23.3 Missing permission boundary

Examples:

- cross-tenant retrieval,
- generated SQL accessing unauthorized rows,
- privileged tool invoked from model output,
- broad shared credentials.

**Control:** enforce identity/resource authorization outside the model.

### 23.4 Silent quality degradation

Examples:

- new parser damages tables,
- new index reduces retrieval recall,
- model alias changes behavior,
- fallback rate increases quietly.

**Control:** quality probes, regression tests, version-aware traces, and alerts.

### 23.5 Retry amplification

Several layers independently retry the same failed dependency.

**Control:** one end-to-end attempt/deadline budget.

### 23.6 Duplicate action

A write succeeds but the client sees a timeout and repeats it.

**Control:** operation identity + idempotency/reconciliation.

### 23.7 Partial workflow completion

One external system is updated and the next step crashes.

**Control:** persisted workflow state plus explicit compensation/recovery.

### 23.8 Wrong calculation

Correct operands are retrieved but an old or wrong formula is applied.

**Control:** version formulas and log computation provenance.

### 23.9 Wrong period or unit

Examples:

- 0.18 interpreted as 0.18% instead of 18%,
- quarterly revenue compared with annual revenue,
- USD interpreted as INR.

**Control:** carry units and time semantics as data.

### 23.10 Cache leakage

An answer generated for one tenant is reused for another.

**Control:** scope-aware keys and permission re-checks.

### 23.11 Provider outage

**Control:** timeout → bounded retry → circuit breaker → qualified fallback → degraded mode.

### 23.12 Unsafe streaming

Content is displayed before required validation occurs.

**Control:** determine which checks must happen before streaming and which can operate incrementally.

### 23.13 Observability leaks sensitive data

The application masks PII before the model but stores the raw input or tool arguments in telemetry.

**Control:** redact before persistence across every logging/tracing path.

### 23.14 Unsafe configuration change

A prompt, parser, model, schema, or index update reaches all users without evaluation or rollback.

**Control:** versioned release gates and canary deployment.

---

## 24. Production failure table

| Failure | Weak response | Production design |
| --- | --- | --- |
| Model timeout | Retry indefinitely | Deadline + bounded retry |
| Provider outage | Send work to any available model | Qualified fallback |
| Retrieval unavailable | Let model answer anyway | Abstain/degrade per task contract |
| Tool times out | Repeat action | Reconcile operation ID |
| Generated SQL is wrong | Execute directly | Validate + read-only + allowlist |
| Index becomes stale | Ignore until users complain | Version + freshness monitoring |
| Queue overload | Keep accepting work | Backpressure / load shedding |
| Huge upload | Process immediately | Admission/file limits |
| Agent loops | Keep reasoning | Step/time/cost caps |
| Cache collision | Return cached answer | Tenant/version-aware keys |
| Parser regression | Re-index in place | Parallel build + qualification |
| Guardrail unavailable | Assume safe | Predefined fail-open/closed behavior |
| User cancels | Continue invisibly | Cancellation + durable state |
| Formula changes | Describe formula in prompt | Versioned calculation code |
| Model alias changes | Assume compatibility | Probes + qualification |

---

## 25. Production readiness checklist

### Data and schema

- [ ] Authoritative sources are documented.
- [ ] Freshness is measurable.
- [ ] AI-facing semantic schema exists where structured retrieval matters.
- [ ] Units, time, and source accompany critical values.
- [ ] Metrics/formulas are centrally versioned.
- [ ] Deletion propagates through derived stores.
- [ ] Tenant/resource permissions propagate into retrieval.

### Retrieval

- [ ] Parsing quality is tested.
- [ ] Retrieval has representative evaluation cases.
- [ ] Evidence includes source identity.
- [ ] Insufficient evidence has an explicit outcome.
- [ ] Index migration and rollback are tested.

### Models and workflows

- [ ] Explicit model/configuration versions are recorded.
- [ ] Structured outputs are validated.
- [ ] Workflows have hard step/time/cost bounds.
- [ ] Overall deadlines exist.
- [ ] Qualified fallback/degraded behavior exists.

### Tools

- [ ] Tool arguments are validated.
- [ ] Authorization is independent of the model.
- [ ] Write tools are separately protected.
- [ ] Side effects use operation IDs/idempotency where appropriate.
- [ ] Retry/reconciliation paths are tested.

### API and cloud

- [ ] Authentication and resource authorization are enforced.
- [ ] Request/file/token limits exist.
- [ ] Per-tenant or per-user quotas exist.
- [ ] Long-running work uses durable jobs/queues.
- [ ] Interactive and batch workloads are isolated where needed.
- [ ] Autoscaling uses workload-appropriate signals.
- [ ] Internal stores are not unnecessarily public.
- [ ] Secrets use managed/scoped credentials.

### Reliability

- [ ] Deadlines and bounded retries exist.
- [ ] Critical dependencies have circuit-breaker/fallback behavior.
- [ ] Backpressure or load shedding is defined.
- [ ] Degraded modes are documented.
- [ ] Cancellation behavior is known.
- [ ] Recovery paths have been exercised.

### Observability

- [ ] End-to-end trace IDs exist.
- [ ] Model/prompt/index/schema/formula versions are visible.
- [ ] Token and cost usage is measured.
- [ ] Tool failures and fallback usage are visible.
- [ ] p95/p99 latency is monitored.
- [ ] Telemetry has sensitive-data controls.

### Evaluation and release

- [ ] Representative regression set exists.
- [ ] Retrieval and generation are scored separately.
- [ ] Production failures are converted into test cases.
- [ ] Releases pass explicit evaluation gates.
- [ ] Canary and rollback procedures exist.
- [ ] Previous compatible configuration is retained during rollout.

---

## 26. Production incident questions

When something goes wrong, establish:

1. Which users/tasks were affected?
2. Which application, model, prompt, parser, index, schema, and formula versions were active?
3. Did the failure originate in data, retrieval, model generation, workflow, or execution?
4. Were external side effects committed?
5. Can the affected component be disabled independently?
6. Is a qualified fallback or degraded path available?
7. Can work be replayed without duplicating actions?
8. What regression test should prevent recurrence?

---

## 27. Frequently asked questions

### Do I need every component in these guides?

No. Start with the smallest architecture that satisfies the task and add complexity only when it addresses a measured need.

### Should every AI application use RAG?

No. RAG is useful for unstructured knowledge. Exact structured facts may belong in SQL or APIs.

### Should the LLM calculate numbers?

Avoid it when deterministic computation is available. Retrieve authoritative operands and calculate in SQL, Python, or a controlled service.

### Should the LLM generate SQL?

For frequent production operations, parameterized queries or semantic APIs are safer. Generated SQL can be useful for flexible analytics but should run with read-only, allowlisted, validated, bounded access.

### Can I give the model the raw production schema?

You can for small controlled analytics tasks, but production systems benefit from an AI-facing semantic layer with documented fields, units, relationships, and permissions.

### Why not use one large model for everything?

A single model is a reasonable starting point. Production routing should change only when task-specific evidence shows a quality, latency, cost, capacity, or policy benefit.

### Are prompts enough to stop dangerous tools?

No. Authorization and execution controls belong outside the model.

### Do I need Kubernetes?

Not automatically. Managed containers or serverless services can be sufficient. Adopt more infrastructure only when scaling, networking, isolation, or operational requirements justify it.

### When should I use queues?

Use durable asynchronous execution when work may outlive an interactive request, needs reliable retries, or can create a large backlog.

### Is retrying an LLM call safe?

Retrying pure generation within a bounded budget is usually easier to reason about. Retrying workflows with side effects requires idempotency or reconciliation.

### What is the difference between fallback and routing?

Routing selects an eligible model/provider during normal operation. Fallback defines behavior when the intended route cannot complete.

### Can model fallback be automatic?

Yes, but only among alternatives already qualified for the task, schema, tools, capacity, and data policy.

### Why use circuit breakers?

They prevent sustained dependency failures from turning into retry storms and cascading outages.

### How should AI responses be cached?

Include tenant/scope, relevant source versions, and configuration versions in the cache identity. Re-check permissions for protected data.

### What if retrieval is unavailable?

If evidence is required, do not silently generate an unsupported answer. Use a defined alternate retrieval path, abstain, degrade, or defer.

### How do I prevent cross-tenant RAG leakage?

Apply tenant/resource filtering before evidence reaches the model and test isolation explicitly.

### Should guardrails fail open or fail closed?

Decide per boundary. High-impact authorization/action controls normally need fail-closed behavior; low-risk informational checks may tolerate limited degradation.

### Why version parsers?

Parser changes can modify text, tables, metadata, and chunk boundaries even when the original source file is unchanged.

### Why version calculations?

A correct business answer may depend on the metric definition applicable at that time. Formula versioning makes results reproducible.

### Do observability tools need privacy controls?

Yes. Traces can contain prompts, retrieved evidence, SQL results, and tool arguments. Redact sensitive values before persistence.

### What should become a regression test?

A confirmed production failure becomes a strong regression candidate when the trigger and expected behavior can be stated reproducibly.

### What is the simplest architecture for a fresher?

Start with:

~~~text
User
 ↓
API
 ↓
Retrieval / SQL
 ↓
LLM
 ↓
Answer
~~~

Then add validation, deterministic calculations, guardrails, tools, queues, observability, routing, fallback, and evaluation only as real requirements appear.

### What is the central production principle?

> **Keep uncertainty inside bounded AI components. Authentication, permissions, state transitions, calculations, quotas, execution controls, and auditability should remain deterministic.**

---

## 28. Final mental model

When reviewing an AI system, work through five questions:

### Bound it
Can tokens, tools, retries, time, or cost run away?

### Validate it
Are evidence, arguments, permissions, schemas, calculations, and outputs checked?

### Observe it
Can the complete request and action be reconstructed?

### Evaluate it
Can you tell whether a model, prompt, parser, index, or schema change made the system better or worse?

### Recover it
Can the system degrade, rollback, reconcile, and resume safely after failure?

That is the difference between a successful AI demo and a production AI system.

Back to [Part 1: Architecture, Data, Retrieval, Models, and Deterministic Facts](./AI_SYSTEM_DESIGN_PART_1.md).
