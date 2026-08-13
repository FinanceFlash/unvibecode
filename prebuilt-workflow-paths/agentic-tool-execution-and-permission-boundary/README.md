# Agentic Tool Execution and Permission Boundary

Starts when an AI agent or LLM controller requests the execution of a registered tool call with specific arguments on behalf of an authenticated user session. Ends when the tool execution finishes safely, returns validated and sanitized output to the agent controller, or is explicitly blocked, sandboxed, or timed out without unauthorized side effects, data leakage, or unhandled permission escalation.

| Task | File |
|---|---|
| Product and business | [PRODUCT_AND_BUSINESS_GUIDE.md](PRODUCT_AND_BUSINESS_GUIDE.md) |
| Engineering | [ENGINEERING_GUIDE.md](ENGINEERING_GUIDE.md) |
| Testing | [TESTING_GUIDE.md](TESTING_GUIDE.md) |
| Core 20 | [CORE_20_SCENARIOS.md](CORE_20_SCENARIOS.md) |
| Paths and edge cases | [PATHS_AND_EDGE_CASES.md](PATHS_AND_EDGE_CASES.md) |
| Permissions and misuse | [PERMISSION_AND_ABUSE_GUIDE.md](PERMISSION_AND_ABUSE_GUIDE.md) |
| Retry and recovery | [RETRY_AND_RECOVERY_GUIDE.md](RETRY_AND_RECOVERY_GUIDE.md) |

## Included
- tool discovery, registration, argument parsing, JSON schema validation, and instruction bounds
- user consent, human-in-the-loop (HITL) approval, action confirmation, and permission check
- execution sandboxing, timeout enforcement, memory bounds, rate limiting, and process isolation
- credential isolation, secret injection, output sanitization, error wrapping, and audit logging
- prompt injection resistance in tool arguments, recursive tool loop limits, and side-effect gating

## Excluded
- prompt template assembly and LLM content generation
- vector retrieval and document chunking
- payment authorization and external gateway billing
- user identity authentication and OAuth token issuance

The five `*_SKILL.md` files are self-contained.
