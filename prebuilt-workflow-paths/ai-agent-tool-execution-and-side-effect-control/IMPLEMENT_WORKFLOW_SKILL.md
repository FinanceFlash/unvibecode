---

name: implement_ai_agent_tool_execution_workflow

description: Implement or modify AI agent tool execution while preserving validation, authorization, side-effect safety, idempotency, result handling, and recovery.

---



# Implement AI Agent Tool Execution Workflow



## Purpose



Implement or modify an AI agent tool-execution workflow while preserving the business boundary and preventing unsafe or duplicate side effects.



## Workflow boundary



Work within:



`tool request → validation → authorization → execution → result validation → outcome/recovery`



Do not introduce unrelated workflow behaviour unless the existing implementation requires it.



## Before changing code



First identify:



- tool registry;

- tool schemas;

- request creation;

- validation layer;

- authorization layer;

- side-effect boundary;

- execution handler;

- result handling;

- retry and recovery logic;

- relevant tests.



Use repository evidence rather than assumptions.



## Implementation requirements



### Tool registration



Only explicitly registered tools should be executable.



**Must not happen:** Arbitrary or unregistered tool names must not reach execution.



### Input validation



Validate:



- tool identity;

- required arguments;

- argument types;

- allowed values;

- resource identifiers;

- constraints required by the business operation.



Validation must occur before protected side effects.



**Must not happen:** Invalid tool arguments must not trigger a business side effect.



### Authorization



Enforce authorization for the requested operation and target resource.



Consider:



- authenticated identity;

- role or permission;

- ownership;

- tenant;

- resource scope;

- policy restrictions.



Authorization must happen before the side-effect boundary.



**Must not happen:** A caller must not modify or access a resource outside its authorized scope.



### Side-effect protection



Identify whether execution:



- creates;

- updates;

- deletes;

- sends;

- charges;

- publishes;

- changes access;

- triggers another business action.



For high-impact operations, preserve appropriate confirmation, policy, or idempotency mechanisms already required by the application.



### Idempotency



For retryable side-effecting operations, use an appropriate mechanism such as:



- idempotency keys;

- unique operation identifiers;

- uniqueness constraints;

- transactional state transitions;

- provider-supported idempotency.



**Must not happen:** Repeating the same logical operation must not unintentionally duplicate its business effect.



### Result validation



Validate tool output before downstream code treats it as successful.



Distinguish:



- successful execution;

- explicit failure;

- malformed result;

- unknown outcome.



**Must not happen:** An invalid or uncertain result must not be treated as confirmed success.



## Error handling



Preserve meaningful error classification.



Do not hide:



- authorization failures;

- validation failures;

- dependency failures;

- timeout conditions;

- partial completion;

- unknown execution outcomes.



## Retry behaviour



Only retry when the operation is known to be safe or protected by an appropriate idempotency mechanism.



Use bounded attempts and appropriate backoff.



**Must not happen:** A failed tool call must not create an unbounded retry loop.



## Timeout behaviour



A timeout does not necessarily mean the operation did not execute.



Where supported:



1. identify the operation;

2. query or reconcile its state;

3. determine whether the side effect occurred;

4. retry only when safe.



## Recovery



Preserve or introduce explicit recovery states when the final outcome is uncertain.



Support reconciliation or compensation where required by the business operation.



## Testing



For every implementation change, add or update tests covering:



- valid execution;

- invalid tool;

- invalid arguments;

- unauthorized access;

- resource boundary;

- side-effect execution;

- duplicate execution;

- retry;

- timeout;

- partial failure;

- malformed result;

- recovery.



## Change discipline



Prefer the smallest complete change.



Do not weaken existing authorization, validation, state management, or recovery controls to simplify implementation.



Do not claim a safeguard exists unless the code and tests support it.



## Completion checklist



- [ ] Tool registration is enforced

- [ ] Arguments are validated

- [ ] Authorization precedes protected side effects

- [ ] Side-effect boundary is understood

- [ ] Duplicate execution is controlled

- [ ] Retries are bounded

- [ ] Timeouts are handled safely

- [ ] Results are validated

- [ ] Partial/unknown outcomes are represented

- [ ] Recovery behaviour is tested

- [ ] Existing tests remain passing

