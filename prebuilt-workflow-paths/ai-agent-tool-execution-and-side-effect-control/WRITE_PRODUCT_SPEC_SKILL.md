---

name: write_ai_agent_tool_execution_product_spec

description: Write or review a product specification for an AI agent tool-execution workflow, including tool selection, validation, authorization, side effects, outcomes, and recovery.

---



# Write AI Agent Tool Execution Product Specification



## Purpose



Write a product specification for a workflow where an AI agent requests an available tool and the application safely validates, authorizes, executes, and records the resulting operation.



## Required workflow boundary



Start with an agent-generated tool request.



End when:



- the operation has a confirmed successful outcome; or

- the request is rejected or fails without an unintended side effect; or

- the operation enters an explicitly unresolved state requiring recovery or reconciliation.



Do not expand the specification into a general LLM generation, RAG, human approval, scheduled job, or external-system synchronization workflow.



## Required specification sections



### People and systems



Identify:



- requesting user or application;

- AI agent;

- tool registry;

- authorization or policy layer;

- tool execution environment;

- target resource;

- observability or audit system.



### Things created or changed



Identify:



- tool request;

- validated arguments;

- authorization decision;

- execution record;

- tool result;

- affected resource;

- recovery or unresolved state where applicable.



### Stages



Describe:



1. tool selection;

2. request validation;

3. authorization and policy check;

4. execution preparation;

5. tool execution;

6. result validation;

7. outcome recording and recovery.



## Required product decisions



Ask the product owner to define:



- which tools are available;

- which tools are read-only;

- which tools can create side effects;

- who can invoke each operation;

- which resources may be affected;

- which actions are high impact;

- whether confirmation or additional policy checks are required;

- which operations must be idempotent;

- what happens after a timeout;

- what counts as success;

- what happens after partial completion;

- which execution evidence must be retained.



## Acceptance criteria



The specification must define acceptance criteria showing that:



1. only registered tools can execute;

2. arguments are validated before execution;

3. authorization occurs before protected side effects;

4. resource-level permissions are enforced;

5. duplicate side effects are controlled;

6. tool results are validated;

7. failures are distinguishable from successful execution;

8. uncertain execution can be safely reconciled;

9. sensitive information is not unnecessarily exposed;

10. important terminal outcomes are observable.



## Core scenarios



Use the workflow's `CORE_20_SCENARIOS.md` as the minimum scenario checklist.



Do not duplicate scenarios merely by changing wording.



## Business consequences



For each important failure path, describe:



- affected people or systems;

- affected records or resources;

- customer impact;

- operational impact;

- security or privacy impact where relevant;

- whether recovery is automatic or manual.



## Evidence rule



This skill writes product requirements. It must not claim that an existing application already implements a control unless supporting repository or runtime evidence is supplied.



Separate:



- required product behaviour;

- implementation evidence;

- unresolved product decisions.



## Output quality



Produce a self-contained specification using the exact headings:



- `People and systems`

- `Things created or changed`

- `Stages`



Every important scenario must state what **Must not happen**.



Keep the workflow boundary explicit and avoid overlapping the existing LLM, RAG, approval, scheduled-job, and external-system synchronization packs.

