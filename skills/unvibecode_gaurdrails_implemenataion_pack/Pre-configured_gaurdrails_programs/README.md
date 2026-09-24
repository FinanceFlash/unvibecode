# Practical guardrails notebooks

Run focused examples, configure their policies, and evaluate failure behavior before connecting them to an application.

| Notebook | Purpose | Execution requirements |
|---|---|---|
| [01: Geography-configurable PII](01_geography_configurable_pii_guardrails.ipynb) | Presidio entity selection, redact/block policies, and a release gate | Python 3.12, Presidio, local English spaCy model |
| [02: Support intent and triage](02_configurable_support_intent_guardrails.ipynb) | SetFit training; separate intent, clarity, scope, urgency, and frustration | Python 3.12, CPU PyTorch, model download |
| [03: Prompt injection and jailbreaks](03_prompt_injection_jailbreak_guardrails.ipynb) | Boundary checks, Sentinel adapter, failure handling, and optional long-context evaluation | Standard library for framework tests; authorized gated-model access for inference |
| [04: Common configuration checker](04_common_guardrails_checker.ipynb) | Profile-aware checks, anti-pattern examples, and design questions | Standard library for checker code |

Use a separate virtual environment for each model notebook. Follow its installation cell, restart the kernel, and run all cells. Notebook outputs are cleared in version control. Start with the embedded synthetic data; never commit customer messages, secrets, model weights, or execution caches.

## Configuration checker

[Implementation guide](README_guardrails_checker.md) explains the CLI and integration contracts. Choose an editable profile:

[Chatbot](guardrails_chatbot.json) · [RAG](guardrails_rag.json) · [Tool agent](guardrails_agent.json) · [Multi-agent](guardrails_multi_agent.json)

From this directory:

```bash
python guardrails_runner.py check --config guardrails_rag.json
python guardrails_runner.py questions --config guardrails_rag.json
python guardrails_runner.py check --config guardrails_rag.json --strict
```

The templates are valid drafts with unresolved bindings and artifacts. Strict mode intentionally fails until those declarations are supplied. The checker never imports the bindings or certifies runtime enforcement.

## Evaluation boundaries

- PII fixtures cover selected entities and English text; passing them does not establish complete PII recall.
- The intent classifier uses a small synthetic dataset. Its baseline evaluation missed duplicate-charge examples and part of a mixed-scope request. Inspect per-label results and evaluate representative held-out data before deployment.
- Injection framework tests use scripted results. Sentinel inference and long-context accuracy require separate real-model evaluation. The external model uses an Elastic license and requires access approval; repository licensing does not replace its terms.
- Model-call and tool-action permissions remain separate from detector scores. Configuration tests do not replace fault injection against the application.
