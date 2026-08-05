---
name: review-llm-structured-generation-risk
description: Review customer, accuracy, privacy, cost, and operational risks in LLM Content Generation and Structured-output Validation. Use when founders, PMs, or engineering managers need prioritized consequences, controls, tests, and release concerns.
---

# Review LLM Structured Content Generation Risk

Review entry, authorization, prompt or source, versions, validation or evidence, provider behavior, retry, recovery, privacy, cost, and downstream paths. Prioritize:
- Prompt or context injection — Untrusted text overrides protected instructions or extracts hidden context
- Cross-tenant data exposure — The prompt includes another customer's documents, settings, or generated output
- Invalid structured output — Downstream code trusts missing, mistyped, invented, or malformed fields
- Unsafe or unsupported content — The model produces harmful, prohibited, or misleading material
- False success — Truncated, blocked, invalid, or uncertain output is reported as complete
- Unbounded cost or latency — Large prompts, retries, or concurrency consume provider capacity and budget
- Version inconsistency — Prompt, schema, policy, or model changes make retries and outputs irreproducible
- Secret or personal-data exposure — Prompts, responses, credentials, or provider errors reach unsafe storage or logs

For each material risk, explain trigger, behavior, business consequence, protection, decision or test, and acceptance condition.

