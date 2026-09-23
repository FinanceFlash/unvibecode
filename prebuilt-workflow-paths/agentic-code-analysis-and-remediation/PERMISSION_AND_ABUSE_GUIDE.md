# Permission and Abuse Guide

## Permission boundaries

* Authorized people and systems initiate analysis sessions.
* Agent execution requires a sandboxed filesystem. Host access outside the repository must not happen.
* Destructive terminal commands require developer approval before execution.
* Transmission of repository credentials, secrets, and environment files to the LLM provider must not happen.
* Enforcement of token budget and iteration caps applies unconditionally across all stages.

## Misuse paths

* Autonomous token exhaustion (OWASP LLM04) — A looping or reflecting agent consumes unbounded tokens without reaching a terminal state.
* Excessive agency (OWASP LLM08) — Agent executes destructive shell commands, modifies host files, or commits unauthorized code.
* Prompt injection via repository content (OWASP LLM01) — Malicious code comments, README instructions, or config files redirect agent goals or override system prompts.
* Sensitive information disclosure (OWASP LLM06) — Agent reads .env, .pem, or credential files and transmits contents to the LLM provider.
* Sandbox escape — Agent uses path traversal, symlinks, or container breakout to access host filesystem.
* Supply chain poisoning — Agent proposes dependencies on non-existent or typo-squatted packages.
* Unauthorized branch push — Agent pushes code to a protected branch without required reviews or approvals.
* Audit evasion — Agent suppresses, truncates, or overwrites its own reflection logs and decision history.

Protect developer identity, repository scope, credentials, secrets, sandbox boundaries, token budgets, privileged tools, and audit records. Deny uncertain identity, ownership, scope, or authorization.
