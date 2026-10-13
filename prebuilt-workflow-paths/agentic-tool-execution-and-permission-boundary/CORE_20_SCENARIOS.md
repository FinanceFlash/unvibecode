# Core 20 Scenarios

| # | Scenario | Must not happen |
|---:|---|---|
| 1 | Valid tool request with complete arguments executes successfully | Tool output is lost or malformed result reaches the agent |
| 2 | Unregistered tool name is requested | Arbitrary command or unapproved function is invoked |
| 3 | Tool arguments violate JSON schema | Unvalidated payload triggers runtime unhandled crash |
| 4 | High-risk tool requires human approval | Destructive side effect runs without explicit user confirmation |
| 5 | Human rejects tool confirmation prompt | Rejected tool executes anyway or session hangs |
| 6 | Requester session lacks required permission scope | Escalated tool action modifies unauthorized tenant resources |
| 7 | Prompt injection in argument payload attempts command injection | Host shell commands or path traversal execute |
| 8 | Tool execution exceeds allotted CPU time limit | Long-running task blocks worker pool indefinitely |
| 9 | Tool execution exceeds RAM allocation | Out-of-memory error crashes host orchestrator process |
| 10 | Tool returns sensitive internal credentials | Raw tokens or private secrets leak into LLM context |
| 11 | External API dependency fails during execution | Failure causes cascade crash without structured error return |
| 12 | Duplicate tool request submitted concurrently | Idempotent operation runs multiple times producing duplicate side effects |
| 13 | Maximum tool call iteration depth reached | Infinite agent loop consumes system budget and rate limits |
| 14 | Network access restricted to allowlisted endpoints | Tool connects to unauthorized internal subnet or metadata IP |
| 15 | Partial tool execution fails mid-operation | Incomplete database changes persist without rollback |
| 16 | Tool output exceeds maximum response size | Unbounded response crashes context memory parser |
| 17 | Tool invocation audit logging fails | Tool executes without leaving verifiable audit evidence |
| 18 | Session revoked while tool execution in progress | Disconnected user session receives finished tool output |
| 19 | Rate limit reached for targeted tool | Exceeded limit allows request flooding or resource starvation |
| 20 | Tool execution retries after transient failure | Retry bypasses permission check or duplicates non-idempotent action |

Full details are in [TESTING_GUIDE.md](TESTING_GUIDE.md).
