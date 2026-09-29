# Agent Engineering
## Single agents, multi-agent systems, and production harnesses

Building an agent that completes a convincing demo is useful. Production begins when the system must survive incomplete information, slow tools, changing requirements, duplicate retries, cancellation, deployment changes, and a restart halfway through an external action.

Good agent engineering starts with the task, not the number of agents. Define the required outcome, what evidence proves success, what authority is allowed, and which decisions genuinely require exploration. Then choose the smallest architecture that can satisfy those constraints.

> **Core rule:** use the minimum autonomy required, and keep authority, state, limits, verification, and recovery in software around the model.

This guide covers architecture, design choices, coordination patterns, the production harness, failure recovery, evaluation, and release.

---

## 1. The 30-second mental model

A production agent is not just an LLM with tools. The **harness** controls the execution around it.

~~~mermaid
flowchart LR
    U["User / Task"] --> H["Agent Harness<br/>context · state · limits · retries"]
    H --> A["Agent / LLM<br/>plan · choose next action"]
    A --> T["Tool Gateway"]
    T --> D["Data / APIs / Code / External systems"]
    D --> T
    T --> H
    H --> V["Verification"]
    V -->|continue| A
    V -->|blocked / partial| O["Result / Action / Status"]
    H --> S["State + Checkpoints"]
    H --> M["Observability + Evaluation"]

    classDef user fill:#eef2ff,stroke:#6366f1,color:#111827;
    classDef core fill:#e0f2fe,stroke:#0284c7,color:#111827;
    classDef action fill:#ecfdf5,stroke:#059669,color:#111827;
    classDef control fill:#fff7ed,stroke:#ea580c,color:#111827;
    class U user;
    class H,A core;
    class T,D action;
    class V,O,S,M control;
~~~

The model can be probabilistic. The surrounding controls should be explicit.

| Component | Production responsibility |
| --- | --- |
| Agent | Chooses a next action from the goal, context, and tool feedback |
| Harness | Builds context, runs the loop, enforces limits, manages state and recovery |
| Tool gateway | Validates tool, arguments, identity, resource, destination, and operation |
| Workflow/orchestrator | Controls dependencies, delegation, gates, and terminal outcomes |
| State/checkpoint store | Persists progress needed to resume |
| Operation ledger | Records intended writes and uncertain external outcomes |
| Verifier | Checks acceptance criteria rather than trusting “done” |
| Observability | Makes decisions, failures, cost, and versions inspectable |

A model call is not automatically an agent. A fixed sequence of model calls can remain a conventional workflow.

---

## 2. Do you actually need an agent?

Use a decision tree before choosing a framework.

~~~mermaid
flowchart TD
    A["What must the system do?"] --> B{"Are the steps known<br/>in advance?"}
    B -->|Yes| C["Use a workflow / code"]
    B -->|No| D{"Does the next step depend<br/>on new observations?"}
    D -->|No| E["Use a bounded model call"]
    D -->|Yes| F{"Can meaningful work run<br/>independently?"}
    F -->|No| G["Single agent + tools"]
    F -->|Yes| H["Consider multiple workers"]
    H --> I{"Does decomposition improve<br/>quality/latency/isolation?"}
    I -->|No| G
    I -->|Yes| J["Multi-agent / orchestrated workers"]

    classDef question fill:#f8fafc,stroke:#64748b,color:#111827;
    classDef simple fill:#ecfdf5,stroke:#059669,color:#111827;
    classDef agent fill:#e0f2fe,stroke:#0284c7,color:#111827;
    classDef multi fill:#f5f3ff,stroke:#7c3aed,color:#111827;
    class A,B,D,F,H,I question;
    class C,E simple;
    class G agent;
    class J multi;
~~~

### Workflow vs single agent vs multi-agent

| Aspect | Workflow | Single agent | Multi-agent |
| --- | --- | --- | --- |
| Steps known in advance | Strong fit | Sometimes | Usually unnecessary |
| Next step depends on discoveries | Limited | Strong fit | Strong fit |
| Parallel independent work | Limited | Limited | Strong fit |
| State complexity | Low–medium | Medium | High |
| Coordination overhead | Low | Medium | High |
| Failure surface | Smaller | Larger | Largest |
| Good starting point | **Default** | When autonomy helps | When decomposition helps |
| Typical examples | Extraction, validation, approvals | Investigation, coding, research | Independent research, subsystem analysis |

**Engineering decision:** complexity alone does not justify multiple agents. Split only where context, permissions, specialization, or independent work creates measurable value.

---

## 3. Build autonomy progressively

Do not jump from one model call directly to a fleet of agents.

| Level | Add only when needed |
| --- | --- |
| 1. Model call | Input is sufficient and output is bounded |
| 2. Model + tools | External facts or deterministic computation are required |
| 3. Single agent loop | New observations determine the next step |
| 4. Persisted state | Work can pause, retry, or outlive one request |
| 5. Verification | “Done” must be checked independently |
| 6. Recovery + observability | Failures, retries, costs, and restarts matter |
| 7. Multi-agent | Independent work or isolation creates measurable value |

**Stop at the lowest level that meets the task contract.**

---

## 4. Eight design principles

### 4.1 Use the minimum autonomy required

Use code for known rules, model calls for bounded interpretation, and agent loops where observations determine the next step. Add agents only when there is a real decomposition boundary. smolagents recommends reducing unnecessary agency; Anthropic recommends simple, composable designs. [1,2]

**Design check:** which decision cannot reasonably be predetermined?

### 4.2 Define responsibilities through contracts

An agent title such as “senior researcher” is not a boundary. Define inputs, owned scope, excluded scope, allowed actions, expected artifacts, and completion conditions.

**Design check:** can the worker finish without guessing what another worker owns?

### 4.3 Treat tools as interfaces the model must learn

Document purpose, parameters and units, return values, side effects, error states, and recovery behavior. Give the agent only the tools it needs. smolagents emphasizes clear tool interfaces and useful tool descriptions. [1]

### 4.4 Give each decision the context it needs

Pass relevant evidence, current state, constraints, and unresolved questions. Preserve source identifiers and qualifiers when compressing. Store large artifacts separately and retrieve only what is needed. Google treats isolation, persistence, and compression as explicit context-design choices. [3]

### 4.5 Define completion through observable outcomes

Do not accept “done” as proof. Completion may require passing tests, required facts, generated artifacts, database state, external receipts, or verified coverage.

### 4.6 Bound the entire execution

Bound deadline, tokens, cost, tool calls, retries, delegation depth, concurrency, and revision loops. Apply limits across the whole task tree, not only per worker.

### 4.7 Enforce authority and recovery outside the prompt

Validate identity, ownership, resource, destination, and operation at execution time. Scope credentials and isolate code execution. Record external operation identity so uncertain writes can be reconciled.

### 4.8 Make decisions inspectable and improvements measurable

Record task ownership, versions, tool outcomes, state transitions, artifacts, cost, and termination reasons. Mask sensitive data. Compare architecture changes against a simpler baseline.

---

## 5. Design from the task

### Step 1 — Define the outcome

| Field | Define before implementation |
| --- | --- |
| Deliverable | Answer, report, patch, analysis, completed action |
| Acceptance | Required facts, tests, constraints, external state |
| Information | Documents, APIs, databases, repository, conversation |
| Authority | Read, propose, edit, execute, publish |
| Limits | Deadline, cost, calls, retries |
| Blocked behavior | Clarify, partial result, escalate, or stop |

For repository repair, “produce a patch” is weaker than:

> reproduce the defect → fix it → pass relevant regression tests → preserve the required interface.

The stronger definition determines what the harness must verify.

### Step 2 — Classify each operation

| Operation | Starting implementation |
| --- | --- |
| Known validation, calculation, transition | Code |
| Bounded classification/extraction/drafting | One model call |
| Investigation with unpredictable next steps | Agent with tools |
| Independent investigation | Parallel workers |
| External mutation | Authorized tool execution + recovery controls |

Do not turn every step into a job title.

### Step 3 — Draw dependencies

Ask:

1. Can these parts run independently?
2. Do they require different context, tools, or permissions?
3. Can a stable artifact preserve what the next stage needs?
4. Can that artifact be verified?

Separate work at stable evidence boundaries: verified requirements, research dossier, patch, calculation result.

### Step 4 — Choose a starting architecture

| Task | Starting architecture | Keep deterministic | Add agents when… |
| --- | --- | --- | --- |
| Classification/extraction | Fixed pipeline | schema, normalization, persistence | hard inputs need adaptive inspection |
| Support | Router + bounded specialist loop | identity, authorization, transaction checks | domains need different context/tools |
| Code repair | Coding agent + verification | tests, workspace isolation, change recording | investigations/edits can run independently |
| Research | Parallel research + synthesis | storage, deduplication, deadline handling | branches emerge dynamically |
| Long-form writing | Requirements → draft → verify | section checks, export, references | sections have separable contracts |
| Data analysis | Analyst + computation tools | queries, calculations, invariants | hypotheses can be investigated separately |
| Incident analysis | Lead + read-only workers | access, change approval, execution limits | subsystems can be inspected independently |

### Step 5 — Define the agent contract

~~~yaml
agent: patch_reviewer
goal: Find verified defects introduced by the patch

inputs:
  - patch
  - relevant_files
  - acceptance_criteria
  - test_results

allowed_actions:
  - read_files
  - run_isolated_tests

prohibited_actions:
  - modify_production
  - merge_changes

output:
  - finding
  - file_location
  - supporting_evidence
  - severity
  - unresolved_questions

stop_when:
  - required_checks_complete
  - budget_exhausted
  - essential_information_unavailable
~~~

Worker outputs should carry task ID, input versions, artifact version, evidence references, unresolved issues, and terminal status.

Prefer terminal states such as:

**COMPLETE · PARTIAL · BLOCKED · FAILED**

instead of a generic “done.”

### Step 6 — Compare with a simpler baseline

Compare the proposed architecture against a fixed workflow or one agent using the same cases and declared total budget.

Measure task success, critical failures, cost per success, end-to-end latency, information lost at handoff, and recovery behavior.

---

# 6. Coordination patterns

These are architectural choices, not universal rankings. Google evaluated many agent configurations and found that task properties strongly influenced whether coordination helped. [4]

## 6.1 Router → specialist

Use when requests fall into distinguishable categories with different tools or context.

~~~mermaid
flowchart LR
    R["Request"] --> D{"Router"}
    D --> A["Specialist A"]
    D --> B["Specialist B"]
    D --> C["Clarify / fallback"]
    A --> V["Validate"]
    B --> V

    classDef input fill:#eef2ff,stroke:#6366f1,color:#111827;
    classDef route fill:#fff7ed,stroke:#ea580c,color:#111827;
    classDef worker fill:#e0f2fe,stroke:#0284c7,color:#111827;
    classDef verify fill:#ecfdf5,stroke:#059669,color:#111827;
    class R input;
    class D,C route;
    class A,B worker;
    class V verify;
~~~

| Use when | Watch | Measure |
| --- | --- | --- |
| categories are separable | misrouting, missing capability | confusion matrix + downstream success |

Routing is an established pattern in Anthropic's agent guidance. [2]

## 6.2 Sequential pipeline

Use when stages are known and each stage can produce a sufficient, checkable artifact.

| Build | Watch | Measure |
| --- | --- | --- |
| typed artifacts, versions, evidence references | assumptions lost in handoff | handoff fidelity + end-to-end success |

Google documents sequential orchestration. Its separate scaling study found deterioration on some tested sequential planning tasks; do not fragment tightly connected reasoning only to create specialists. [3,4]

## 6.3 Parallel workers → merger

Use when subtasks can proceed independently.

~~~mermaid
flowchart TD
    D["Defined subtasks"] --> A["Worker A"]
    D --> B["Worker B"]
    D --> C["Worker C"]
    A --> M["Merge + coverage check"]
    B --> M
    C --> M
    M --> O["Combined result"]

    classDef task fill:#fff7ed,stroke:#ea580c,color:#111827;
    classDef worker fill:#e0f2fe,stroke:#0284c7,color:#111827;
    classDef merge fill:#ecfdf5,stroke:#059669,color:#111827;
    class D task;
    class A,B,C worker;
    class M,O merge;
~~~

| Build | Watch | Measure |
| --- | --- | --- |
| output namespaces, coverage map, conflict policy | duplicate work, races, stragglers | coverage + total cost + p95 latency |

Google's scaling research supports parallelization when work is decomposable, with meaningful variation across tasks. [4]

## 6.4 Dynamic orchestrator → workers

Use when required subtasks emerge during investigation.

| Build | Watch | Measure |
| --- | --- | --- |
| task ledger, root budget, bounded delegation | overdelegation, unsupported synthesis | useful completed work vs coordination overhead |

Anthropic describes this pattern in its production research system. [5]

## 6.5 Generator → verifier → revision

Use when explicit feedback can improve an artifact.

~~~mermaid
flowchart LR
    G["Generator"] --> V["Verifier"]
    V --> D{"Requirements met?"}
    D -->|Yes| O["Accept"]
    D -->|No + budget| G
    D -->|Blocked / exhausted| H["Hold / escalate"]

    classDef gen fill:#e0f2fe,stroke:#0284c7,color:#111827;
    classDef verify fill:#fff7ed,stroke:#ea580c,color:#111827;
    classDef good fill:#ecfdf5,stroke:#059669,color:#111827;
    classDef stop fill:#fef2f2,stroke:#dc2626,color:#111827;
    class G gen;
    class V,D verify;
    class O good;
    class H stop;
~~~

| Build | Watch | Measure |
| --- | --- | --- |
| independent criteria, specific defects, revision cap | endless polishing, shared assumptions | errors corrected vs errors introduced |

Anthropic's evaluator–optimizer guidance emphasizes clear criteria and actionable feedback. [2]

## 6.6 Independent candidates → adjudication

Use when alternate attempts justify extra cost.

| Build | Watch | Measure |
| --- | --- | --- |
| independent attempts + external criteria | correlated errors mistaken for consensus | improvement over one attempt at equal total budget |

Parallel voting is documented by Anthropic. [2]

## 6.7 Bounded peer debate

Use when explicit disagreement can reveal errors that independent attempts miss.

| Build | Watch | Measure |
| --- | --- | --- |
| evidence-linked objections + limited rounds | persuasion replacing evidence | net error correction vs cost |

Multi-agent debate research reports benchmark improvements, not a guarantee that consensus establishes truth. [6]

---

## 7. The production harness

The harness is where a demo becomes a system.

~~~mermaid
flowchart TD
    U["Task"] --> C["Context Builder"]
    C --> A["Agent Loop"]
    A --> G["Tool Gateway"]
    G --> X["Tools / APIs / DB / Code"]
    X --> G
    G --> A
    A --> V["Verifier"]
    V -->|continue| A
    V -->|terminal| O["Result"]
    A <--> S["State / Checkpoints"]
    G <--> L["Operation Ledger"]
    A --> B["Budget Manager"]
    A --> T["Trace / Metrics"]
    A --> R["Artifact Store"]

    classDef core fill:#e0f2fe,stroke:#0284c7,color:#111827;
    classDef boundary fill:#fff7ed,stroke:#ea580c,color:#111827;
    classDef state fill:#f5f3ff,stroke:#7c3aed,color:#111827;
    classDef verify fill:#ecfdf5,stroke:#059669,color:#111827;
    class A,C core;
    class G,X boundary;
    class S,L,B,T,R state;
    class V,O verify;
~~~

### Harness responsibilities

| Component | Application responsibility |
| --- | --- |
| Context builder | Select authorized evidence, constraints, and current artifacts |
| Tool gateway | Validate schema, identity, ownership, destination, operation |
| Scheduler/orchestrator | Dependencies, concurrency, deadlines, task ownership |
| Budget manager | Reserve/reconcile cost across descendants |
| State store | Persist resumable progress |
| Operation ledger | Record writes and uncertain external effects |
| Artifact store | Preserve evidence and outputs with versions |
| Verifier | Apply acceptance criteria and request specific rework |
| Trace layer | Record diagnostic evidence with privacy controls |

A framework may implement several boxes. Confirm its guarantees; application authorization, semantic acceptance, and downstream idempotency still belong to your system.

---

## 8. Agent execution sequence

~~~mermaid
sequenceDiagram
    participant U as User
    participant H as Harness
    participant A as Agent
    participant G as Tool Gateway
    participant X as External System
    participant V as Verifier

    U->>H: Task
    H->>H: Authenticate + construct context + budgets
    H->>A: Goal + context + limits
    A->>G: Proposed tool(args)
    G->>G: Validate identity + permission + args
    G->>X: Execute
    X-->>G: Result / receipt / error
    G-->>H: Normalized result + operation metadata
    H->>A: Updated state
    A-->>H: Candidate completion
    H->>V: Result + independent requirements
    V-->>H: Accept / revise / blocked
    H-->>U: Result / partial / blocked / failed
~~~

The model proposes. The gateway authorizes. The harness remembers. The verifier decides whether completion evidence is sufficient.

---

## 9. Keep context, state, memory, and external truth separate

| Information | Best placement |
| --- | --- |
| Immediate instructions/evidence | Model context |
| Large reports, patches, documents | Versioned artifact store |
| Ownership, deadlines, retries, status | Application state |
| External writes and uncertain outcomes | Operation ledger |
| Reusable verified facts/preferences | Governed memory with provenance |

LangGraph distinguishes thread-scoped checkpoints from cross-thread stores. Neither automatically proves an external side effect happened exactly once. [8]

### Explicit runtime states

Use explicit terminal/runtime states such as:

`RUNNING · WAITING · CANCEL_REQUESTED · COMPLETE · PARTIAL · BLOCKED · FAILED · CANCELLED`

Define transitions in application code. A completed worker is not proof that the overall task met its acceptance criteria.

---

# 10. Production failures: what actually goes for toss

## 10.1 The tool succeeded, but the response disappeared

This is one of the most important agent failure modes.

~~~mermaid
sequenceDiagram
    participant A as Agent
    participant G as Tool Gateway
    participant P as Payment API

    A->>G: refund(order_123)
    G->>P: refund(order_123)
    P->>P: Refund commits
    P--xG: Response lost / timeout
    G-->>A: Timeout
    A->>G: Retry refund(order_123)
    G->>P: Refund again
    Note over P: DOUBLE REFUND
~~~

### Correct design

~~~mermaid
flowchart TD
    A["Agent requests refund"] --> O["Assign stable operation_id"]
    O --> L{"Operation ledger"}
    L -->|already completed| R["Return existing receipt"]
    L -->|unknown| C["Reconcile external state"]
    L -->|new| G["Tool gateway executes"]
    G --> E["Persist receipt / outcome"]
    C --> E

    classDef request fill:#eef2ff,stroke:#6366f1,color:#111827;
    classDef control fill:#fff7ed,stroke:#ea580c,color:#111827;
    classDef action fill:#e0f2fe,stroke:#0284c7,color:#111827;
    classDef safe fill:#ecfdf5,stroke:#059669,color:#111827;
    class A request;
    class O,L,C control;
    class G action;
    class R,E safe;
~~~

**Rule:** a timed-out write may have succeeded. Reconcile before repeating it.

## 10.2 Parallel workers overwrite each other

~~~mermaid
flowchart TD
    A["Worker A"] --> S["shared_result"]
    B["Worker B"] --> S
    C["Worker C"] --> S
    S --> X["Last writer wins<br/>other findings disappear"]

    A2["Worker A"] --> SA["result/A"]
    B2["Worker B"] --> SB["result/B"]
    C2["Worker C"] --> SC["result/C"]
    SA --> M["Explicit merge + coverage check"]
    SB --> M
    SC --> M

    classDef worker fill:#e0f2fe,stroke:#0284c7,color:#111827;
    classDef bad fill:#fef2f2,stroke:#dc2626,color:#111827;
    classDef isolated fill:#f5f3ff,stroke:#7c3aed,color:#111827;
    classDef good fill:#ecfdf5,stroke:#059669,color:#111827;
    class A,B,C,A2,B2,C2 worker;
    class S,X bad;
    class SA,SB,SC isolated;
    class M good;
~~~

Use per-worker namespaces and explicit merge logic. Locks stop simultaneous writes; they do not decide which conflicting conclusion is correct. Google ADK documentation warns about shared-state concurrency. [9]

## 10.3 Cancellation is not rollback

~~~mermaid
sequenceDiagram
    participant U as User
    participant H as Harness
    participant T as Tool

    U->>H: Cancel task
    H->>H: CANCEL_REQUESTED
    Note over H,T: Stop new dispatch
    H-->>T: Cancel if supported
    T-->>H: In-flight action may still complete
    H->>H: Reconcile actual outcome
    H-->>U: CANCELLED + committed effects, if any
~~~

Google's runtime documentation describes asynchronous cancellation and continuing in-flight work. [10]

## 10.4 Tool failure looks like “no data”

A tool response must distinguish:

~~~json
{
  "status": "error",
  "error_code": "UPSTREAM_TIMEOUT",
  "retryable": true,
  "results": null
}
~~~

from:

~~~json
{
  "status": "ok",
  "results": []
}
~~~

Otherwise the agent may convert an infrastructure failure into a confident “nothing found.”

## 10.5 Failure matrix

| Demo assumption | Production failure | Control | Regression test |
| --- | --- | --- | --- |
| “Each worker has a budget” | descendants overspend root request | root-owned atomic budget | concurrent nested delegation |
| “Done means complete” | required section is missing | independent acceptance criteria | delete one required item |
| “Checkpoint means safe retry” | write duplicates after timeout | operation ID + reconciliation | crash after external commit |
| “Cancel stops everything” | in-flight write completes | cancellation state + reconciliation | cancel before/during/after commit |
| “Workers can share state” | results overwrite | per-worker namespace + merge | randomize completion order |
| “Agreement means truth” | repeated unsupported claim | preserve source/evidence origin | inject one plausible unsupported claim |
| “Empty means no result” | backend timed out | typed tool outcomes | timeout vs successful-empty |
| “Latest deploy can resume old run” | tool/state schema incompatible | versioned checkpoints + migration | pause → deploy → resume |
| “Wait for every worker” | one optional straggler blocks result | required/optional dependency semantics | delay required vs optional worker |
| “Coordinator can delegate authority” | privilege expands through handoff | bind original identity/scope | unauthorized resource request |
| “Summary is enough for handoff” | evidence disappears | artifact + evidence references | resume from persisted records only |
| “More agents means better” | cost/latency rises without quality gain | paired baseline comparison | equal-budget architecture test |

Anthropic reports overlapping work, excessive spawning, long-running handoff issues, and version-management concerns in its production agent engineering write-ups. [5,7]

---

## 11. Evaluation and release

MAST groups observed multi-agent failures into specification/system design, inter-agent misalignment, and verification/termination. Use these as coverage categories rather than a replacement for application-specific evaluation. [11]

### What to measure

| Dimension | Production measure |
| --- | --- |
| Outcome | tasks satisfying all mandatory requirements |
| Critical errors | attempts containing predefined serious failures |
| Efficiency | total cost / successful tasks |
| Latency | end-to-end distribution including timeouts |
| Tool reliability | tool failures, retries, uncertain writes |
| Coordination | duplicate work, missing coverage, invalid handoffs, unresolved conflicts |
| Recovery | injected failures recovered without duplicate/prohibited effects |
| Human intervention | cases needing escalation/approval |
| Evaluation health | missing grades, flaky fixtures, stale labels |

### Release sequence

~~~mermaid
flowchart LR
    D["Design"] --> B["Simple baseline"]
    B --> E["Offline evaluation"]
    E --> F["Failure injection"]
    F --> S["Shadow / sandbox"]
    S --> C["Limited canary"]
    C --> P["Production"]
    C -->|critical failure| R["Rollback / restrict"]

    classDef prep fill:#e0f2fe,stroke:#0284c7,color:#111827;
    classDef test fill:#fff7ed,stroke:#ea580c,color:#111827;
    classDef live fill:#ecfdf5,stroke:#059669,color:#111827;
    classDef rollback fill:#fef2f2,stroke:#dc2626,color:#111827;
    class D,B prep;
    class E,F,S,C test;
    class P live;
    class R rollback;
~~~

Before release, demonstrate a successful path, a blocked path, a budget-exhausted path, cancellation, tool failure, and restart around an external action.

Check final outcomes **and prohibited intermediate effects**.

---

# 12. Production checklist

## Architecture

- [ ] A fixed workflow was considered before adding an agent.
- [ ] Multi-agent decomposition has a concrete reason: independence, context, permission, or parallelism.
- [ ] Each agent has an explicit contract and terminal conditions.
- [ ] Required vs optional dependencies are defined.

## Tools and authority

- [ ] Tool schemas describe purpose, arguments, units, effects, and errors.
- [ ] Identity/resource authorization happens outside the prompt.
- [ ] Read and write permissions are separated where appropriate.
- [ ] External writes use stable operation identity.
- [ ] Timed-out writes are reconciled before retry.

## State and recovery

- [ ] Context, application state, long-term memory, and external operation truth are distinct.
- [ ] Long-running tasks persist enough state to resume safely.
- [ ] Checkpoints include compatible workflow/tool/state versions.
- [ ] Cancellation stops new dispatch and reports in-flight effects.
- [ ] Partial, blocked, failed, and cancelled are separate outcomes.

## Limits

- [ ] Root request has a deadline and cost budget.
- [ ] Descendants reserve from the root budget.
- [ ] Tool calls, retries, concurrency, delegation depth, and revision loops are bounded.
- [ ] Budget remains for final synthesis/reporting.

## Multi-agent coordination

- [ ] Worker scope and exclusions are explicit.
- [ ] Parallel outputs use separate namespaces.
- [ ] Merge step checks coverage and conflicts.
- [ ] Claims retain original evidence/source identity.
- [ ] Agent agreement is not treated as independent proof.

## Observability and evaluation

- [ ] Task/parent IDs and versions are traceable.
- [ ] Tool outcomes distinguish error, empty, partial, denied, and stale states.
- [ ] Cost, latency, retry, and termination reason are recorded.
- [ ] Sensitive trace data has masking and retention controls.
- [ ] Architecture is compared against a simpler baseline.
- [ ] Important production failures have regression tests.

## Release

- [ ] Happy path passes.
- [ ] Blocked path passes.
- [ ] Budget exhaustion is tested.
- [ ] Cancellation is tested.
- [ ] Crash-after-external-write recovery is tested.
- [ ] Pause/deploy/resume compatibility is tested.
- [ ] Rollback or route restriction is possible.

---

# 13. Frequently asked questions

### Where should I start when an agent works in a demo but fails in production?

Find the first boundary where reality diverged: context, tool arguments, tool execution, state persistence, handoff, or verification. Repair that boundary before rewriting the entire prompt or adding agents.

### Does a complex task need multiple agents?

No. Complex work can still require one coherent reasoning loop. Split only when work is independently useful or needs separate context, tools, permissions, or concurrency.

### Are sequential agents a bad design?

No. Sequential stages work when each produces a sufficient, checkable artifact. Avoid splitting a continuous investigation into summaries that discard the basis for the next decision.

### Should the orchestrator always be an LLM?

No. Use code when dependencies and transitions are known. Use an LLM when discovering or revising the decomposition is itself part of the task.

### Does each agent need a different model?

No. Different contexts or roles can use the same model. Measure the system rather than assuming model diversity improves reliability.

### Should every agent see the full conversation?

Usually not. Give each worker only the evidence, requirements, and artifacts needed for its task, with enough provenance to verify conclusions.

### Is agreement between agents proof?

No. Agents may share model biases, sources, and assumptions. Verify against evidence, executable behavior, or authoritative records.

### Can a critic make the generator reliable?

Only when the critic's criteria are valid and sufficiently independent. Measure false acceptance and false rejection, and cap revision loops.

### Do checkpoints prevent duplicate actions?

No. Checkpoints preserve execution state. External effects require stable operation identity, downstream deduplication when available, and reconciliation of uncertain outcomes.

### Can the system return before every worker finishes?

Yes, when unfinished branches are optional and the result identifies missing coverage. Required branches must complete or produce a partial/blocked terminal result.

### Why do agents repeat the same search/tool call?

The prior result may be absent from context, the error may be ambiguous, or the loop may lack a progress condition. Track normalized calls plus relevant state versions and stop repetition that produces no new evidence.

### How should two agents update the same file or record?

Prefer separate outputs and one integration owner. If shared writes are unavoidable, use version checks/transactions and an explicit conflict policy.

### What must a handoff contain?

Task ID, input versions, output artifact, evidence references, constraints, unresolved questions, and terminal status. Do not pass only a persuasive summary.

### Should a timeout automatically trigger retry?

For a bounded read, sometimes. For a write, first determine whether the operation already succeeded.

### How do I control the cost of nested agents?

Give the root request one budget, reserve portions atomically for descendants and retries, cap depth/concurrency, and reserve enough for final synthesis.

### How do I know whether more agents helped?

Compare paired cases against a simpler architecture at comparable total budgets. Measure success, serious errors, cost per success, latency, and handoff failures.

### Does structured output make an agent reliable?

It improves validation and integration. Valid JSON can still contain incorrect facts, missing requirements, or unauthorized actions.

---

# 14. Further reading

1. [smolagents: Building good agents](https://github.com/huggingface/smolagents/blob/main/docs/source/en/tutorials/building_good_agents.md) and [Introduction to agents](https://github.com/huggingface/smolagents/blob/main/docs/source/en/conceptual_guides/intro_agents.md).
2. [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents).
3. [Google Cloud: Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system).
4. [Google Research: Towards a science of scaling agent systems](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/) — January 2026; [research paper](https://arxiv.org/abs/2512.08296).
5. [Anthropic: How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — June 2025.
6. [Multi-agent debate research and implementation](https://github.com/composable-models/llm_multiagent_debate) — ICML 2024.
7. [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — November 2025.
8. [LangGraph: Persistence](https://docs.langchain.com/oss/python/langgraph/persistence).
9. [Google ADK: Parallel agents](https://github.com/google/adk-docs/blob/main/docs/agents/workflow-agents/parallel-agents.md).
10. [Google Cloud: Use an ADK agent, including cancellation behavior](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/use-an-adk-agent).
11. [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) — MAST, 2025.
