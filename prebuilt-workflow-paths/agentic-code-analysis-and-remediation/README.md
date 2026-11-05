# Agentic Code Analysis and Automated Remediation

Starts when a developer or CI pipeline grants an agent access to a repository for analysis or remediation. Ends when the agent delivers an analysis report, proposes a pull request, exhausts its quota, or is terminated by the developer.

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
- repository access authorization, source file indexing, abstract syntax tree and dependency graph extraction, code analysis, autonomous reflection loops, sandbox execution, code remediation proposals, and pull request generation

## Excluded
- generic static application security testing without autonomous agent intervention, general continuous integration runner tasks without LLM operations

The five `*_SKILL.md` files are self-contained.
