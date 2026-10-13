---

name: test_ai_agent_tool_execution_workflow

description: Design and review tests for AI agent tool execution, covering validation, authorization, side effects, idempotency, failures, concurrency, retries, and recovery.

---



# Test AI Agent Tool Execution Workflow



## Purpose



Design tests that verify an AI agent can safely request and execute tools without causing unauthorized, duplicate, invalid, or unrecoverable business effects.



## Workflow boundary



Test:



`tool request → validation → authorization → execution → result validation → outcome/recovery`



Keep adjacent workflows separate unless the application explicitly crosses this boundary.



## Test evidence



Each test should identify:



- setup;

- relevant actor;

- tool;

- arguments;

- target resource;

- expected state;

- expected result;

- failure condition;

- what must not happen.



## Core test categories



### 1. Valid tool execution



Verify a registered tool executes with valid arguments.



**Must not happen:** A valid request must not be rejected because of unrelated validation.



### 2. Unknown tool



Request a tool that is not registered.



**Must not happen:** The unknown tool must not execute.



### 3. Invalid arguments



Provide missing, malformed, or invalid arguments.



**Must not happen:** Invalid arguments must not reach the side-effect boundary.



### 4. Unauthorized execution



Use an actor without permission.



**Must not happen:** The protected operation must not execute.



### 5. Resource isolation



Attempt to access another user's or tenant's resource.



**Must not happen:** Cross-resource or cross-tenant access must not occur.



### 6. Read-only tool



Execute a tool expected to have no side effect.



Verify that business state remains unchanged.



### 7. Side-effecting tool



Execute a tool that creates or modifies business state.



Verify the expected state transition.



### 8. Duplicate request



Submit the same logical operation more than once.



**Must not happen:** The business effect must not be duplicated when idempotency is required.



### 9. Concurrent requests



Execute equivalent operations concurrently.



Check:



- race conditions;

- uniqueness;

- state transitions;

- locking or transactional behaviour.



**Must not happen:** Concurrent execution must not create contradictory or duplicate state.



### 10. Dependency failure



Make a required dependency fail.



**Must not happen:** The application must not report success when the required operation did not complete.



### 11. Timeout



Cause the tool or dependency to exceed its timeout.



Verify that the final outcome is not incorrectly assumed.



**Must not happen:** A timeout must not automatically cause a duplicate retry.



### 12. Retry



Trigger a retryable failure.



Verify bounded retry behaviour and backoff where applicable.



**Must not happen:** Retries must not become unbounded or duplicate side effects.



### 13. Non-retryable failure



Trigger an error that should stop execution.



**Must not happen:** The operation must not continue through unsafe retries.



### 14. Partial completion



Cause execution to fail after one or more effects have occurred.



Verify that partial state is detected and handled.



**Must not happen:** Partial completion must not be silently reported as full success.



### 15. Malformed tool result



Return an invalid or incomplete result.



**Must not happen:** Downstream code must not treat malformed output as confirmed success.



### 16. Process interruption



Interrupt execution during the operation.



Verify that restart or recovery can determine the outcome where required.



### 17. Recovery and reconciliation



Provide an uncertain execution state and run the recovery path.



Verify that authoritative state is used to determine the result.



**Must not happen:** Recovery must not blindly repeat a potentially completed operation.



### 18. Sensitive data handling



Use inputs or outputs containing sensitive information.



Verify that logs and errors do not expose unnecessary secrets or private data.



### 19. Policy boundary



Test an operation restricted by application policy.



Verify that policy is evaluated before the protected side effect.



### 20. Terminal outcome



Verify that success, failure, and unresolved outcomes are represented distinctly.



**Must not happen:** An unresolved operation must not be presented as confirmed success.



## Test levels



Use the appropriate level:



- unit tests for validation and decision logic;

- integration tests for tool execution and persistence;

- end-to-end tests for complete agent-to-tool flows;

- concurrency tests for race conditions;

- recovery tests for partial and uncertain outcomes.



## Test design rules



Tests should verify observable business state, not only internal function calls.



Prefer assertions such as:



- resource was created exactly once;

- unauthorized resource remained unchanged;

- operation state became unresolved;

- retry count remained within the configured bound;

- recovery reconciled the authoritative state.



## Regression testing



Every bug fix should include a regression test that reproduces the original failure before verifying the fix.



Do not remove existing coverage for authorization, validation, idempotency, or recovery.



## Final checklist



- [ ] Happy path covered

- [ ] Invalid input covered

- [ ] Unauthorized path covered

- [ ] Resource isolation covered

- [ ] Side-effect boundary covered

- [ ] Duplicate execution covered

- [ ] Concurrency covered

- [ ] Dependency failure covered

- [ ] Timeout covered

- [ ] Retry covered

- [ ] Partial completion covered

- [ ] Recovery covered

- [ ] Sensitive data handling covered

- [ ] Terminal outcomes covered

- [ ] Regression test added for changed behaviour

