# UnvibeCode Engineering Guide Visual Standard

## Purpose

UnvibeCode engineering guides should read like **visual engineering handbooks**, not long-form documentation.

Target roughly:

- **40–50% visual structure overall**: diagrams, decision trees, comparison tables, failure flows, and checklists.
- **50–60% text**: explanation, implementation detail, caveats, examples, and references.

For a long guide, do **not** turn every subsection into a diagram. A practical ceiling is roughly **6–12 Mermaid diagrams**, depending on length. When several patterns are structurally similar, show 2–3 representative diagrams and compare the rest in a table.

Do not add visuals only to make a page look busy. Every visual must help a reader make a design decision, understand a runtime path, diagnose a failure, or ship safely.

---

## 1. The five recurring visual types

Use these across implementation guides so readers learn one visual language and can scan every guide quickly.

### 1.1 High-level architecture diagram

Place near the beginning.

It should answer:

- What are the major components?
- What talks to what?
- Where are the important boundaries?
- Where do state, tools, data, verification, and users sit?

Prefer Mermaid when the diagram can be expressed clearly. Use a PNG only when Mermaid becomes unreadable.

**Rule:** keep the first architecture diagram simple enough to understand in roughly 20 seconds.

### 1.2 Decision tree

Use whenever engineers must choose between approaches.

Examples:

- Workflow vs agent vs multi-agent.
- Vector retrieval vs SQL/API.
- Synchronous request vs durable job.
- Fail-open vs fail-closed.
- Small model vs strong model vs cascade.

A good decision tree ends in an implementation choice, not a vague recommendation.

### 1.3 Comparison table

Use for alternatives with meaningful trade-offs.

Good columns include:

- when to use,
- when not to use,
- complexity,
- reliability,
- latency,
- cost,
- state requirements,
- operational burden,
- and failure mode.

Avoid tables that repeat prose without helping a decision.

### 1.4 Sequence or failure diagram

Use sequence diagrams to show **what happens at runtime**.

Use failure diagrams to show **what goes wrong in production**.

A useful pattern is:

~~~text
Normal path
    ↓
Failure path
    ↓
Corrected design
~~~

Production failures are often more memorable than abstract principles.

Examples:

- action succeeds → response is lost → retry duplicates action,
- retrieval times out → agent treats empty result as “no evidence,”
- two workers write shared state → last writer wins,
- cancellation reaches UI but not the external tool,
- parser/index/model version changes silently.

### 1.5 Production checklist

End implementation guides with an actionable checklist.

Checklist items should be verifiable.

Good:

- [ ] Tool writes use stable operation IDs.
- [ ] Retrieval failure is distinguishable from zero results.
- [ ] Root-level budget includes descendants and retries.

Weak:

- [ ] System is reliable.
- [ ] Security is good.
- [ ] Agent is production ready.

---

## 2. Optional visual modules

Use these when they materially improve the topic.

### Progressive build diagram

Show how a production design evolves:

~~~text
Model call
   ↓
Agent + tools
   ↓
Agent + tools + state
   ↓
+ verification
   ↓
+ observability + recovery
~~~

The reader should understand where they can stop.

### “What goes for toss in production?” table

Use three columns:

| Looks fine in demo | Production failure | Control |
| --- | --- | --- |

This is especially useful for agents, RAG, routing, guardrails, observability, and operations.

### Metrics table

Connect a metric to the engineering question it answers.

| Metric | Why it matters |
| --- | --- |
| Task success | Does the system actually complete the job? |
| p95 latency | What does a slow user experience? |
| Tool failure rate | Are dependencies unstable? |
| Cost per success | Is the architecture economically useful? |

### Small real-world scenario

Use a short workflow rather than a long case study.

Example:

~~~text
Bug report
  ↓
Reproduce
  ↓
Inspect repository
  ↓
Patch
  ↓
Run tests
  ↓
Independent verification
  ↓
Patch / blocked result
~~~

Then identify:

- deterministic parts,
- agentic parts,
- human approval points.

### Decision card

After a complex section, add a short conclusion:

> **Engineering decision**
>
> Use a workflow when the steps are known.  
> Use an agent when observations determine the next action.  
> Use multiple agents only when decomposition creates real independence.

---

## 3. Recommended page rhythm

Avoid long runs of prose.

A strong section usually follows:

1. **2–4 short paragraphs**
2. **diagram / comparison / decision visual**
3. **implementation rules**
4. **production failure or caveat**
5. **what to measure / verify**

Then move to the next concept.

Do not use this rigidly when the content does not need all five.

---

## 4. Diagram rules

### Prefer Mermaid when

- architecture has clear boxes and arrows,
- runtime order matters,
- a decision tree is useful,
- source-controlled editability matters.

### Prefer an image when

- the visual is a compact infographic,
- layout is too dense for Mermaid,
- the visual is intentionally explanatory rather than executable,

### Keep diagrams readable

- One main idea per diagram.
- Do not diagram every member of a repetitive pattern family; use a comparison table for the rest.
- Prefer fewer than ~10–12 major nodes.
- Use short labels.
- Keep direction consistent.
- Avoid crossing arrows where possible.
- Do not encode important meaning only through color.
- Follow each diagram with the engineering conclusion it supports.

---

## 5. Table rules

- Prefer 3–6 meaningful columns.
- Use comparisons rather than paragraph-sized cells.
- Put the decision variable in the first column.
- Use symbols such as ✅ / ⚠️ sparingly and only when the meaning is obvious.
- Do not rank technologies without evidence; compare requirements and trade-offs instead.

---

## 6. Headings should help navigation

Prefer headings that answer an engineer’s question.

Examples:

- **Do you actually need an agent?**
- **Where should state live?**
- **What happens when the tool times out after committing?**
- **How should a fallback behave?**

Use noun headings where they are naturally clearer, such as **Production checklist** or **Further reading**.

---

## 7. Production failures should be first-class content

Do not hide failures in a final warning paragraph.

For important systems, explicitly cover:

- symptom,
- why the obvious response is unsafe,
- control,
- and regression/recovery test.

Where useful, visualize:

~~~text
DEMO ASSUMPTION
      ↓
PRODUCTION EVENT
      ↓
FAILURE
      ↓
CONTROL
~~~

The goal is to teach engineers how the system breaks, not only how the happy path works.

---

---

## 8. Standard guide structure

Use this as a starting template rather than a mandatory outline.

~~~text
Title
Scope

30-second mental model
High-level architecture

Decision tree
Comparison table

Core principles
Design process

Implementation architecture
Runtime sequence

Patterns / alternatives
Failure diagrams

Production failures
Metrics / evaluation

Production checklist
FAQ

Further reading
~~~

---

## 9. Review checklist for future UnvibeCode guides

Before publishing, check:

- [ ] A reader can understand the high-level architecture before deep prose.
- [ ] The guide has at least one clear decision aid where alternatives exist.
- [ ] Major alternatives are compared in a table.
- [ ] Runtime behavior is shown with a flow or sequence where useful.
- [ ] At least one important production failure is visualized.
- [ ] Failure sections include a control and a test, not only a warning.
- [ ] Production checklist items are verifiable.
- [ ] Diagrams remain readable on GitHub.
- [ ] Text does not merely repeat the diagram.
- [ ] Visuals are functional, not decorative.
- [ ] The guide links to deeper UnvibeCode guides rather than duplicating whole topics.
