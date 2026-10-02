# Common guardrails configuration checker

Unvibecode · Practical notebook 04

Use this package to draft a guardrails design and review its declared configuration. It does not inspect your application code, run the PII/SetFit/Sentinel models, or prove that a configured control executes.

## Files and quick start

- `04_common_guardrails_checker.ipynb`: standalone notebook with the checker, examples, and regression tests. Python standard-library code; open it in Jupyter and Run All.
- `guardrails_runner.py`: standalone CLI; Python 3.10+ and no third-party runtime packages.
- `guardrails_chatbot.json`, `guardrails_rag.json`, `guardrails_agent.json`, `guardrails_multi_agent.json`: independent editable profiles. No shared-file merge is required.

Keep the runner and selected JSON file in the same working folder, then:

```bash
python guardrails_runner.py check --config guardrails_rag.json
python guardrails_runner.py questions --config guardrails_rag.json
python guardrails_runner.py check --config guardrails_rag.json --strict
```

On Windows, `py` can replace `python`. To start another configuration:

```bash
python guardrails_runner.py init --app agent --out my_agent.json
```

`init` refuses to overwrite an existing file. `check` prints a JSON report. Exit codes: **0** means no configuration errors; **1** means failed checks (or unresolved warnings in strict mode); **2** means a file/schema parsing operation failed. Unknown and duplicate JSON keys are rejected.

The supplied draft profiles have zero errors and unresolved warnings. This is intentional: control bindings, trained intent artifacts, and authorized Sentinel access must be supplied. Strict mode should exit 1 until those declarations are resolved. Even after it exits 0, `runtime_verified` remains false.

## What to configure

| Area | What you supply |
|---|---|
| Application/features | Workflow type plus retrieval, tool, and memory usage |
| Stage controls | Stage, implementation tier, release ordering, failure action, dotted callable reference |
| PII | Geography union, language, redact/block policy, recognizer version |
| Intent | Supported labels, uncertainty behavior, clarification limit, trained model and threshold artifacts |
| Injection | Pinned Sentinel revision, token bounds, thresholds, model-access declaration |
| Runtime | Request/guard deadlines, worker and queue bounds, global model/tool/retry/handoff budgets |
| Observability | Metadata-only logging, retention, policy and model versions |

Numbers are starter values, not recommended latency SLAs or calibrated thresholds. Adjust them using your workload. The schema deliberately requires explicit settings and blocks silent text truncation. Request-wide counters must include retries and nested agent/tool activity; declaring them here does not implement the counters.

Every mandatory control runs `before_release` of its protected boundary. An answer check therefore precedes delivery to the user; a tool check precedes the side effect; a memory-write check precedes persistence. This describes ordering, not a requirement to run CPU work inside an async event loop.

## Connect the previous notebooks

| Notebook | Common configuration | Adapter responsibility |
|---|---|---|
| 01: PII | `pii`, `input_pii`, `output_pii` | Instantiate the PII configuration; forward only released text; block scanner errors. |
| 02: Intent | `intent`, `input_intent` | Load trained weights and their thresholds together; preserve mixed intents; bound clarification. |
| 03: Injection | `injection` and boundary-specific injection controls | Load the pinned model with authorized access; scan complete inputs; withhold uncertain, failed, or oversized scans. |

The runner never imports or executes `binding` values. A reference such as `support.security.check_tool_permissions` is a design declaration until your application actually calls it. The runner also does not read model artifacts or test Hugging Face access. `access_confirmed=true` is an operator declaration, not an access probe.

Content moderation, retrieval permissions, evidence sufficiency, answer grounding, tool authorization, memory policy, and agent-handoff controls need application-specific implementations beyond notebooks 01–03. Do not map all of these to the injection classifier.

The profiles target the notebook 01 country/language coverage and notebook 03 Sentinel adapter. Changing to another detector or adding a country requires updating the schema/adapter checks and regression tests, not merely changing a name.

## Workflow-specific decisions

- **Chatbot:** Scope and intent, missing context, input/output PII, content policy, injection, bounded clarification.
- **RAG:** Add access checks before source release, provenance, retrieved-text injection, sufficient evidence, and answer grounding. Missing evidence should trigger retrieval recovery or abstention; it is different from failing to use available evidence.
- **Agent:** Add deterministic schema, permission, ownership, destination, and idempotency checks before tools; scan results and memory. The example enables memory; disable that feature only if the application does not persist or reuse it.
- **Multi-agent:** Add sender identity, delegation permissions, provenance, and incoming-message checks at handoffs. Use shared request budgets; a child agent must not reset call or retry limits or acquire broader permissions.

## Use with an LLM

Supply your application context, selected JSON profile, checker report, and this instruction:

> Review the declared design against the application context. Treat the configuration as a specification, not proof of implementation. Ask at most six specific questions about unresolved decisions. Do not ask again for facts already supplied; combine relevant questions about stages, permissions, data, failure responses, and performance targets. Then propose a stage-by-stage design, list the exact bindings/artifacts still needed, and specify runtime tests for every protected boundary. Do not claim that a model score authorizes a transaction or that a passing configuration report proves runtime safety.

The `questions` command produces six profile-aware starting questions. It does not read your repository or infer answers from application code.

## Runtime verification still required

1. Inject detector errors, timeouts, malformed results, and oversized input; assert that protected LLM calls, tool effects, and memory writes do not occur.
2. Check retrieval ACLs and tool ownership using an identity that lacks access, not only a valid account.
3. Assert that output is buffered until mandatory checks complete; test sensitive values across stream boundaries.
4. Exercise retry loops and nested handoffs; assert that shared budgets stop the entire request.
5. Test duplicate side-effect requests and verify idempotency in the authoritative service.
6. Inspect actual traces/logs for payload leakage and missing policy/model versions.

The notebook's regression tests verify that the configuration checker catches declared anti-patterns. They do not perform these runtime checks on your application.
