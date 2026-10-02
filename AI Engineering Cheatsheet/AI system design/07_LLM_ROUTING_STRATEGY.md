# LLM Routing: Evaluate Offline, Then Route Selectively Online

*A practical guide to mixing hosted open-weight and closed models without turning routing into another fragile AI system.*

## Why a hybrid mix of models usually makes sense

Once an AI product grows beyond one feature, it is unusual for every request to need the same model.

Some tasks are simple and repetitive: classify an intent, extract fields, rewrite text, or validate a schema. Others need stronger reasoning: understand a large repository, reconcile conflicting documents, diagnose an incident across services, or recover a long-running agent after a partial failure.

Using the strongest model for everything can work, but it often means paying high latency and cost for work that a smaller model handles just as well. The opposite strategy—forcing every task through the cheapest model—usually creates retries, escalations, and failures that erase the apparent savings.

A practical production architecture is therefore **hybrid**:

- use small, fast models for tasks they reliably pass;
- use stronger models where additional capability measurably improves outcomes;
- use specialist or open-weight models where modality, privacy, deployment, or cost makes them a better fit;
- use learned decision models such as **Jev or Laya** for bounded intent classification when useful;
- keep deterministic code for permissions, calculations, and operations that do not need a model.

The goal is not to find one universally “best” model. It is to build a **small qualified model pool** where each model has a job it has demonstrated it can perform.

| Task | Possible allocation |
| --- | --- |
| Intent / topic classification | Jev, Laya, small classifier, or small LLM |
| Field extraction | Small/medium structured-output model |
| Routine RAG Q&A | Mid-cost model |
| Complex multi-document synthesis | Strong reasoning model |
| Repository-wide architecture analysis | Strong long-context/coding model |
| Simple answer verification | Small evaluator / learned decision model |
| High-impact ambiguous case | Strong model or human review |

This is ordinary system design applied to models: choose the smallest component that satisfies the requirement with enough reliability.

> **Evaluate models offline, assign each task to the smallest qualified option, and make routing more dynamic only when the added complexity creates measured value.**

---

## 1. Start with model allocation, not a complicated router

The first routing decision happens offline: determine which models are suitable for each task.

Runtime routing should implement that policy, not invent it from scratch on every request.

The objective is to minimize **total cost per successful task** while satisfying:

- quality,
- critical-error limits,
- latency,
- reliability,
- tool/schema compatibility,
- context requirements,
- and data-handling constraints.

Separate three decisions:

| Decision | Question |
| --- | --- |
| Workflow selection | Does this need RAG, calculation, code execution, generation, or an action workflow? |
| Model allocation | Which approved model should perform this task or step? |
| Provider selection | Which approved endpoint should serve that model? |

Start with a small pool and a fixed task-to-model mapping. Add learned routing, cascades, or parallel candidates only after they beat that baseline.

---

## 2. Describe tasks using separate dimensions

Do not collapse everything into a single “easy / medium / hard” label.

| Dimension | Example | Why it matters |
| --- | --- | --- |
| Business task | Code review, invoice extraction, policy Q&A | Defines the outcome |
| Operation | Classification, extraction, reasoning, verification, tool execution | Helps choose model/evaluator |
| Execution structure | Single call, fixed pipeline, agent workflow | Determines response vs trajectory evaluation |
| Answer structure | Label, JSON, free text, multiple valid answers | Determines scoring |
| Difficulty signals | Conflicting evidence, many dependencies, strict schema | May justify stronger allocation |
| Error consequence | Draft vs external write | Determines thresholds and controls |
| Serving need | Deadline, modality, privacy, tool support | Filters eligible models/providers |

Risk is not the same as difficulty. A one-field update may be easy to understand but consequential if executed incorrectly.

### Build a useful task taxonomy

Split tasks when they genuinely need different models, evaluators, tools, or controls.

| Family | Typical tasks | Evaluation emphasis |
| --- | --- | --- |
| Coding | generation, repair, review, repository understanding | executable behavior, regressions, evidence |
| Documents | extraction, transformation, report creation | field accuracy, fact preservation, completeness |
| Knowledge / RAG | lookup, synthesis, contradiction resolution | correctness, support, abstention |
| Classification | intent, urgency, topic, out-of-scope | accuracy, macro-F1, critical-class recall |
| Data | SQL, calculations, reconciliation | execution, numerical invariants |
| Agents | research, record updates, transactions, recovery | final state, forbidden effects, repeated-run success |
| Multimodal | scans, images, video | modality-specific labels and task outcomes |

Keep observable tags such as `conflicting_sources`, `long_context`, `strict_schema`, or `external_write`. Validate that they actually predict failures before using them in a router.

---

## 3. Evaluate models by task before routing them

A router is only as good as the evidence behind its allocation policy. For the broader evaluation methodology, see [Evaluation Engineering](./06_EVALUATION_ENGINEERING.md).

### Match evaluation to the task

| Task | Useful measurement |
| --- | --- |
| Classification | accuracy, macro-F1, critical-class recall |
| Extraction | field accuracy, whole-record accuracy |
| Grounded Q&A | correctness, evidence support, abstention |
| Long context | task accuracy by context length/slice |
| Code | executable success and regressions |
| Tool calling | function + argument correctness |
| Agent workflow | final state, prohibited actions, recovery |
| Architecture/specification | constraint coverage, contract validity, expert-calibrated rubric |

Prefer deterministic checks and execution where they measure the requirement directly.

### Define an evaluation contract

For each task record:

- input and initial state,
- allowed evidence/tools,
- required outcome,
- serious failure conditions,
- primary metric,
- diagnostic metrics,
- token/time/retry budget,
- scorer version,
- model/provider/prompt versions.

A serious error should remain visible even when average quality is high.

### Build a per-case model matrix

Store outcomes by case rather than only aggregate averages:

```text
case_id
task
difficulty_tags
consequence_level
model
provider
pass / fail
failure_type
cost
latency
```

This shows where models have complementary strengths.

### Compare policies, not just models

Evaluate on the same holdout:

1. strongest fixed model,
2. cheapest qualifying fixed model,
3. fixed task-to-model mapping,
4. proposed dynamic router,
5. cascade if applicable.

A dynamic router is useful only if the **whole policy** improves the quality–cost–latency trade-off.

---

## 4. Run the offline selection process

1. **Set acceptance criteria first.** Define task success, critical errors, latency limits, and budget.
2. **Build representative cases.** Include normal traffic, edge cases, missing information, and known failures.
3. **Keep a holdout.** Do not train the router or tune thresholds on the final comparison set.
4. **Evaluate candidate configurations.** Record model, provider, prompt, tools, inference budget, and evaluator versions.
5. **Compare per-case results.** Look for predictable subgroups where one model clearly outperforms another.
6. **Evaluate full workflows.** A cheap first step may create expensive downstream repair.
7. **Publish a versioned allocation policy.** Define primary model, eligibility conditions, escalation, deadlines, and stop behavior.

Use quality-versus-cost curves instead of one leaderboard rank.

If two policies perform within measurement uncertainty, prefer the simpler one.

---

## 5. Choose a runtime routing strategy only when it solves a real problem

| Strategy | Use when |
| --- | --- |
| Fixed task mapping | Application already knows the task |
| Intent classification | Request is free-form and task must be identified |
| Learned quality router | Same task varies substantially in model difficulty |
| Verification cascade | Cheap model fails detectably and escalation is affordable |
| Workflow-step allocation | Different steps need different strengths |
| Best-of-n | Multiple inexpensive samples measurably beat one expensive call |
| Provider failover | Same qualified model needs endpoint redundancy |

### Intent classification: where Jev and Laya fit

If your application already knows that a request came from `/invoice-extraction`, you do not need an intent router.

If users enter free-form requests such as:

> “I was charged twice and need this fixed”

you may need a bounded intent decision:

```text
billing
refund
technical_support
account_access
unknown
```

Options include:

- application rules,
- small fine-tuned classifiers,
- embedding / semantic routers,
- a small LLM,
- **TypeSafe AI Jev**,
- **Laya**.

Jev and Laya are useful when the output is a **closed decision space**, not free-form generation.

Conceptually:

```text
request
  ↓
choice(
  billing,
  refund,
  technical_support,
  account_access,
  unknown
)
  ↓
probability per option
  ↓
routing policy
```

Laya supports bounded typed decisions for routing and intent-style classification. As with any learned classifier, validate labels, languages, confidence behavior, and unknown-intent handling on your own traffic.

TypeSafe's Jev similarly exposes bounded typed decisions such as `Choice`, `Score`, and `Noul`, making it suitable for low-latency semantic classification where you want probabilities rather than generated prose.

Do not treat classifier confidence as proof that the downstream model will succeed. Evaluate:

**intent classification accuracy** separately from **model-answer success**.

Always retain an `unknown`, clarification, or safe-default route for inputs that do not fit the taxonomy.

### Cascades

A two-stage cascade costs approximately:

**cheap attempt + checker + escalation rate × strong attempt**

The cheap path is worthwhile only if:

- the cheap model passes enough cases,
- failures can be detected reliably,
- escalation stays reasonably low,
- and sequential latency is acceptable.

If 80% of requests escalate, direct routing to the strong model may be simpler and cheaper.

---

## 6. Which routing approach should a developer actually use?

You usually do **not** need a routing framework on day one.

Start here:

```text
Does the app already know the task?
    ├─ yes → fixed task mapping
    └─ no
       ↓
Is it a bounded intent/category decision?
    ├─ yes → Jev / Laya / classifier / Semantic Router
    └─ no
       ↓
Do models have measurable complementary strengths?
    ├─ no → use the simplest qualified fixed model
    └─ yes → test learned router or cascade
```

### Practical options

| Option | Good fit | Do not assume |
| --- | --- | --- |
| Application rules | Endpoint/task metadata already identifies work | Every free-form request fits deterministic rules |
| **Jev** | Fast bounded semantic decisions with typed probabilities | Probability equals downstream model success |
| **Laya** | Local/open learned intent and typed decisions | High confidence is automatically calibrated for your traffic |
| **Semantic Router** | Example/embedding-based intent grouping | Semantic similarity predicts answer quality |
| **RouteLLM** | Experimenting with strong-vs-weak learned allocation | Pretrained routing policy transfers to your workload |
| **LLMRouter** | Comparing many routing algorithm families | You need all those algorithms in production |
| **BEST-Route** | Testing model choice plus best-of-n compute allocation | Reward-model score equals application success |

### A simple rule of thumb

Use **Jev/Laya/classification** when the question is:

> “What kind of request is this?”

Use **RouteLLM-style quality routing** when the question is:

> “Which of these qualified models is likely to succeed on this request?”

Use **provider routing** when the question is:

> “Which endpoint should serve the already-selected model?”

These are different decisions. Keeping them separate makes the system easier to debug.

---

## 7. Production system design

A useful runtime path is:

```text
Request
  ↓
Task / intent identification
  ↓
Eligibility filter
  ↓
Versioned model policy
  ↓
Provider adapter
  ↓
Execution
  ↓
Task-specific validation
  ↓
Telemetry + regression loop
```

### Eligibility comes before preference

Before choosing the “best” model, remove models/providers that cannot safely serve the request.

Check:

- modality,
- context length,
- tool support,
- required parameters/schema,
- data policy,
- tenant restrictions,
- destination restrictions,
- current availability.

Then select among the remaining qualified options.

### Keep routing separate from authorization

A router can select a model.

It cannot authorize:

- a payment,
- an email,
- a database write,
- a production deployment,
- or access to protected data.

Those controls remain deterministic application responsibilities.

### Measure the policy in production

Track:

- selected task/intent,
- selected model/provider,
- classification confidence where relevant,
- fallback/escalation reason,
- first-attempt success,
- final task success,
- cost per successful task,
- p95 latency,
- critical failures,
- router overhead.

For offline counterfactual analysis, run alternative qualified models on the same cases. Production logs from only the selected model cannot tell you every over-routing or under-routing error.

---

## 8. Critical production routing failures

### 1. Unknown intent is forced into the nearest known route

A user asks for something outside the taxonomy. The classifier still chooses `billing` with the highest probability, so the request reaches a workflow that was never designed for it.

This is especially dangerous when the route can trigger tools.

**Control:** Include an `unknown` / clarify path and test out-of-scope traffic explicitly.

**Test:** Send unrelated, ambiguous, multilingual, and mixed-intent inputs. The router should not be forced to choose a business workflow when evidence is weak.

---

### 2. A “cheap first” cascade becomes two model calls for almost every request

The small model fails often enough that the strong model is called anyway.

You now pay:

**small model + checker + strong model**

while also increasing p95 latency.

The dashboard may still look good if it reports only final answer quality.

**Control:** Track escalation rate, first-attempt success, total cost per successful task, and end-to-end latency.

**Test:** Compare the complete cascade against direct strong-model routing on the same holdout. Remove the cascade if it does not create a meaningful gain.

---

### 3. Provider failover silently changes capability or policy

The primary model endpoint fails. The gateway moves traffic to another provider or model that does not support the same tool schema, context size, structured output, or data-handling requirement.

HTTP availability is restored, but application behavior is wrong.

**Control:** Build failover only among pre-qualified endpoints. Apply eligibility checks before fallback.

**Test:** Fail the primary provider while running long-context, structured-output, tool-calling, and restricted-data cases. The fallback must preserve the task contract or fail explicitly.

---

### 4. Model switching breaks a long-running conversation or agent

A workflow begins with one model, then the router changes models halfway through because load, cost, or classification changed.

The new model interprets tool history differently, has another context limit, or behaves differently around structured outputs. A previously valid agent state becomes unreliable.

**Control:** Prefer session/workflow affinity. Switch models only at explicit boundaries where state can be validated and normalized.

**Test:** Pause an active workflow, switch to the fallback model, resume, and verify tool-message compatibility, pending operations, context, and output schema.

---

## 9. Worked example: routing a repository assistant

Suppose a repository assistant supports three tasks:

| Task | Nature | Evaluation |
| --- | --- | --- |
| Find refund-limit validation | repository lookup, read-only | gold file/symbol/evidence |
| Fix rounding bug | bounded code modification | hidden rounding + regression tests |
| Diagnose duplicate refunds | multi-service reasoning, high consequence | seeded incident + causal evidence + forbidden actions |

Assume offline evaluation shows:

- Model A qualifies for lookup and narrow fixes.
- Model B is needed for cross-service diagnosis.

The first policy is simple:

```text
lookup           → A
narrow code fix  → A
incident         → B
```

If the application already knows the task, no semantic classifier is needed.

If the user enters free-form instructions, use a bounded intent classifier such as Jev, Laya, or another validated classifier:

```text
repository_lookup
code_change
incident_diagnosis
unknown
```

Then apply the versioned allocation policy.

For narrow fixes, you may test an optional cascade:

```text
A generates patch
   ↓
tests / validator
   ↓
pass → return
fail → one escalation to B
```

Evaluate the complete cascade. If tests frequently send work to B anyway, direct B routing may be better.

Provider outage and quality failure remain separate:

- **provider outage** → approved provider failover;
- **patch fails tests** → quality escalation;
- **missing repository context** → retrieval repair;
- **budget exhausted** → stop.

Routing never authorizes production deployment.

---

## 10. Frequently asked questions

### How many models should I start with?

Usually two or three are enough to establish whether routing creates value.

A common starting point is:

- one cheap/general model,
- one stronger model,
- optionally one specialist model.

A large model catalog makes evaluation and operations harder.

### Do I need a router if my application already knows the task?

No.

If the endpoint or workflow already identifies the task, use that metadata directly. Classification adds latency and another failure mode without adding information.

### When would I use Jev or Laya instead of an embedding-based semantic router?

Use Jev/Laya when you want a learned **bounded decision over named choices**, often with probabilities.

Use embedding routing when similarity to route examples is a good representation of intent.

Evaluate both on boundary cases, unknown requests, languages, and mixed intents.

### Can I route purely on classifier confidence?

Not safely unless you have calibrated that confidence on your own traffic.

A classifier can be highly confident and still be systematically wrong on an unseen language, domain, or request type.

Use confidence together with validation data, an unknown route, and task risk.

### Should the strongest model handle every high-risk task?

Not automatically.

Risk determines controls and acceptance thresholds. Capability determines model allocation.

An easy but high-impact action may still use a small model for interpretation while deterministic authorization and execution controls protect the action.

### When does a cascade make sense?

When the cheap model succeeds frequently, its failures are detectable, and escalation is relatively rare.

If failure detection is weak or escalation is common, use direct routing.

### What is the difference between provider fallback and quality escalation?

**Provider fallback** responds to serving failure: outage, quota, timeout.

**Quality escalation** responds to task failure: invalid schema, failed test, insufficient evidence, low validated confidence.

Do not treat them as the same mechanism.

### Can the LLM route requests by prompting itself?

Yes, but that is still another model decision to evaluate.

For small bounded taxonomies, a classifier/Jev/Laya-style decision may be cheaper and easier to measure. For complex task understanding, an LLM classifier may be appropriate.

Compare accuracy, latency, cost, and unknown-intent behavior.

### Should I switch models inside a running agent?

Prefer not to unless there is a clear boundary.

If you must switch, validate state, tool history, schema compatibility, context limits, and pending external operations first.

### How do I know whether routing actually saves money?

Measure **cost per successful task**, not price per token.

Include:

- classifier/router cost,
- failed cheap attempts,
- checker cost,
- escalations,
- retries,
- tool calls,
- and downstream repair.

### What are the core router metrics?

Track:

- task success,
- serious-error rate,
- under-routing,
- over-routing,
- escalation rate,
- first-attempt success,
- total cost per success,
- p95 latency,
- router/classifier error rate.

### How often should routing policies be re-evaluated?

Re-evaluate when:

- a model/provider changes,
- prompts/tools change,
- new task types appear,
- traffic distribution changes,
- failure patterns shift,
- or a cheaper/stronger candidate becomes available.

Keep the policy versioned so incidents can be reproduced and rolled back.

---

## References

1. [OpenRouter Auto Router](https://github.com/OpenRouterTeam/docs/blob/main/guides/routing/routers/auto-router.mdx)
2. [LM Evaluation Harness task configuration](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/task_guide.md)
3. [LM Evaluation Harness API guide](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/API_guide.md)
4. [Scikit-learn metrics](https://github.com/scikit-learn/scikit-learn/tree/main/sklearn/metrics)
5. [CLINC out-of-scope evaluation](https://github.com/clinc/oos-eval)
6. [LongBench](https://github.com/THUDM/LongBench)
7. [IFEval](https://github.com/google-research/google-research/tree/master/instruction_following_eval)
8. [LiveCodeBench](https://github.com/LiveCodeBench/LiveCodeBench)
9. [SWE-bench](https://github.com/SWE-bench/SWE-bench)
10. [Berkeley Function Calling Leaderboard](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard)
11. [τ-bench](https://github.com/sierra-research/tau2-bench)
12. [RouteLLM](https://github.com/lm-sys/RouteLLM)
13. [LLMRouter](https://github.com/ulab-uiuc/LLMRouter)
14. [BEST-Route / HybridLLM](https://github.com/microsoft/best-route-llm)
15. [Semantic Router](https://github.com/aurelio-labs/semantic-router)
16. [Laya](https://github.com/NandhaKishorM/laya)
17. [TypeSafe AI / Jev](https://typesafe.ai/)
18. [OpenRouter provider selection](https://github.com/OpenRouterTeam/docs/blob/main/guides/routing/provider-selection.mdx)
19. [OpenRouter model fallbacks](https://github.com/OpenRouterTeam/docs/blob/main/guides/routing/model-fallbacks.mdx)
