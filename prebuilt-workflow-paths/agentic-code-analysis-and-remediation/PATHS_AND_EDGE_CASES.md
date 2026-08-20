# Paths and Edge Cases

## Supported paths
- Single-pass analysis with successful AST extraction and report generation
- Multi-iteration reflection loop with convergence and bounded token consumption
- Graceful quota exhaustion with partial-result delivery and explicit status
- Skipped unreadable or permission-denied files with logged warnings
- Blocked destructive commands with developer approval gate
- Rejected prompt injection from malicious repository content
- Mid-session cancellation with immediate resource release
- Provider timeout with exponential backoff and bounded retry

## Normal paths
- A valid repository is analyzed successfully and produces a complete report
- A remediation proposal passes validation and is submitted as a pull request
- Token quota is consumed within limits and the session terminates normally

## Denied paths
- Required repository access credentials are missing or revoked
- Token budget or iteration cap is exceeded before reaching a conclusion
- Agent attempts to execute an unapproved destructive command
- Repository content overrides system prompt boundaries via injection
- Agent attempts path traversal or symlink escape beyond the sandbox

## Timing, concurrency, and boundaries
- Two analysis sessions target the same repository and branch simultaneously
- Token usage is tested just below, at, and above the configured budget limit
- Provider model version or policy changes between reflection iterations
- Repository index changes during an active analysis session
- Cancellation signal arrives after a remediation proposal has been submitted but before VCS confirmation

Cover valid, invalid, duplicate, stale, replayed, repeated, simultaneous, partially completed, unauthorized, exhausted, and recovery outcomes.
