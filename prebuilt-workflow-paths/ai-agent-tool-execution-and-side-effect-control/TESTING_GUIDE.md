\# Testing Guide



Each scenario should verify both the expected outcome and the `Must not happen` condition.



Use unit tests for validation and policy decisions, integration tests for tool execution and state changes, and end-to-end tests where the complete agent-to-tool path is business-critical.



\## 01. Valid read-only tool execution



\*\*Given:\*\* A registered read-only tool and valid arguments.



\*\*When:\*\* The agent requests the tool.



\*\*Expect:\*\* The tool executes and returns a valid result.



\*\*Must not happen:\*\* An unrelated tool or operation is executed.



\*\*Suggested test level:\*\* Unit + integration.



\---



\## 02. Valid side-effecting tool execution



\*\*Given:\*\* A registered side-effecting tool and an authorized request.



\*\*When:\*\* The agent invokes the tool.



\*\*Expect:\*\* The intended state change occurs exactly as specified.



\*\*Must not happen:\*\* An unintended resource is modified.



\*\*Suggested test level:\*\* Integration.



\---



\## 03. Unknown tool rejection



\*\*Given:\*\* A tool request references an unavailable tool.



\*\*When:\*\* The request reaches validation.



\*\*Expect:\*\* The request is rejected before execution.



\*\*Must not happen:\*\* Dynamic input must not create an executable tool.



\*\*Suggested test level:\*\* Unit.



\---



\## 04. Missing required argument



\*\*Given:\*\* A registered tool requires an argument that is absent.



\*\*When:\*\* The agent submits the request.



\*\*Expect:\*\* Validation fails before execution.



\*\*Must not happen:\*\* The tool must not perform a side effect using incomplete input.



\*\*Suggested test level:\*\* Unit.



\---



\## 05. Invalid argument type or value



\*\*Given:\*\* A tool receives an invalid argument type, format, or value.



\*\*When:\*\* The request is validated.



\*\*Expect:\*\* Validation rejects the request.



\*\*Must not happen:\*\* Invalid input must not reach the execution boundary.



\*\*Suggested test level:\*\* Unit.



\---



\## 06. Unauthorized operation



\*\*Given:\*\* A valid tool request that the execution context is not permitted to perform.



\*\*When:\*\* Authorization is evaluated.



\*\*Expect:\*\* The operation is denied before execution.



\*\*Must not happen:\*\* The tool must not perform the protected operation.



\*\*Suggested test level:\*\* Unit + integration.



\---



\## 07. Unauthorized resource access



\*\*Given:\*\* The caller can use a tool but cannot access the requested resource.



\*\*When:\*\* The request targets that resource.



\*\*Expect:\*\* Resource-level authorization rejects it.



\*\*Must not happen:\*\* The tool must not access another user's or tenant's resource.



\*\*Suggested test level:\*\* Integration.



\---



\## 08. Policy-blocked high-impact action



\*\*Given:\*\* A structurally valid request violates an applicable high-impact policy.



\*\*When:\*\* Policy checks run.



\*\*Expect:\*\* Execution is blocked and the decision is observable.



\*\*Must not happen:\*\* Tool availability must not bypass the policy.



\*\*Suggested test level:\*\* Unit + integration.



\---



\## 09. Concurrent execution on the same resource



\*\*Given:\*\* Two valid requests target the same mutable resource concurrently.



\*\*When:\*\* Both executions run.



\*\*Expect:\*\* The application's defined concurrency guarantee is preserved.



\*\*Must not happen:\*\* Updates must not be silently lost or leave contradictory state.



\*\*Suggested test level:\*\* Integration + concurrency test.



\---



\## 10. Duplicate tool request



\*\*Given:\*\* The same side-effecting request is submitted twice with the same operation identity.



\*\*When:\*\* Both requests are processed.



\*\*Expect:\*\* Idempotency or deduplication prevents an unintended duplicate effect.



\*\*Must not happen:\*\* One logical operation must not create two business effects.



\*\*Suggested test level:\*\* Integration.



\---



\## 11. Tool timeout before confirmed completion



\*\*Given:\*\* A side-effecting tool exceeds its timeout without a confirmed result.



\*\*When:\*\* The timeout is handled.



\*\*Expect:\*\* The execution is represented as uncertain when completion cannot be established.



\*\*Must not happen:\*\* The timeout must not automatically be treated as confirmed non-execution.



\*\*Suggested test level:\*\* Integration.



\---



\## 12. Tool failure before side effect



\*\*Given:\*\* The tool fails before reaching its side-effect boundary.



\*\*When:\*\* The failure is returned.



\*\*Expect:\*\* The operation is reported as failed and the protected state remains unchanged.



\*\*Must not happen:\*\* The system must not report success.



\*\*Suggested test level:\*\* Integration.



\---



\## 13. Tool failure after partial side effect



\*\*Given:\*\* A tool performs a partial operation and then fails.



\*\*When:\*\* The failure is handled.



\*\*Expect:\*\* The partial state is detected and the defined recovery or reconciliation path is triggered.



\*\*Must not happen:\*\* Partial completion must not be silently treated as either full success or no execution.



\*\*Suggested test level:\*\* Integration.



\---



\## 14. Malformed tool result



\*\*Given:\*\* A tool returns data that violates its result contract.



\*\*When:\*\* Result validation runs.



\*\*Expect:\*\* The result is rejected or marked invalid.



\*\*Must not happen:\*\* Downstream code must not treat the malformed result as successful execution.



\*\*Suggested test level:\*\* Unit.



\---



\## 15. Sensitive result handling



\*\*Given:\*\* A tool returns sensitive data that is not required for the next agent step.



\*\*When:\*\* The result is passed through the result-handling layer.



\*\*Expect:\*\* The configured exposure policy is applied.



\*\*Must not happen:\*\* Unnecessary sensitive information must not be exposed to the agent.



\*\*Suggested test level:\*\* Unit + integration.



\---



\## 16. Cross-tenant or cross-user access attempt



\*\*Given:\*\* A valid tool request contains a resource identifier belonging to another user or tenant.



\*\*When:\*\* Resource authorization runs.



\*\*Expect:\*\* Access is denied.



\*\*Must not happen:\*\* Manipulating the resource identifier must not bypass isolation.



\*\*Suggested test level:\*\* Integration + security test.



\---



\## 17. Dependency unavailable



\*\*Given:\*\* A required dependency is unavailable.



\*\*When:\*\* The tool attempts execution.



\*\*Expect:\*\* The operation fails safely and its outcome is recorded.



\*\*Must not happen:\*\* Dependency failure must not produce false success or an uncontrolled partial effect.



\*\*Suggested test level:\*\* Integration.



\---



\## 18. Safe retry after retryable failure



\*\*Given:\*\* A tool returns an explicitly retryable failure.



\*\*When:\*\* Retry handling processes the failure.



\*\*Expect:\*\* The operation is retried only within the configured retry policy and only when safe.



\*\*Must not happen:\*\* Retries must not become unbounded or duplicate unsafe side effects.



\*\*Suggested test level:\*\* Unit + integration.



\---



\## 19. Recovery after uncertain execution



\*\*Given:\*\* A side-effecting request has an unknown final status.



\*\*When:\*\* Recovery or reconciliation is initiated.



\*\*Expect:\*\* The system determines or safely reconciles the final state.



\*\*Must not happen:\*\* Recovery must not blindly repeat an operation that may already have succeeded.



\*\*Suggested test level:\*\* Integration + recovery test.



\---



\## 20. Audit and outcome consistency



\*\*Given:\*\* A tool request reaches a terminal outcome.



\*\*When:\*\* The execution record is created or updated.



\*\*Expect:\*\* The recorded outcome matches the observed execution state.



\*\*Must not happen:\*\* A rejected, failed, or uncertain operation must not be recorded as successful.



\*\*Suggested test level:\*\* Unit + integration.



\## Test data and isolation



Tests should use isolated resources and synthetic credentials or identities.



Do not place real credentials, API keys, customer data, or proprietary information in test fixtures.



\## Regression expectations



When changing tool validation, authorization, execution, retry, or recovery behaviour, rerun all affected scenarios and the repository's complete quality suite.



A passing happy-path test alone is not sufficient evidence for side-effecting tool workflows.

