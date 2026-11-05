# Engineering Guide

## Trace the implementation
1. Session creation, repository access, authentication, cloning, and sandbox provisioning entry points
2. File discovery, recursive walk, symlink detection, permission checks, and unreadable-file handling
3. AST extraction, dependency graph construction, language detection, and token estimation
4. Reflection loop iteration, convergence checks, token accounting, and budget enforcement
5. Sandbox boundaries, command interception, destructive-action blocking, and developer approval gates
6. Remediation proposal generation, syntax validation, dependency verification, and test execution
7. VCS branch creation, PR drafting, authorization checks, and handoff to review
8. Audit logging, sensitive-data redaction, credential filtering, and session metrics

## Rules the code should protect
- Every session must bind the current developer, repository, sandbox, token budget, and iteration cap
- Only sandboxed file access and approved commands may execute during analysis
- Unreadable files must be skipped and logged without aborting the session
- Iteration and token limits must be enforced regardless of agent confidence or convergence progress
- Remediation proposals must pass syntax, dependency, and test validation before PR creation
- VCS operations must target only the authorized branch and never bypass required reviews
- Prompts assembled from repository content must preserve system-instruction boundaries
- Credentials, secrets, and personal data must never reach the LLM provider or unsafe logs

## Build or change safely
1. Confirm product and policy decisions before relying on provider, sandbox, or orchestrator defaults.
2. Follow existing authorization, sandbox, privacy, storage, logging, monitoring, and test conventions.
3. Bind every session to the authoritative developer, repository, sandbox scope, quota, and policy.
4. Enforce sandbox, iteration, token, command, branch, and credential rules at every material effect.
5. Make retries and replays safe after partial failure, lost provider responses, and mid-session cancellation.
6. Keep session, quota, proposal, VCS, and audit inconsistency visible and repairable.
7. Add the core 20 tests.
