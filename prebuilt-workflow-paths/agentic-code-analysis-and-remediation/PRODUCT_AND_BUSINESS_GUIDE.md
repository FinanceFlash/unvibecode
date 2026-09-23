# Product and Business Guide

## Boundary
Starts when a developer or CI pipeline grants an agent access to a repository for analysis or remediation. Ends when the agent delivers an analysis report, proposes a pull request, exhausts its quota, or is terminated by the developer.

## People and systems
- Developer
- Agent Orchestrator
- LLM Provider
- Sandbox Environment
- Source Code Repository
- Version Control System (Git forge)
- CI/CD Pipeline

## Things created or changed
- Analysis session
- Token quota
- Ingested file index
- AST/dependency graph
- Reflection log
- Remediation proposal
- Pull request draft
- Audit record

## Stages

### Session
- pending
- ingesting
- analyzing
- remediating
- completed
- failed
- terminated

### Repository
- unscanned
- indexed
- analyzed
- remediated
- skipped

### Proposal
- absent
- drafted
- validated
- submitted
- rejected

### Quota
- available
- consumed
- exhausted
- released

## Product decisions
- Mandatory isolated sandbox environment for all agent-executed commands.
- Configurable hard limits on token usage and loop iterations per session.
- Automatic exclusion of sensitive files (e.g., .env) from file indexing.
- Read-only repository access by default, write access strictly scoped to branch creation.
- Required manual approval for all agent-generated pull requests.

## Happy paths
- Agent successfully analyzes specified codebase and generates accurate architectural summary.
- Agent detects vulnerability, writes patch, verifies tests in sandbox, and drafts a pull request.
- CI pipeline triggers agent analysis, agent completes review without findings, and pipeline proceeds.

## Negative paths
- Agent fails to authenticate with source code repository.
- Token quota exhausted during complex analysis loop.
- Agent generates syntactically invalid code that fails sandbox validation.
- Agent enters unbounded reflection loop and is terminated by orchestrator.
- LLM provider returns persistent rate limit errors.

## Edge cases
- Repository contains crafted payloads attempting prompt injection (LLM01).
- Extremely large or auto-generated files cause model denial of service (LLM04).
- Required dependencies are unavailable in the isolated sandbox environment.
- Concurrent analysis sessions on the same branch cause merge conflicts.

## Acceptance criteria
1. Agent execution strictly terminates when token quota or iteration limits are reached.
2. System prevents reading and transmission of specified sensitive files (e.g., .env).
3. Sandbox Environment blocks unauthorized network access and destructive commands (LLM08).
4. Prompt injection attempts are logged and do not result in arbitrary code execution.
5. All agent interactions with the LLM provider are recorded in the audit log.
6. Pull requests created by the agent lack auto-merge privileges.
7. Agent cleanly releases sandbox resources upon session termination.
8. System correctly handles LLM provider timeouts and rate limits.
9. Agent distinguishes between safe read operations and restricted write operations.
10. Analysis session gracefully fails if repository access is revoked mid-flight.

## Business risks
| Risk | Business consequence |
|---|---|
| Prompt injection execution | Attacker controls agent to exfiltrate code or modify CI/CD pipelines. |
| Model DoS (token exhaustion) | Excessive LLM API costs and resource starvation for other operations. |
| Excessive agency | Agent executes destructive commands causing infrastructure downtime. |
| Sensitive information disclosure | Exposure of API keys, credentials, or proprietary algorithms to external LLMs. |
| Hallucinated code fixes | Decreased developer trust, wasted review time, and potential introduction of subtle bugs. |
