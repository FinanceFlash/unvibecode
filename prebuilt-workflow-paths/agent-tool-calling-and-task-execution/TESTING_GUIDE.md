# Testing Guide

1. **Successful Execution**: Given valid task, When executed, Expect success, Must not happen: Task fails silently.
2. **Missing Tool**: Given request for fake tool, When selected, Expect error, Must not happen: System crashes.
3. **Invalid Arguments**: Given malformed args, When authorized, Expect validation error, Must not happen: Tool executes with bad data.
4. **Unauthorized Tool**: Given restricted tool, When requested, Expect denial, Must not happen: Privilege escalation.
5. **Tool Timeout**: Given slow tool, When executed, Expect timeout, Must not happen: Agent hangs indefinitely.
6. **Tool Error**: Given tool fault, When executed, Expect handled error, Must not happen: Unhandled exception.
7. **Rate Limit Exceeded**: Given rate limit, When hit, Expect backoff, Must not happen: Quota exhaustion.
8. **Max Steps Exceeded**: Given complex task, When step limit reached, Expect escalation, Must not happen: Infinite loop.
9. **Ambiguous Task**: Given vague input, When planned, Expect clarification, Must not happen: Agent guesses.
10. **Partial Failure Recovery**: Given minor failure, When executing, Expect recovery, Must not happen: Unnecessary failure.
11. **Malicious Instruction**: Given injection, When received, Expect rejection, Must not happen: Payload execution.
12. **Context Window Overflow**: Given huge output, When validating, Expect truncation, Must not happen: LLM rejection.
13. **Idempotency Key Conflict**: Given retry, When executed, Expect safety, Must not happen: Duplicate side effect.
14. **Service Unavailability**: Given LLM outage, When planning, Expect graceful failure, Must not happen: Data loss.
15. **Concurrent Task Conflict**: Given concurrent edits, When executing, Expect lock/conflict handling, Must not happen: Data corruption.
16. **Task Cancellation**: Given cancel signal, When processing, Expect halt, Must not happen: Continued execution.
17. **Tool Registry Update**: Given schema change, When selecting, Expect schema sync, Must not happen: Schema mismatch crash.
18. **Unsafe Tool Chaining**: Given chained tools, When executing, Expect sanitization, Must not happen: Command injection.
19. **Escalation Triggered**: Given stuck agent, When escalated, Expect human notification, Must not happen: Limbo state.
20. **Audit Log Failure**: Given audit outage, When executing, Expect halt, Must not happen: Un-audited action.
