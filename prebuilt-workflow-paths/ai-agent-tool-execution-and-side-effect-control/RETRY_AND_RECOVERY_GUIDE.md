\# Retry and Recovery Guide



\## Recovery boundary



Retry and recovery begin when a tool execution does not reach a clearly confirmed terminal outcome.



The system must distinguish:



\- confirmed success;

\- confirmed failure before side effect;

\- confirmed failure after partial side effect;

\- unknown outcome.



\## Retry classification



Before retrying, classify the failure.



\### Safe retry



A retry may be appropriate when:



\- the failure occurred before the side-effect boundary;

\- the operation is explicitly idempotent;

\- the tool contract guarantees safe repetition;

\- the operation has a unique idempotency key or equivalent protection.



\*\*Must not happen:\*\* A retry must not be performed merely because an error is present.



\### Unsafe or uncertain retry



Do not blindly retry when:



\- execution may already have reached the side-effect boundary;

\- the tool timed out without confirming completion;

\- the operation is non-idempotent;

\- the final state cannot be determined.



\*\*Must not happen:\*\* An uncertain side-effecting operation must not be repeated without an appropriate safety mechanism.



\## Idempotency



For retryable side-effecting operations, identify the mechanism that prevents duplicate effects.



Possible mechanisms include:



\- idempotency keys;

\- unique operation identifiers;

\- database uniqueness constraints;

\- transactional state transitions;

\- provider-supported idempotency;

\- explicit deduplication records.



The mechanism should be tied to the business operation rather than only to an individual network attempt.



\## Bounded retries



Retries should have explicit limits.



Define:



\- maximum attempts;

\- retryable error classes;

\- backoff behaviour;

\- timeout limits;

\- stopping conditions.



\*\*Must not happen:\*\* A tool failure must not create an unbounded retry loop.



\## Timeout recovery



A timeout means the caller did not receive a response within the configured period. It does not necessarily prove that execution stopped.



After a timeout, prefer:



1\. query execution status if supported;

2\. reconcile the target state;

3\. use the operation identifier to determine whether the request already completed;

4\. retry only when the operation is known to be safe.



\*\*Must not happen:\*\* A timeout must not automatically be treated as confirmed non-execution.



\## Partial completion



If an operation performs multiple effects and fails part way through, record the partial state.



Recovery may require:



\- rollback;

\- compensating action;

\- reconciliation;

\- manual intervention;

\- resuming from a safe checkpoint.



\*\*Must not happen:\*\* Partial completion must not silently become a false success.



\## Dependency failures



When a dependency is unavailable:



\- classify the dependency failure;

\- determine whether the side effect occurred;

\- retry only if safe;

\- preserve enough state for later recovery.



\*\*Must not happen:\*\* Dependency recovery must not duplicate an already completed business operation.



\## Recovery state



Where the final outcome cannot immediately be determined, use an explicit unresolved state rather than guessing.



A useful state model may distinguish:



`REQUESTED → RUNNING → SUCCEEDED`



and failure or uncertainty paths such as:



`REQUESTED → REJECTED`



`RUNNING → FAILED`



`RUNNING → PARTIAL`



`RUNNING → UNKNOWN`



The exact state model should match the application.



\## Reconciliation



A reconciliation process should use durable operation identity and authoritative state where possible.



Examples:



\- checking whether a record was created;

\- checking whether a mutation was committed;

\- querying an external provider for operation status;

\- comparing expected and actual state.



\*\*Must not happen:\*\* Reconciliation must not rely only on the absence of a response.



\## Recovery after process interruption



If the worker or application process terminates during execution, recovery should determine whether the operation:



\- never started;

\- completed;

\- partially completed;

\- remains unresolved.



Persisted operation state should support this determination where the business impact requires it.



\## Observability



Record non-sensitive information needed to diagnose recovery:



\- operation identifier;

\- tool identifier;

\- execution state;

\- attempt number;

\- relevant timestamps;

\- failure classification;

\- recovery decision.



Do not record credentials, secrets, or unnecessary sensitive tool arguments.



\## Manual repair



Some operations cannot be safely automated after an uncertain or partial outcome.



Define when manual intervention is required and what evidence the operator needs.



\*\*Must not happen:\*\* Operators must not be instructed to blindly repeat a potentially completed side-effecting action.



\## Recovery testing checklist



\- \[ ] Retryable failure retries safely

\- \[ ] Non-retryable failure stops

\- \[ ] Retry count is bounded

\- \[ ] Backoff is bounded

\- \[ ] Duplicate execution is prevented

\- \[ ] Timeout creates an appropriate uncertain state

\- \[ ] Partial completion is detectable

\- \[ ] Recovery can reconcile uncertain execution

\- \[ ] Process interruption is recoverable

\- \[ ] Manual repair path is defined where required

\- \[ ] Recovery evidence is observable

