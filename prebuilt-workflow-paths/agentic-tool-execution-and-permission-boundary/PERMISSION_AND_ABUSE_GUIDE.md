# Permission and Abuse Guide

## Security Threat Model

Agentic tool execution introduces unique threat vectors due to the non-deterministic nature of LLM reasoning and susceptibility to indirect prompt injection.

| Vulnerability / Threat Vector | Attack Scenario | Prevention Control |
|---|---|---|
| Indirect Prompt Injection | Malicious website contents instruct agent to call `send_email` with internal data | Strict HITL approval for external data transmission tools |
| SSRF (Server-Side Request Forgery) | Agent tool takes URL argument and requests `http://169.254.169.254/latest/meta-data` | Network egress allowlisting and metadata IP blocking |
| Privilege Escalation | User tricks agent into invoking admin-only maintenance tool | Fine-grained RBAC evaluation per tool call session token |
| Resource Exhaustion (DoS) | Agent trapped in endless tool calling loop | Iteration caps (max 10 tool steps per user turn) |
| Environment Variable Theft | Tool script prints `process.env` | Micro-container isolation with stripped environment |

## Abuse Monitoring

- Track tool invocation velocity per user session. Trigger rate limiting if tool requests exceed 30 per minute.
- Flag repeated schema validation failures as potential automated fuzzing attacks.
