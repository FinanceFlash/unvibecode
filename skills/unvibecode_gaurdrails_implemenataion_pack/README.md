# Guardrails implementation pack

Three deliverables: application-specific implementation guides, a production anti-pattern FAQ, and an evidence-based verification guide. These are Markdown files intended for developers and coding LLMs. No runtime guardrail programs are included in this release.

## 1. Choose the application guide

| Application | File | Extra guides when capabilities overlap |
|---|---|---|
| RAG | [01_RAG_IMPLEMENTATION.md](01_RAG_IMPLEMENTATION.md) | Add tool-agent controls for actions |
| Conversational chatbot | [02_CHATBOT_IMPLEMENTATION.md](02_CHATBOT_IMPLEMENTATION.md) | Add RAG for retrieval; tool-agent for API actions |
| Agent with tool calling | [03_TOOL_AGENT_IMPLEMENTATION.md](03_TOOL_AGENT_IMPLEMENTATION.md) | Add RAG for document answers |
| Multi-agent application | [04_MULTI_AGENT_IMPLEMENTATION.md](04_MULTI_AGENT_IMPLEMENTATION.md) | Add tool-agent/RAG details for participating agents |

Each guide stands alone: it includes LLM instructions, six application-specific question prompts, a stage/interface control matrix, method tiers, failure paths, system-design rules, acceptance cases and a required design-output format. The repeated common sections are intentional so an individual file can be passed to an LLM without losing essential instructions.

## 2. Use the production FAQ

[05_PRODUCTION_ANTIPATTERN_FAQ.md](05_PRODUCTION_ANTIPATTERN_FAQ.md) contains 28 focused failures: missing version history, PII in observability, premature external transmission, asynchronous bypasses, silent truncation, streaming leaks, stale approvals, duplicate actions, unbounded calls, delegation loops, unsafe caches, memory poisoning and more.

Each entry includes a corrective action and verification step. Use it while designing and again when reviewing production incidents.

## 3. Verify with evidence

[06_VERIFY_GUARDRAILS.md](06_VERIFY_GUARDRAILS.md) provides a reviewer prompt, 30 stable checklist IDs, failure-injection scenarios and a report format. It works before code exists and becomes stronger as configuration, implementation and runtime evidence are supplied.

A design-level PASS means the requirement is specified. It does not establish runtime enforcement. No evidence is reported as UNVERIFIED, not silently converted to success.

## How to start

Give the selected application guide to an LLM with this message:

> Use the attached application implementation guide to design our guardrails. Here is our existing context: [supported tasks, users/tenants, data sources, models/framework, deployment, tools, memory, streaming, privacy constraints, latency goals, and known failures]. First summarize what is already known, then ask 5–6 specific unanswered questions using the guide and this context. Do not repeat questions I have already answered. After my responses, produce the guide's required design output. Keep unresolved policy choices explicit. Do not write code yet.

If the application combines capabilities, attach the relevant guides together. Ask for one combined design with duplicate controls merged and each boundary still covered.

After design, give the verification guide to a reviewer with the design and available evidence:

> Apply the attached verification guide to this design and evidence. Report the evidence level for every conclusion. Propose missing tests but do not claim to run them. Prioritize unauthorized side effects, privacy failures, cross-tenant access and unbounded execution.

Do not share secrets or raw customer data with a reviewing LLM. Redacted schemas, synthetic examples and minimal relevant code are usually enough to begin.

## Intended boundaries

- The guides propose implementation requirements; they do not install or enforce them.
- T1–T4 are checking methods. T5 is scope routing, which can use those methods and normally runs early.
- Detector choices and thresholds require workload-specific validation; there is no universal low-latency or best-accuracy setting.
- All listed failure paths are minimum inventories to extend for the actual application, not an exhaustive claim about every production system.
- Sources are linked compactly inside each guide. Framework-specific settings must be checked against the deployed release.

Author: Divya Singaravelu, open-source creator of UnvibeCode.
