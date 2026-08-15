---
name: write-agentic-tool-execution-spec
description: Write or review a product specification for Agentic Tool Execution and Permission Boundary. Use when defining tool registration, JSON schema bounds, human-in-the-loop approvals, sandboxing, permission checks, audit logging, rate limits, or error recovery.
---

# Write an Agentic Tool Execution Specification

Use application-native terms. Decide:
- Who may execute which registered tools under which user role or tenant context
- Required JSON schemas, argument types, required parameters, and unknown-field policy
- Human-in-the-loop (HITL) approval rules for high-risk side-effecting operations
- Execution sandboxing, CPU/memory resource limits, and network egress boundaries
- Secret injection, token scope handling, and output credential redaction rules
- Maximum execution timeouts, retry policies, and circuit breaker parameters
- Audit log retention, trace metadata formatting, and observability rules

Write scope, actors, objects, states, paths, user outcomes, permissions, validation, recovery, privacy, misuse, acceptance criteria, and unanswered decisions.
