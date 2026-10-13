---

name: review_ai_agent_tool_execution_business_risk

description: Review AI agent tool execution for evidence-backed customer, revenue, privacy, security, and operational risks without treating generic possibilities as confirmed defects.

---



# Review AI Agent Tool Execution Business Risk



## Purpose



Review an AI agent tool-execution workflow for business risks caused by incorrect tool selection, unsafe execution, authorization failures, duplicate side effects, unreliable results, or incomplete recovery.



The goal is to identify risks supported by concrete evidence rather than assuming that a missing control exists.



## Workflow boundary



Review the path from:



`agent tool request → validation → authorization → execution → result validation → outcome/recovery`



Do not expand the review into general LLM generation, RAG retrieval, human approval, scheduled execution, or external-system synchronization unless the supplied evidence shows that the issue crosses this workflow boundary.



## Evidence requirements



For every material risk, identify evidence such as:



- file path;

- symbol or function;

- configuration;

- test;

- runtime behaviour;

- relevant input/output;

- state transition;

- externally visible effect.



Do not report a risk solely because a generic best practice is absent.



Clearly distinguish:



- **Observed behaviour**

- **Business consequence**

- **Evidence**

- **Uncertainty or investigation gap**



## Risk review sequence



### 1. Identify tool capabilities



Determine which tools can:



- read data;

- modify data;

- delete data;

- send communications;

- change access;

- trigger business actions;

- create other externally visible effects.



### 2. Trace authorization



Determine whether the actual requested operation and target resource are authorized before the side effect occurs.



Look for:



- identity checks;

- permission checks;

- resource ownership;

- tenant boundaries;

- policy enforcement.



### 3. Trace side effects



Identify the exact code path that changes business state.



Determine whether validation and authorization occur before that boundary.



### 4. Review duplicate execution



Inspect retries, repeated requests, idempotency keys, deduplication, and unique constraints.



Consider whether a repeated request could create:



- duplicate records;

- duplicate notifications;

- duplicate financial effects;

- repeated destructive actions;

- contradictory state.



### 5. Review uncertain execution



Pay particular attention to:



- timeouts;

- connection failures;

- worker interruption;

- partial completion;

- ambiguous tool responses.



Determine whether the system can establish the final state safely.



### 6. Review result handling



Determine whether tool results are validated before downstream use.



Look for risks where a failed or malformed result could be treated as confirmed success.



## Business impact categories



Consider only evidence-supported impact such as:



- customer-visible incorrect state;

- unauthorized data access;

- cross-user or cross-tenant exposure;

- financial loss;

- duplicate business action;

- data corruption or loss;

- privacy impact;

- operational failure;

- inability to recover an uncertain operation.



Do not exaggerate impact.



## Required Skills



For every material risk, include a `Required Skills` field only when the required expertise can be grounded in the identified evidence.



Examples may include:



- Python;

- API authorization;

- Database transactions;

- Concurrency and idempotency;

- Agent tool integration;

- Input validation;

- Secure data handling.



Do not invent specialized expertise that is unsupported by the risk evidence.



## Risk output structure



For each supported material risk, provide:



### Risk



A concise description of the observed issue.



### Affected workflow



Identify the relevant workflow stage and code path.



### Evidence



Provide concrete file, symbol, configuration, test, or runtime evidence.



### Business impact



Explain the specific customer, revenue, privacy, security, or operational consequence.



### Required Skills



List only evidence-supported technical expertise needed to investigate or remediate the issue.



### Confidence



State whether the evidence is strong, supported, or insufficient.



### What to change



Suggest a remediation direction without claiming that a specific implementation is required unless the evidence supports it.



## Investigation gaps



If the evidence is incomplete, record the missing evidence instead of promoting the candidate to a confirmed risk.



Examples:



- execution outcome cannot be established;

- authorization logic is outside the reviewed path;

- downstream side effect is not represented;

- retry behaviour cannot be determined;

- runtime configuration is unavailable.



## Important reporting rule



Do not convert the absence of an observed risk into a claim that the repository is completely safe.



A statement such as "no evidence-supported business risk identified" means only that the available evidence did not meet the reporting threshold.



## Final review checklist



Before reporting a risk, verify:



- [ ] The workflow is within scope.

- [ ] The behaviour is supported by evidence.

- [ ] The affected code path is identified.

- [ ] The business consequence is concrete.

- [ ] The risk is not only a generic best-practice concern.

- [ ] Required Skills are evidence-supported.

- [ ] Uncertainty is explicitly stated.

- [ ] The proposed change addresses the observed failure.

