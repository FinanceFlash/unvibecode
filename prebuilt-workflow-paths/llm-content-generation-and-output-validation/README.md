# LLM Content Generation and Structured-output Validation

Starts when an authorized request supplies user input and approved context for content generation. Ends when the request is rejected, blocked, returns a schema-valid and policy-compliant output, or fails explicitly without exposing data or misleading downstream consumers.

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
- input validation, authorization, prompt assembly, instruction precedence, model and version selection
- token limits, generation, safety checks, structured-output parsing, schema validation, and bounded repair
- output persistence or handoff, usage, cost, latency, audit, privacy, retry, and recovery
- prompt injection, cross-tenant context, unsafe content, malformed output, and misuse controls

## Excluded
- retrieval and evidence-cited question answering
- model training and registry approval
- autonomous tool execution or agent action
- human content publication approval

The five `*_SKILL.md` files are self-contained.

