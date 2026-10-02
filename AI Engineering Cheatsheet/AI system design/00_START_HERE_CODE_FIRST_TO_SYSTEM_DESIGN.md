# Start Here: First Principles for AI System Design

Most developers begin **code-first**:

> What should I build, and which framework should I use?

That is useful for learning implementation. It becomes limiting when the system grows, because code does not tell you **where a responsibility should live, what should be trusted, or what should happen when something fails**.

A better progression is:

```text
CODE-FIRST
How do I implement this?
        ↓
PATTERN-FIRST
What kind of system problem is this?
        ↓
RESPONSIBILITY-FIRST
Which component should own it?
        ↓
IMPLEMENTATION
Which technology best fits that responsibility?
```

This guide is organized around that progression.

The idea is influenced by Khalil Stemmler’s discussion of moving from Code-First toward Pattern-First and Responsibility-First engineering:

- [The Code-First Developer](https://khalilstemmler.com/articles/the-phases-of-craftship/code-first/)
- [The 5 Phases of Craftship](https://khalilstemmler.com/articles/the-phases-of-craftship/the-5-phases/)

---

## The first principles used throughout this guide

### 1. Responsibility before component

Do not start with:

> “Should I use LangGraph, a vector DB, Kafka, or another agent?”

Start with:

> **What responsibility exists, and who should own it?**

Examples:

| Responsibility | Better owner |
| --- | --- |
| Interpret intent | Model / classifier |
| Retrieve evidence | Retriever / DB / graph |
| Calculate a number | Deterministic code |
| Authorize an action | Application / authorization service |
| Track workflow progress | Explicit state |
| Confirm an external write | Tool receipt / reconciliation |
| Explain the result | Model |

Architecture becomes easier when each component has a clear job.

---

### 2. Pattern before framework

Many production failures repeat across domains.

| Situation | Pattern |
| --- | --- |
| Work outlives an HTTP request | Durable job / queue |
| Remote write may already have succeeded | Idempotency + reconciliation |
| Evidence may be incomplete | Evidence-sufficiency gate |
| Provider may fail | Circuit breaker + qualified fallback |
| State must survive restart | Durable checkpoint |
| Many tenants share infrastructure | Tenant isolation |
| Different tasks need different models | Model allocation / routing |

The framework comes **after** recognizing the problem shape.

---

### 3. Keep deterministic work deterministic

LLMs are useful for interpretation, synthesis, extraction, classification, and language.

They should not replace deterministic systems for:

- permissions,
- exact database facts,
- arithmetic,
- quotas,
- workflow invariants,
- destination restrictions,
- transaction identity,
- or confirmation of external side effects.

A useful rule is:

> **Use models for ambiguity. Use code for authority.**

---

### 4. Separate decision from execution

A model may propose:

> “Refund this order.”

The application must still validate:

**identity → tenant → resource → permission → operation → arguments → destination**

before anything happens.

This same principle appears repeatedly in RAG, agents, guardrails, memory, and operations.

---

### 5. Make evidence and state explicit

Conversation text is not workflow truth.

A model saying:

> “The deployment succeeded”

does not prove that the deployment system committed it.

Likewise, a retrieved document being similar to a question does not prove that it is current, authorized, or authoritative.

Store important truth explicitly:

- source/version/provenance,
- operation IDs,
- approvals,
- artifact versions,
- workflow state,
- external receipts.

---

### 6. Bound non-determinism

A probabilistic component should never have an unlimited path through production infrastructure.

Bound:

- model tokens,
- retries,
- tool calls,
- agent steps,
- recursion,
- execution time,
- cost.

This is why many “AI failures” are actually ordinary system-design failures.

---

### 7. Design the failure path with the happy path

For every component ask:

1. What can be missing?
2. What can be stale?
3. What can be unauthorized?
4. What can time out?
5. What can commit before the response is lost?
6. What should the system do next?

Recovery should be designed, not improvised after an incident.

---

### 8. Evaluate and observe responsibilities separately

Do not reduce the whole system to “the model was wrong.”

If an answer fails, determine whether the first failure was in:

**parsing → retrieval → context → model → tool → state**

Evaluation tells you whether the responsibility works.

Observability tells you what happened in production.

Operations closes the loop by fixing, releasing, recovering, and turning incidents into regression tests.

---

## How this guide applies those principles

The reading order follows the system responsibilities rather than a list of technologies.

| Step | Guide | Main responsibility |
| --- | --- | --- |
| 01 | [AI System Design Foundations](./01_AI_SYSTEM_DESIGN_FOUNDATIONS.md) | See the whole system and its boundaries |
| 02 | [RAG](./02_RAG/README.md) | Route evidence to the right source |
| 03 | [Context, Memory, and State](./03_CONTEXT_MEMORY_STATE_ENGINEERING.md) | Separate model context, reusable memory, and workflow truth |
| 04 | [Agent Engineering](./04_AGENT_ENGINEERING.md) | Add autonomy only where it creates value |
| 05 | [Guardrails](./05_GUARDRAILS/README.md) | Put controls at the boundary where risk occurs |
| 06 | [Evaluation Engineering](./06_EVALUATION_ENGINEERING.md) | Prove each responsibility works |
| 07 | [LLM Routing](./07_LLM_ROUTING_STRATEGY.md) | Allocate qualified models to tasks |
| 08 | [Production Serving and Cloud Architecture](./08_PRODUCTION_SERVING_AND_CLOUD_ARCHITECTURE.md) | Handle real traffic, queues, retries, scaling, and releases |
| 09 | [AI Observability](./09_AI_OBSERVABILITY_IMPLEMENTATION.md) | Reconstruct what happened |
| 10 | [AI Operations](./10_AI_OPERATIONS_IMPLEMENTATION.md) | Release, recover, migrate, and improve continuously |

---

## Use this question before adding anything

Before adding a model, agent, queue, cache, vector database, classifier, or framework, ask:

> **What responsibility does it own, what failure does it solve, and what happens when it is wrong?**

If those answers are unclear, more code will usually make the system harder to reason about.

The goal of this guide is not less code.

It is **code built on explicit responsibilities, proven patterns, and known failure boundaries**.
