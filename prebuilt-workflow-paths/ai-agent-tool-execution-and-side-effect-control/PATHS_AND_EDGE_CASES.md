\# Paths and Edge Cases



\## Supported paths



\### 1. Read-only execution

A registered read-only tool receives valid arguments and returns a valid result.



\### 2. Side-effecting execution

An authorized tool modifies the intended resource and returns a validated success result.



\### 3. Repeated execution

The same logical request is received more than once and is handled according to the operation's idempotency policy.



\### 4. Retryable failure

A retryable failure occurs and the operation is retried only when retrying is safe.



\### 5. Recovery

Execution ends in an uncertain or partial state and the system uses status checking, reconciliation, or another defined recovery path.



\## Validation edge cases



\- Unknown tool name

\- Missing required argument

\- Unexpected argument

\- Wrong argument type

\- Invalid identifier

\- Invalid enum or unsupported value

\- Oversized input

\- Empty input where prohibited

\- Malformed structured input



\*\*Must not happen:\*\* Invalid requests must not reach a protected side-effect boundary.



\## Permission edge cases



\- Valid tool but unauthorized operation

\- Authorized operation against an unauthorized resource

\- Cross-user resource identifier

\- Cross-tenant resource identifier

\- Expired or invalid execution context

\- Policy-blocked high-impact operation



\*\*Must not happen:\*\* Tool availability must not bypass resource-level authorization or policy checks.



\## Timing edge cases



\- Tool timeout before execution

\- Timeout after execution may have started

\- Slow dependency

\- Concurrent requests for the same resource

\- Retry arriving while the first execution is still unresolved



\*\*Must not happen:\*\* Timing uncertainty must not cause duplicate or contradictory business effects.



\## Execution edge cases



\- Tool unavailable

\- Tool throws an exception

\- Dependency unavailable

\- Tool partially completes

\- Tool returns an invalid result

\- Tool returns a valid failure result

\- Tool returns success with incomplete data



\*\*Must not happen:\*\* Failure or malformed output must not be promoted to confirmed success.



\## Side-effect edge cases



Side-effecting operations should be classified before implementation or review.



Examples include:



\- creating a record;

\- modifying a record;

\- deleting a record;

\- sending a message;

\- changing access or entitlement;

\- triggering another business action.



For each operation, identify whether duplicate execution is safe.



\*\*Must not happen:\*\* A retry must not blindly repeat an operation whose first execution may already have succeeded.



\## Sensitive-data edge cases



\- Tool returns credentials or secrets

\- Tool returns another user's data

\- Tool returns unnecessary personal information

\- Tool result contains internal implementation details

\- Tool arguments contain sensitive information



\*\*Must not happen:\*\* Sensitive information must not be exposed beyond the minimum required execution context.



\## Recovery edge cases



\### Confirmed failure



The tool definitively reports that the protected operation did not occur.



\*\*Expected:\*\* Record failure and follow the normal retry policy if applicable.



\### Confirmed success



The tool definitively reports successful completion.



\*\*Expected:\*\* Record success and make the validated result available downstream.



\### Unknown outcome



The system cannot determine whether the operation completed.



\*\*Expected:\*\* Mark the operation as unresolved and use a safe status or reconciliation mechanism.



\*\*Must not happen:\*\* Unknown outcome must not be treated as confirmed failure merely because the request timed out.



\### Partial completion



Some effects occurred before execution failed.



\*\*Expected:\*\* Preserve evidence of the partial state and use the defined recovery or reconciliation path.



\*\*Must not happen:\*\* Partial completion must not be silently discarded.



\## Boundary conditions



The workflow begins when an agent has produced a tool request.



The workflow ends when the tool operation has a confirmed terminal outcome or is explicitly placed into an unresolved/recovery state.



The workflow does not own the complete lifecycle of:



\- general LLM generation;

\- RAG retrieval and citation grounding;

\- human approval;

\- scheduled execution;

\- external-system synchronization.



Those workflows should use their corresponding packs.



\## Review checklist



Before considering the workflow complete, verify:



\- \[ ] Tool is registered.

\- \[ ] Arguments are validated.

\- \[ ] Authorization is checked.

\- \[ ] Resource access is authorized.

\- \[ ] Side effects are identified.

\- \[ ] Duplicate execution is considered.

\- \[ ] Timeout behaviour is defined.

\- \[ ] Partial completion is handled.

\- \[ ] Results are validated.

\- \[ ] Sensitive results are controlled.

\- \[ ] Recovery is defined for uncertain execution.

\- \[ ] Terminal outcomes are recorded.

