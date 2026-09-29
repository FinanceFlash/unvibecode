# Context Assembly, Generation, and Citations

Retrieving the right evidence is not enough.

The model only sees the **final assembled context**, not the retriever's full candidate set.

## 1. Distinguish the stages

~~~text
source
  ↓
retrieval
  ↓
reranking
  ↓
compression / context assembly
  ↓
model
  ↓
answer
~~~

Evidence can be lost at every step.

A retrieval metric measured before reranking cannot prove that the model actually received the required fact.

## 2. Reserve context for required evidence first

Before filling the prompt with optional history or broad background, reserve space for:

- current task requirements,
- decisive evidence,
- source identity,
- critical exceptions,
- structured facts,
- pending workflow state where relevant.

Token budget is an architecture constraint.

## 3. Preserve qualifiers

Compression and summarization must not silently remove:

- “only if,”
- “except,”
- dates,
- units,
- approval requirements,
- thresholds,
- uncertainty,
- source conflicts.

A shorter context is not better if it changes meaning.

## 4. Separate evidence from instructions

Retrieved documents, web pages, emails, and user uploads are data.

Do not promote instructions found inside them into trusted application policy.

Keep system/application instructions structurally separate from retrieved content.

## 5. Citations need claim-level support

A citation can be valid and still fail to support the claim.

Check:

- source exists,
- cited region contains the evidence,
- evidence is applicable,
- claim preserves conditions/units/time,
- source is current enough for the task.

A source ID proves provenance, not truth.

## 6. Design for abstention

Abstention is not a model personality choice. It is a system outcome when evidence requirements are not met.

Possible outcomes:

- answer fully,
- answer supported parts and state gaps,
- perform another bounded retrieval step,
- ask for clarification,
- escalate,
- abstain.

Do not silently switch from “answer from supplied evidence” to “answer from model memory” during retrieval failure.

## 7. Conflicting evidence

When current sources conflict:

- apply an approved authority/precedence rule,
- surface the conflict,
- or escalate.

Do not use model confidence or vector similarity as the authority mechanism.

## 8. Verify before release

For high-value answers, verify:

- material claims,
- required facts,
- citations,
- exact protected values,
- completeness,
- unsupported additions.

The verification layer should inspect the **actual evidence the model received**, while source-level evaluation separately checks the answer against authoritative truth.

That distinction lets you tell whether the failure belongs to retrieval/context or generation.
