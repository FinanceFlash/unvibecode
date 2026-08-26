# Core 20 Scenarios

| # | Scenario | Trigger | Stage | Expected | Must not happen |
|---|---|---|---|---|---|
| 1 | Successful Execution | Valid task | Completion/Escalation | Success | Task fails silently |
| 2 | Missing Tool | Agent requests non-existent tool | Tool Selection | Error to agent | System crashes |
| 3 | Invalid Arguments | Agent provides malformed arguments | Authorization | Validation error | Tool executes with bad data |
| 4 | Unauthorized Tool | Agent lacks permission for tool | Authorization | Denied | Privilege escalation |
| 5 | Tool Timeout | Tool takes too long | Execution | Timeout error to agent | Agent hangs indefinitely |
| 6 | Tool Error | Tool returns error | Result Validation | Error logged and passed to agent | Unhandled exception crashes orchestrator |
| 7 | Rate Limit Exceeded | Too many tool calls | Execution | Backoff and retry | Quota exhaustion without backoff |
| 8 | Max Steps Exceeded | Agent loops too many times | Planning | Escalation | Infinite loop |
| 9 | Ambiguous Task | User input lacks detail | Planning | Ask for clarification | Agent guesses critical parameters |
| 10 | Partial Failure Recovery | One step fails, others succeed | Execution | Agent adjusts plan | Whole task fails if recoverable |
| 11 | Malicious Instruction | Prompt injection attempt | Task Received | Rejected | Agent executes malicious payload |
| 12 | Context Window Overflow | Tool output too large | Result Validation | Truncation or summarization | LLM provider rejects subsequent calls |
| 13 | Idempotency Key Conflict | Retry of stateful tool | Execution | Safe retry | Duplicate side effect |
| 14 | Service Unavailability | LLM provider down | Planning | Retry or fail gracefully | Data loss of Task Request |
| 15 | Concurrent Task Conflict | Two agents edit same resource | Execution | Concurrency control handles it | Data corruption |
| 16 | Task Cancellation | User aborts | Any | Graceful halt | Agent continues executing side effects |
| 17 | Tool Registry Update | Tool changed during execution | Tool Selection | Agent uses new schema or fails gracefully | Schema mismatch crash |
| 18 | Unsafe Tool Chaining | Output of tool A used directly in tool B unsafely | Execution | Validation catches unsafe injection | Command injection |
| 19 | Escalation Triggered | Agent cannot proceed | Completion/Escalation | Human notified | Task stuck in limbo |
| 20 | Audit Log Failure | Cannot write to audit log | Authorization/Execution | Halt execution | Silent un-audited action |
