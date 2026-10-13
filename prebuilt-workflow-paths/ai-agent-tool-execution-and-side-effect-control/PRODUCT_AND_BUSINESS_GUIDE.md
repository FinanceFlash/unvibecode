\# Product and Business Guide



\## People and systems



\- \*\*End user or requesting application\*\* — provides the task that may require a tool operation.

\- \*\*AI agent\*\* — decides whether a tool is needed and proposes the tool request.

\- \*\*Tool registry or tool provider\*\* — defines which tools are available and their accepted inputs.

\- \*\*Policy and authorization layer\*\* — determines whether the requested operation is permitted.

\- \*\*Tool execution environment\*\* — performs the approved operation.

\- \*\*Target resource or service\*\* — the resource affected by a side-effecting operation.

\- \*\*Observability or audit system\*\* — records enough execution information to understand the outcome.



\## Things created or changed



\- Agent tool request

\- Validated tool arguments

\- Authorization decision

\- Execution record

\- Tool result

\- Target resource when the operation has an approved side effect

\- Failure or recovery state when execution does not complete normally



\## Stages



\### 1. Tool selection



The agent identifies an available tool that can contribute to the requested task.



\*\*Decision:\*\* Is the selected tool appropriate for the requested operation?



\*\*Must not happen:\*\* The system must not execute an unrelated or unavailable tool because the agent selected it incorrectly.



\### 2. Request validation



The system validates the tool name, required arguments, argument types, allowed values, and resource identifiers.



\*\*Decision:\*\* Is the request structurally valid?



\*\*Must not happen:\*\* Invalid or malformed tool arguments must not reach a side-effecting execution path.



\### 3. Authorization and policy check



The system evaluates whether the requested operation is permitted for the current execution context.



Relevant factors may include the requesting identity, agent permissions, tool permissions, target resource, operation type, and applicable business policy.



\*\*Decision:\*\* Is this exact operation permitted?



\*\*Must not happen:\*\* An agent must not gain authority merely because it can construct a syntactically valid tool request.



\### 4. Execution preparation



The system establishes the execution context and any safeguards required for the operation.



For side-effecting operations, the system should determine whether an idempotency key, transaction boundary, concurrency control, or other protection is required.



\*\*Must not happen:\*\* An operation requiring execution safeguards must not bypass those safeguards.



\### 5. Tool execution



The authorized operation is executed against the intended target.



\*\*Decision:\*\* Did execution start and complete according to the tool contract?



\*\*Must not happen:\*\* A rejected request must not produce the protected side effect.



\### 6. Result validation



The system validates the returned status and result before treating it as successful.



\*\*Must not happen:\*\* A malformed, ambiguous, or failed result must not be represented downstream as a confirmed successful operation.



\### 7. Outcome recording



The system records the relevant execution outcome.



The record should distinguish successful execution, rejection, validation failure, timeout, tool failure, and uncertain or partially completed execution where applicable.



\*\*Must not happen:\*\* An execution outcome must not be silently lost when it is needed for troubleshooting, reconciliation, or recovery.



\## Core business decisions



\### Read-only versus side-effecting tools



Read-only operations can generally be evaluated differently from operations that modify data, trigger external actions, spend resources, or change user-visible state.



The application should identify which tools can create externally visible effects.



\### Least privilege



A tool should receive only the permissions required for its intended operation.



The ability of an agent to invoke a tool does not by itself establish permission to access every resource that tool can reach.



\### User-visible effects



Where an operation changes user-visible or business-critical state, product requirements should define:



\- who may request the operation;

\- which resources may be affected;

\- whether confirmation is required;

\- what counts as success;

\- what happens when execution is uncertain;

\- how duplicate execution is prevented or reconciled.



\## Supported paths



\- Valid read-only tool request

\- Valid side-effecting tool request

\- Invalid tool name

\- Invalid or incomplete arguments

\- Unauthorized operation

\- Tool unavailable

\- Tool timeout

\- Tool-reported failure

\- Malformed tool result

\- Duplicate execution attempt

\- Partially completed operation

\- Recovery or reconciliation after uncertain execution



\## Acceptance criteria



A conforming implementation should be able to demonstrate that:



1\. only registered tools can be selected for execution;

2\. tool arguments are validated before execution;

3\. authorization is evaluated before protected side effects;

4\. side-effecting operations use appropriate duplicate-execution protection;

5\. failed or rejected requests do not appear successful;

6\. tool results are validated before downstream use;

7\. execution outcomes can be distinguished and investigated;

8\. uncertain execution can be recovered or reconciled without blindly repeating a side effect.



\## Business-risk questions



Before adopting this workflow, product and engineering teams should answer:



\- Which tools can change business-critical state?

\- Which users, agents, or services may invoke each tool?

\- Which actions require additional confirmation or policy checks?

\- Which operations must be idempotent?

\- What is the expected behaviour after a timeout when the tool may already have executed?

\- Which results are safe to expose to the agent?

\- Which execution evidence must be retained for troubleshooting or audit?



\## Boundary reminders



This guide does not define general LLM generation, retrieval grounding, human approval, scheduled execution, or external-system synchronization as independent workflows. When those lifecycles become the primary business outcome, use the corresponding workflow pack instead.

