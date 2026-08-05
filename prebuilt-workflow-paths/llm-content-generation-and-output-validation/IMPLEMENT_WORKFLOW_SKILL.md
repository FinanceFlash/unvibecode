---
name: implement-llm-structured-generation
description: Implement or modify LLM Content Generation and Structured-output Validation. Use when adding or changing authorization, prompt or retrieval logic, validation, provider calls, output handling, retries, recovery, privacy controls, monitoring, or tests.
---

# Implement LLM Structured Content Generation

Confirm:
- Who may generate which content using which tenant data
- Permitted input, context, attachment, personal-data, and secret boundaries
- System-instruction and user-input separation and precedence
- Prompt template, model, model version, parameters, and rollout policy
- Token, character, attachment, latency, cost, and concurrency limits
- Required output schema, field constraints, enums, formats, and unknown-field policy
- Maximum parse, validation, repair, and provider retry attempts
- Safety, moderation, refusal, human-review, and fallback policy
- Whether and how raw prompts, responses, usage, and accepted outputs are retained
- Caching, idempotency, observability, privacy, and abuse policy

Follow project conventions and protect:
- Only authorized tenant-scoped context may enter a generation request
- Untrusted input must not override protected instructions or permissions
- Only schema-valid and business-valid output may reach downstream consumers
- Safety, refusal, truncation, timeout, and uncertainty must remain explicit states
- Retry and repair must be bounded and version-aware
- Repeated requests must not duplicate expensive or material downstream effects unintentionally
- Usage, validation, safety, version, latency, and cost must remain observable
- Prompts, outputs, secrets, personal data, and credentials must remain protected

Add all core tests and summarize decisions, files, state changes, recovery, privacy and security controls, and remaining gaps.

