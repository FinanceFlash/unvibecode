# Permission and Abuse Guide

## Permission boundaries
- Only authorized tenant-scoped context may enter a generation request
- Untrusted input must not override protected instructions or permissions
- Only schema-valid and business-valid output may reach downstream consumers
- Safety, refusal, truncation, timeout, and uncertainty must remain explicit states
- Retry and repair must be bounded and version-aware

## Misuse paths
- Prompt or context injection — Untrusted text overrides protected instructions or extracts hidden context
- Cross-tenant data exposure — The prompt includes another customer's documents, settings, or generated output
- Invalid structured output — Downstream code trusts missing, mistyped, invented, or malformed fields
- Unsafe or unsupported content — The model produces harmful, prohibited, or misleading material
- False success — Truncated, blocked, invalid, or uncertain output is reported as complete
- Unbounded cost or latency — Large prompts, retries, or concurrency consume provider capacity and budget
- Version inconsistency — Prompt, schema, policy, or model changes make retries and outputs irreproducible
- Secret or personal-data exposure — Prompts, responses, credentials, or provider errors reach unsafe storage or logs

Protect actor identity, tenant scope, prompts, sources, outputs, provider credentials, support tools, and audit records. Deny uncertain ownership, evidence, or permission.

