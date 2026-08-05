---
name: write-llm-structured-generation-spec
description: Write or review a product specification for LLM Content Generation and Structured-output Validation. Use when defining actors, states, authorization, model or evidence rules, edge cases, acceptance criteria, recovery, or business risks.
---

# Write a LLM Structured Content Generation Specification

Use application-native terms. Decide:
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

Write scope, actors, objects, states, paths, user outcomes, permissions, validation, recovery, privacy, misuse, acceptance criteria, and unanswered decisions.

