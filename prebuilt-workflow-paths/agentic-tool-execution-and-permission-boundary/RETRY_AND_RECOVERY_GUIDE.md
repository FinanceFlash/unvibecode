# Retry and Recovery Guide

## Transient Failure Management

1. **Network Retries**: For read-only tools connecting to external APIs, implement exponential backoff with jitter (max 3 retries, base delay 500ms).
2. **Non-Idempotent Mutations**: Never automatically retry tools with state-changing side effects (e.g., `process_payment`, `send_sms`) unless an explicit idempotency key was confirmed by the downstream target.
3. **Sandbox Recovery**: If a worker sandbox process crashes due to memory overflow, terminate the container cleanly, mark the execution as `FAILED_SANDBOX`, and return a graceful error message to the orchestrator to prevent container leakage.

## Recovery Procedures

- **Stuck State Cleanup**: A background reaper process scans for tool executions stuck in `RUNNING` status longer than 60 seconds and marks them `TIMED_OUT`.
- **Fallbacks**: When a primary tool fails, the orchestrator may return a structured error payload advising the LLM of the specific constraint rather than throwing an unhandled exception.
