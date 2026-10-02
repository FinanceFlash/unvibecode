# LLM routing: evaluate offline, then route selectively online

*A practical guide to mixing hosted open-weight and closed models. Sources checked 26 September 2026. The task taxonomy and implementation recommendations below are proposed design guidance; repository capabilities are identified separately.*

## 1. Start with model allocation, not a complicated router

The first routing decision happens offline: determine which models are suitable for each application task. Runtime routing implements that policy and adapts only where adaptation provides a measured benefit.

The objective is to minimize total cost per successful task while satisfying quality, latency, reliability, and data-handling requirements. Open-weight versus closed is a deployment and licensing distinction, not a dependable capability ranking. Hosted open-weight models still have provider costs and data policies.

Separate three decisions:

| Decision | Question |
|---|---|
| Workflow selection | Does this request need retrieval, calculation, code execution, generation, or an action workflow? |
| Model allocation | Which approved model should perform this task or step? |
| Provider selection | Which approved endpoint should serve that model? |

Begin with a small model pool and a fixed task-to-model mapping. Add a classifier, learned quality router, cascade, or parallel candidate generation only after comparing it against that baseline.

## 2. Describe tasks using separate dimensions

Your proposed dimensions are useful, but they should not be collapsed into one difficulty label.

| Dimension | What to record | Why it matters |
|---|---|---|
| Business task | Code review, specification drafting, invoice extraction, policy Q&A | Defines the intended outcome |
| Operation | Classification, extraction, generation, reasoning, verification, tool execution | Helps choose an evaluator |
| Execution structure | Single call, fixed pipeline, branching workflow, interactive agent | Determines whether to evaluate a response or a trajectory |
| Answer structure | One label/value, multiple valid answers, structured record, free-form text | Determines whether exact matching is appropriate |
| Difficulty signals | Input size/quality, dependencies, conflicting evidence, reasoning steps, constraints | May justify different model allocation within a task |
| Error consequences | Reversible draft, misleading advice, external write, destructive action | Determines acceptance thresholds and execution controls |
| Serving requirements | Deadline, budget, modality, privacy, required tools | Filters eligible models and providers |

“Semantic understanding” is a capability requirement; “workflow” describes execution structure. They can occur together. Likewise, multiple valid answers differ from generating multiple candidate answers: the first affects grading, the second is an inference strategy.

Risk is separate from difficulty. A one-field account update can be easy to interpret but consequential if applied incorrectly.

## 3. Build a useful task taxonomy

Split tasks when they need different models, evaluators, tools, or controls—not as finely as possible. Excessively narrow categories create sparse evaluation sets and maintenance work.

The following is a proposed application taxonomy, not OpenRouter’s official classification list. OpenRouter documents approximately 30 task types, including code debugging, multi-step planning, knowledge Q&A, math, support, and research reports. Its current managed Auto Router uses task classification and recent aggregate spend signals; these are not substitutes for your quality evaluations. [1]

| Family | Specific tasks to distinguish | Evaluation emphasis |
|---|---|---|
| Coding: implementation | Function generation, feature implementation, refactoring, migration | Executable behavior and regressions |
| Coding: specifications | Requirements extraction, acceptance criteria, API specifications | Traceability, completeness, schema/contract validation |
| Coding: review | Bug detection, security review, performance review | Verified findings, missed defects, false positives |
| Coding: repository understanding | Symbol lookup, dependency tracing, workflow explanation, change-impact analysis | Correct files/symbols, relationships, evidence |
| Coding: architecture | Design alternatives, system decomposition, capacity planning | Constraints, calculations, scenario tests, expert review |
| Coding: DevOps | Infrastructure configuration, CI repair, incident diagnosis, deployment planning | Validation, sandbox execution, recovery behavior |
| Documents: transformation | Rewrite, translation, summarization, formatting | Fact preservation, coverage, measurable constraints |
| Documents: creation | Reports, proposals, specifications, presentations | Required content, source support, audience suitability |
| Documents: extraction | Fields, entities, tables, relationships | Field/set accuracy and provenance |
| Knowledge and RAG | Direct lookup, multi-document synthesis, contradiction resolution, abstention | Correctness, evidence use, evidence sufficiency |
| Classification | Intent, topic, urgency, out-of-scope detection | Label accuracy, class-specific precision/recall |
| Data analysis | SQL, calculations, reconciliation, chart interpretation | Execution results, numerical checks, invariants |
| Agents | Read-only research, record updates, transaction workflows, recovery | Final state, policy compliance, repeated-run success |
| Multimodal | Scanned document reading, image reasoning, video understanding | Modality-specific labels and task outcomes |

For difficulty, retain observable tags such as “conflicting sources,” “three dependent systems,” or “strict nested schema.” Validate that they actually predict model failures. A long input is not automatically difficult; a short input can require substantial reasoning.

## 4. Match evaluation to the nature of the task

A benchmark is a dataset plus protocol and scorer. A metric is a measurement. A harness runs the experiment. A router uses resulting evidence to choose execution paths.

| Task nature | Concrete measurement | Benchmark or implementation starting point | Limitation |
|---|---|---|---|
| Classification | Accuracy, macro-F1, critical-class recall | CLINC out-of-scope evaluation | Public labels may differ from yours |
| Multiple-choice reasoning | Correct-option accuracy from likelihood or generated answers | MMLU-Pro; LM Evaluation Harness | Does not measure complete agent behavior |
| Short grounded answers | Normalized exact match, token F1, correct abstention | SQuAD 2.0 | Limited view of long-form semantic quality |
| Long-context comprehension | Accuracy by task and context group | LongBench v2 | Comprehension is not citation faithfulness |
| Extraction | Field accuracy, set precision/recall, whole-record accuracy | Custom gold records and deterministic scorers | Schema validity alone does not establish truth |
| Instruction following | Individual and all-constraint pass rates | IFEval | Measurable constraints do not cover every quality dimension |
| Grounded prose | Fact coverage, evidence matching, unsupported claims | Custom fact/evidence labels; ALCE-style evaluation | Automated semantic support commonly uses fallible entailment models |
| Code generation | Executable task success/pass@1 | LiveCodeBench | Programming problems differ from repository maintenance |
| Repository changes | Resolution rate and regression checks | SWE-bench Verified | Evaluates the harness/model combination |
| Code review | Precision of verified findings; recall on known defects | Seeded defects, confirmed historical bugs, reproduction tests | Absence of known defects does not prove a clean repository |
| Tool calling | Function/argument correctness and execution success | BFCL | Tool correctness alone does not establish workflow success |
| Agent workflows | Final-state assertions, policy violations, consistency | τ-bench family and custom sandbox scenarios | Environment, simulator, and version affect results |
| Architecture/specifications | Constraint satisfaction, requirement coverage, executable contracts | Custom scenarios and expert-calibrated rubrics | No universal deterministic score for good design |

Primary benchmark references appear in [5–12].

Prefer reference matching, executable tests, and state assertions wherever they measure the actual requirement. For open-ended work, combine objective checks with explicit rubrics and calibrated reviewers. Do not claim that every semantic task can be reduced to an objective scalar.

Likelihood evaluates how a model ranks supplied candidates. High probability is not proof of truth. Compare candidate-selection accuracy against gold answers; use calibration metrics only when suitable probabilities are available. Output-token logprobs do not necessarily provide arbitrary continuation scoring. Keep likelihood-based and generated-answer protocols separate. The harness API guide documents relevant endpoint restrictions. [3]

Add metamorphic tests: paraphrasing should preserve intent; changing a source value should change the answer; removing essential evidence should trigger abstention. Add property tests: totals reconcile, refunds stay within limits, and unrelated records remain untouched. These complement correctness tests because a model can be consistently wrong.

### 4.1 Create an evaluation contract for each task

Before running models, specify the unit of evaluation and the conditions for success. The following is a proposed contract, not a framework-specific schema.

| Contract field | Example: grounded policy Q&A |
|---|---|
| Case ID and task tags | `policy_017`; exception handling; two sources |
| Inputs | Question, source documents, applicable policy date |
| Required output | Answer, conditions, supporting passage IDs, or abstention |
| Ground truth | Approved limit, applicable exception, acceptable evidence sets |
| Primary metric | Fully correct and supported response rate |
| Diagnostic metrics | Required-fact coverage, unsupported assertions, unnecessary abstention |
| Serious failure | Unconditional approval where prior authorization is required |
| Allowed resources | Supplied documents only; no external retrieval |
| Budget | Declared token, time, and retry limits |
| Scorer version | Frozen normalization rules, gold labels, and grading code |

For coding, substitute a repository snapshot, requested behavior, hidden tests, and regression tests. For agents, specify initial environment state, user goal, allowed tools, expected final-state predicates, and forbidden side effects. Do not require an exact action sequence unless the order itself is a requirement.

### 4.2 Define the metrics precisely

| Metric | Definition | Interpretation |
|---|---|---|
| Accuracy | Correct predictions / evaluated cases | Useful for balanced label or answer tasks |
| Precision | True positives / all predicted positives | How many flagged cases/findings are correct? |
| Recall | True positives / all actual positives | How many relevant cases/findings were found? |
| Macro-F1 | Mean of each class's F1; F1 = 2PR/(P+R) | Gives every class equal weight |
| Whole-record accuracy | Records with every required field correct / records | Prevents many easy fields hiding a critical-field error |
| Exact match | Outputs matching an accepted answer after frozen normalization / cases | Deterministic but strict about valid variants |
| Token F1 | Token-overlap precision/recall combined into F1 | Partial lexical overlap, not proof of semantic equivalence |
| Retrieval recall@k | Relevant items found in top k / all annotated relevant items | Measures retrieval coverage; specify item unit and aggregation |
| Correct abstention rate | Appropriate abstentions / unanswerable cases | Must be paired with unnecessary-abstention rate on answerable cases |
| Task pass rate | Cases satisfying all mandatory outcome checks / cases | Primary outcome for executable or state-based evaluation |
| Serious-error rate | Cases containing a predefined serious failure / cases | Report separately from average success |
| Checker false-accept rate | Incorrect outputs accepted / all incorrect outputs checked | Tests whether escalation can safely rely on the checker |
| Cost per successful task | Total cost of all attempts / successful tasks | Includes failures, retries, judges, tools, and escalation |

Define denominators, aggregation, and missing-output handling before testing. A timeout or exhausted retry is a failure in the end-to-end score, even if it is excluded from a separately reported model-capability diagnostic. Standard classification and probability metrics have implementations in scikit-learn. [4]

### 4.3 Use likelihood scoring as one track

For a question x and candidate answer a, calculate the sum of conditional token log-probabilities, log P(a|x). Select the highest-scoring candidate and compare it with the gold answer. Report accuracy. If the benchmark uses length normalization, follow its specified rule; do not change normalization to improve a preferred model's score.

For probability diagnostics, log loss penalizes low probability assigned to the true class. Brier score measures squared error between class probabilities and the one-hot ground truth; declare the binary/multiclass convention. Calibration asks whether predictions assigned similar confidence are correct at the corresponding frequency. Confidence-bin results depend on sample size and binning.

Candidate-normalized probabilities are conditional on the supplied answer set; they are not automatically the probability that a free-form answer is correct. Missing candidates in top-k API logprobs prevent exact reconstruction. Never compare average token logprobs across different tokenizers as a universal capability ranking. [3,4]

For mixed hosted open-weight and closed models, use the same generated-answer or execution protocol as the common comparison. Add likelihood diagnostics only for endpoints that support the necessary scoring. Do not label one model's likelihood accuracy and another's generated-answer accuracy as the same experiment.

### 4.4 Grounding: evaluate retrieval, facts, and support separately

Build cases containing verified facts, accepted evidence passages, and an answerability label. Score three stages separately:

1. **Retrieval:** Did the necessary evidence reach the model? Use passage/document recall and ranking metrics appropriate to the dataset.
2. **Answer correctness:** Did the output contain the required values, relationships, and exceptions? Use structured fact matching where feasible.
3. **Evidence support:** Does each asserted fact follow from its cited evidence? Real citation IDs and verbatim quotes are necessary checks in some tasks, but do not by themselves prove support.

For unrestricted prose, semantic support still requires annotated judgments or a calibrated entailment evaluator. ALCE's implementation is a useful reference for the latter; its scores are model-based estimates. [12] Measure unsupported claims and omitted required facts separately: an empty answer should not win by making no unsupported claims.

Test answerable and unanswerable cases. Add counterfactual variants: change the source amount, remove an exception, or replace a date, then check whether the response tracks the changed evidence. These controlled cases help distinguish source use from memorized answers.

### 4.5 Coding, review, DevOps, and agent evaluations

| Task | Test fixture | Passing condition |
|---|---|---|
| Function generation | Inputs with ordinary, boundary, and adversarial cases | Required behavior passes hidden tests |
| Repository patch | Fixed repository plus issue-specific and regression tests | Bug fixed and required existing behavior preserved |
| Code review | Known defects plus clean controls | Findings match verified defects; unsupported findings count against precision |
| Infrastructure change | Disposable environment, validation, plan, and policy checks | Valid configuration and intended state without prohibited changes |
| Incident diagnosis | Seeded fault, logs, topology, and controlled observations | Identifies the cause with supporting evidence; generic plausible advice does not pass |
| Agent transaction | Initial state, user goal, tool simulator, state predicates | Correct final state and no forbidden effects |
| Agent recovery | Injected timeout, duplicate delivery, stale state, missing tool | Safe termination or successful recovery within the shared budget |

Use isolated execution and prevent test tampering. Freeze model, harness, tools, and environment versions. For model comparisons, hold the surrounding harness constant; for system comparisons, explicitly report harness changes. SWE-bench and BFCL provide concrete executable evaluation patterns; the τ-bench evaluator illustrates configurable workflow rewards. [10,11]

Distinguish **pass@k** (at least one success among k attempts) from **pass^k** (all k trials succeed). The former concerns repeated-attempt opportunity; the latter concerns reliability. Follow the benchmark's estimator and protocol. Neither should replace single-attempt performance when users receive only one attempt.

### 4.6 Keep evaluators honest

Audit graders before using them to select models. Include deliberately wrong but fluent answers, correct paraphrases, incomplete answers, invalid schemas, and outputs that try to instruct the judge. Code graders should fail for real behavioral errors and accept valid alternatives.

Where semantic judgment is necessary, hide candidate identity, use explicit criteria, and compare automated decisions with independently labeled examples. Record disagreement and false acceptance. Reward-model preferences, embedding similarity, and entailment predictions are useful signals, but they are not deterministic correctness labels.

For architecture and specifications, evaluate measurable requirements first: missing requirements, invalid contracts, inconsistent interfaces, calculations, and scenario outcomes. Keep the remaining expert judgment visible rather than disguising it inside an apparently objective score.

### 4.7 Convert results into a routing decision

Store one row per case, candidate configuration, and trial:

`case_id, task, difficulty_tags, consequence_level, model_version, provider, prompt_version, harness_version, trial, outcome, error_type, cost, latency, scorer_version`

Report results by task and important subgroups, alongside overall results weighted to expected traffic. Report stress-test results separately. Use paired comparisons on the same cases; confidence intervals should respect related cases, such as multiple requests from one repository or conversation. Keep the final holdout untouched while choosing thresholds.

An illustrative decision table:

| Observed result | Allocation decision |
|---|---|
| A meets quality and serious-error requirements at lower cost | Route the task directly to A |
| A fails specifically on identifiable conflicting-source cases; B passes | Add a tested conditional rule for that subgroup |
| A fails unpredictably, but a validated checker detects failures and B repairs them | Evaluate a cascade end to end |
| A and B fail on the same cases | Improve evidence/tools/task design instead of assuming escalation helps |
| Differences are smaller than measurement uncertainty | Retain the simpler policy and gather more evidence |

Measure **under-routing** (cheap route fails when the stronger route succeeds), **over-routing** (expensive route used when an eligible cheaper route would succeed), escalation rate, and routing overhead. These diagnostics require offline outcomes for the alternative models; production logs from the selected model alone cannot reveal every counterfactual.

For workflow routing, add the cost of downstream repair. For all policies, report quality, serious errors, total cost per success, and p95 end-to-end latency together. A router is useful only if the complete policy improves the trade-off that matters to the application.

## 5. Run the offline selection process

1. **Set acceptance criteria first.** Define task success, serious errors, latency limits, and budget. High-consequence tasks need separate error checks, not merely a higher average score.
2. **Construct representative cases.** Include routine traffic, edge cases, missing information, and known failures. Keep production-frequency estimates separate from a deliberately difficult stress set.
3. **Separate development and holdout data.** Tune prompts, train routers, and calibrate thresholds without using the final holdout. Group related repository/document/conversation cases to reduce leakage.
4. **Evaluate candidate configurations.** Record model version, provider, prompt, inference budget, context, tools, harness, and evaluator version. Give candidates comparable tuning effort.
5. **Build a per-case result matrix.** Store task tags, pass/fail, failure type, cost, and latency for each model. This reveals complementary strengths hidden by averages.
6. **Compare policies.** Evaluate the best fixed model, cheapest qualifying fixed model, fixed task mapping, and any proposed dynamic strategy on the same holdout.
7. **Evaluate workflows end to end.** A cheaper extraction step may create expensive downstream errors. Do not infer mixed-pipeline success from separate component scores.
8. **Publish a versioned allocation policy.** Specify primary model, approved endpoints, eligibility conditions, escalation conditions, deadlines, and stop behavior.

Use quality-versus-cost curves rather than one leaderboard rank. A configuration is dominated if another is at least as good on all required dimensions and better on one. Report uncertainty and raw counts; zero observed serious errors is not a zero-risk guarantee.

Compare every learned router with fixed-model and simple-routing baselines. RouteLLM provides evaluation machinery for comparing routing policies; use your held-out data to establish whether added complexity creates value. [13]

## 6. Use evaluation harnesses and YAML appropriately

LM Evaluation Harness supports configurable task definitions: dataset/split, prompt construction, choices or reference target, output type, generation settings, filters, and metrics. Adapt a matching task configuration and freeze the harness/config version for reproducibility. [2]

| Evaluation requirement | Suitable approach |
|---|---|
| Labeled classification, MCQ, short-answer generation | Harness task YAML plus dataset and scorer |
| Specialized normalization or field checks | Custom scoring/filter code referenced by the evaluation setup |
| Repository execution | SWE-bench-style environment and executable test runner |
| Tool and agent interactions | BFCL/τ-bench-style runner with tools, state, and trajectory evaluation |
| Production failures | Custom fixtures for timeouts, missing tools, partial execution, retries, and recovery |

YAML configures an evaluator; it does not supply ground truth or automatically make a metric valid. An evaluation agent can help draft cases, code, and configs, but generated expected answers require verification. Keep hidden tests protected from the system being evaluated.

Maintain a common generation/execution track for all hosted candidates. Add a likelihood track where endpoints support it. A generic chat API does not guarantee likelihood-scoring compatibility. [3]

## 7. Choose a runtime strategy only where useful

| Strategy | Decision mechanism | Use when |
|---|---|---|
| Fixed task mapping | Task ID maps to an approved model | Categories have stable model requirements |
| Semantic routing | Similarity/classification identifies the task or workflow | Requests are free-form and application metadata does not identify intent |
| Learned quality–cost routing | Predict model success or relative preference before answering | Within-task variation is substantial and training evidence exists |
| Verification cascade | Generate cheaply, check, then escalate | Failures can be detected reliably and sequential latency is acceptable |
| Workflow-step allocation | Assign different models to distinct steps | Components specialize and the whole pipeline validates well |
| Best-of-n / parallel selection | Generate multiple candidates and select one | Additional sampling measurably improves accepted quality |
| Provider routing and failover | Select healthy eligible endpoints | Availability and serving performance require adaptation |

Semantic similarity identifies related requests; it does not inherently predict which model will answer correctly. Likewise, a runtime router can use a policy learned offline; “offline” and “dynamic” are stages, not mutually exclusive algorithm families.

For a two-stage cascade, expected inference cost is approximately:

**cheap attempt + checker + escalation probability × strong attempt**

Include retry, tool, cache, and selection costs in the full measurement. Escalation based on a bad answer is different from failover after an API error.

## 8. Router libraries: what they actually provide

The following descriptions were checked against the repositories’ README files. They are capability summaries, not production certification or measured comparisons. [14–17]

| Library | Documented mechanisms | Best role in your plan | Main qualification |
|---|---|---|---|
| **lm-sys/RouteLLM** | `mf`, `sw_ranking`, `bert`, `causal_llm`; strong/weak-model threshold routing | A focused experiment in learned two-model allocation | Existing preference-trained routers need workload validation and threshold calibration |
| **ulab-uiuc/LLMRouter** | 16+ methods spanning single-round, multi-round, multimodal, agentic, and personalized routing; training/inference CLI and data pipeline | Compare algorithm families within a common experimental framework | Verify each chosen method’s data, dependencies, modality, and serving support |
| **microsoft/best-route-llm** | HybridLLM and BEST-Route; model allocation and best-of-n compute choices | Study whether multiple inexpensive samples compete with one expensive answer | Research workflow includes reward-model scoring; those rewards are proxies for your task success |
| **aurelio-labs/semantic-router** | Embedding-based route matching, route examples, threshold optimization, local encoders, multimodal examples | Fast task/workflow identification before applying your allocation policy | Route-match confidence is not answer-quality confidence; retain an unknown route |

### Common router algorithms in these libraries

| Router type | How it works | Offline evidence needed |
|---|---|---|
| Semantic similarity | Match a query to examples defining a route | Labeled route examples, near-boundary cases, unknown intents |
| K-nearest-neighbor routing | Use outcomes on similar historical queries to select a model | Query representations and per-model task results |
| Similarity-weighted Elo | Weight pairwise preference evidence by similarity to the current prompt | Pairwise outcomes/preferences and prompt embeddings |
| Matrix factorization | Learn latent relationships between query representations and model preferences | Query/model preference observations |
| SVM, MLP, BERT classifiers | Predict a route or model-performance class from input features | Labeled outcomes or routing targets |
| Causal-LM router | Fine-tune a generative model to make routing decisions | Routing training examples and inference-overhead measurements |
| HybridLLM | Learn deterministic or probabilistic allocation between a model pair | Paired model quality/cost evidence |
| BEST-Route | Allocate among model and best-of-n sampling configurations | Multiple sampled responses, selection scores, total costs |
| Graph/personalized/multi-round routers | Incorporate model/query relationships, user context, or sequential state | Method-specific interaction and outcome data |

RouteLLM’s `sw_ranking` is specifically similarity-weighted Elo, not simply a generic Elo classifier. BEST-Route optimizes compute allocation as well as model choice. LLMRouter documents image/video and other multimodal capabilities, but “uniquely offers multimodal routing” is too strong: Semantic Router also documents multimodal examples. [14–17]

Do not install all four by default. Use simple application rules first; Semantic Router if intent identification needs it; RouteLLM for a focused two-model predictor; LLMRouter for broader comparative experiments; BEST-Route when sampling-budget allocation is the question.

## 9. Production system design

| Component | Responsibility |
|---|---|
| Task identifier | Use application metadata or classify free-form intent |
| Eligibility filter | Enforce modality, context, parameter, destination, and data-policy requirements |
| Versioned policy | Choose the approved primary model and conditional alternatives |
| Provider adapter/gateway | Normalize API calls and record actual endpoint/model |
| Execution controller | Enforce workflow budget, deadline, retries, concurrency, and stop conditions |
| Task validator | Apply schema, fact, test, or state checks appropriate to the task |
| Telemetry and evaluation loop | Record outcomes and feed reproducible failures into regression tests |

Model selection cannot authorize external actions. Tool permissions and destination restrictions must be enforced independently.

| Failure mode | Design response |
|---|---|
| Unknown task or uncertain route | Known-safe default, clarification, or abstention |
| Overload, timeout, provider outage | Bounded queue/retries, circuit breaker, approved fallback |
| Cheap model frequently escalates | Re-evaluate direct routing; count both attempts |
| Checker accepts incorrect output | Measure false acceptance against gold cases; improve or remove the cascade |
| Missing retrieval evidence | Repair retrieval or abstain; a stronger generator cannot supply absent evidence |
| Unsupported tools or output parameters | Filter incompatible endpoints and fail explicitly |
| Partial tool execution and retries | Checkpoints, idempotency, state reconciliation |
| Model switching changes behavior | Compatibility tests, canonical state, explicit switch boundaries |
| Switching destroys caches | Prefer session affinity unless measured benefit justifies switching |
| Model/provider/evaluator drift | Version records, canary release, regression gates, rollback |
| Sensitive information in logs | Redaction, restricted access, retention controls |
| Long loops or runaway costs | Shared step, token, time, and spend limits across all layers |

OpenRouter documents provider filters, parameter requirements, routing preferences, and model failover. Latency preferences are not a guaranteed deadline; error fallback is not semantic answer verification. Auto Exacto addresses provider quality signals for tool calls, not application-specific authorization. [18–20]

Load-test the complete policy under expected concurrency. Quality measured offline and latency measured on an idle endpoint are insufficient evidence of production behavior. Include model-upgrade evaluation, ongoing annotation, gateway operation, and on-call burden in the maintenance decision.

## 10. Worked example: routing a repository assistant

Suppose the application supports three tasks: symbol lookup, narrow code changes, and cross-service incident diagnosis.

| Task | Nature and difficulty tags | Offline evaluation |
|---|---|---|
| Find the refund-limit validation | Repository retrieval; usually bounded; read-only | Gold symbol/file location, accepted evidence paths |
| Fix a rounding bug | Code generation; bounded modification | Hidden rounding cases and regression tests |
| Diagnose duplicate refunds across services | Multi-step workflow; partial evidence; high consequences | Seeded incident sandbox, causal evidence checks, forbidden-action checks |

Evaluate a small open-weight candidate A and a second candidate B, which may be open or closed. Assume the results establish that A qualifies for lookup and narrow fixes, while B is required for incident diagnosis. These are hypothetical conclusions, not claims about named models.

The initial policy uses A for the first two tasks and B for diagnosis. If the application already knows the task, no semantic classifier is needed.

Next test an optional cascade for narrow fixes: A generates a patch, tests execute, and B receives one escalation if required tests fail. Evaluate the complete cascade, including whether B repairs A’s failures, how often faulty patches pass the checker, and total latency. Tests must cover meaningful behavior rather than merely validate the generated implementation.

At runtime, “fix this rounding issue” follows the tested policy. A provider outage triggers approved availability failover. A failing patch triggers quality escalation. Missing repository context triggers retrieval. Exhausting the budget stops execution. None of these decisions permits automatic production deployment.

The offline deliverables are the task taxonomy, dataset/scorers, per-case model matrix, and versioned policy. The runtime deliverables are the controller, validators, monitoring, and regression loop. A learned router is added only if it improves the held-out quality–cost–latency trade-off enough to justify its overhead and maintenance.

## GitHub references

1. [OpenRouter Auto Router — current task classification and routing behavior](https://github.com/OpenRouterTeam/docs/blob/main/guides/routing/routers/auto-router.mdx).
2. [EleutherAI LM Evaluation Harness — task configuration guide](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/task_guide.md).
3. [EleutherAI LM Evaluation Harness — API and likelihood-scoring support](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/API_guide.md).
4. [Scikit-learn — classification and probability scoring implementations](https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/metrics/_classification.py).
5. [CLINC intent and out-of-scope evaluation](https://github.com/clinc/oos-eval).
6. [MMLU-Pro](https://github.com/TIGER-AI-Lab/MMLU-Pro) and [SQuAD 2.0 scoring](https://github.com/huggingface/evaluate/blob/main/metrics/squad_v2/squad_v2.py).
7. [LongBench and LongBench v2](https://github.com/THUDM/LongBench).
8. [Google Research IFEval](https://github.com/google-research/google-research/tree/master/instruction_following_eval).
9. [LiveCodeBench](https://github.com/LiveCodeBench/LiveCodeBench).
10. [SWE-bench evaluation](https://github.com/SWE-bench/SWE-bench/blob/main/docs/guides/evaluation.md).
11. [Berkeley Function Calling Leaderboard methods](https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard) and [Sierra τ-bench evaluation criteria](https://github.com/sierra-research/tau2-bench/blob/main/docs/evaluation.md).
12. [ALCE evaluation implementation](https://github.com/princeton-nlp/ALCE/blob/main/eval.py).
13. [RouteLLM — router evaluation implementation](https://github.com/lm-sys/RouteLLM/tree/main/routellm/evals).
14. [LMSYS RouteLLM README](https://github.com/lm-sys/RouteLLM/blob/main/README.md).
15. [UIUC LLMRouter README](https://github.com/ulab-uiuc/LLMRouter/blob/main/README.md).
16. [Microsoft HybridLLM and BEST-Route README](https://github.com/microsoft/best-route-llm/blob/main/README.md).
17. [Aurelio Semantic Router README](https://github.com/aurelio-labs/semantic-router/blob/main/README.md).
18. [OpenRouter provider selection](https://github.com/OpenRouterTeam/docs/blob/main/guides/routing/provider-selection.mdx).
19. [OpenRouter model fallbacks](https://github.com/OpenRouterTeam/docs/blob/main/guides/routing/model-fallbacks.mdx).
20. [OpenRouter — Auto Exacto documentation source](https://github.com/OpenRouterTeam/docs/blob/main/guides/routing/auto-exacto.mdx).
