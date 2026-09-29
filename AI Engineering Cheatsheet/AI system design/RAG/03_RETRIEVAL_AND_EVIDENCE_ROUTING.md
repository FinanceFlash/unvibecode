# Retrieval and Evidence Routing

Retrieval should follow the structure of the evidence.

The question is not:

> “Which vector database should we use?”

It is:

> **“Which retrieval mechanism can produce the evidence this question requires?”**

## 1. Match retrieval to evidence

| Evidence need | Mechanism |
| --- | --- |
| Semantically related passage | Vector retrieval |
| Exact term / identifier | Keyword or exact lookup |
| Both meaning and identifiers | Hybrid retrieval |
| Current structured fact | SQL/API |
| Multi-hop relationship | Knowledge graph |
| Code symbol / dependency | AST/symbol-aware retrieval |
| Current external information | Search/external extraction |

A mature system may use several paths and combine their results.

## 2. Vector retrieval

Use vector retrieval when wording varies but semantic similarity is meaningful.

Do not confuse similarity with:

- truth,
- authorization,
- freshness,
- completeness,
- authority.

Apply deterministic filters first when metadata encodes hard constraints.

## 3. Hybrid retrieval

Hybrid retrieval is useful when questions mix semantic language with exact identifiers.

Examples:

- error code + explanation,
- product ID + policy language,
- function name + conceptual description.

Compare it against vector-only and lexical-only baselines on representative queries rather than assuming hybrid is automatically better.

## 4. Reranking

Reranking answers:

> Which of these eligible candidates should reach the final context first?

It should not decide:

- whether the user may access the source,
- whether the source is current,
- whether a source is authoritative.

Those controls belong earlier.

## 5. Knowledge graphs

Use a graph when the answer genuinely depends on relationships that are awkward to reconstruct from independent chunks.

Examples:

- service → API → database → downstream dependency,
- company → subsidiary → contract → obligation,
- policy → exception → product → geography.

Graph edges need provenance and versioning. An inferred relationship should not be treated like an authoritative source fact.

Avoid adding a knowledge graph merely because the corpus is large.

## 6. Structured lookup belongs outside document retrieval

If the system already has an exact database value, retrieve it directly.

Do not embed a customer-balance table into a vector index and ask the LLM to infer the latest row.

Use:

- parameterized SQL,
- approved API calls,
- semantic views,
- deterministic filters.

## 7. Code retrieval is its own problem

Code requires structure beyond text similarity.

Useful signals include:

- AST nodes,
- symbols,
- imports,
- call relationships,
- file/package boundaries,
- static dependencies.

AST analysis still cannot prove all runtime relationships, especially with reflection, dynamic dispatch, generated code, or external systems.

Preserve the distinction between:

- syntax,
- statically resolved connection,
- inferred business relationship,
- runtime behavior.

## 8. Test retrieval with controlled changes

Good retrieval tests include:

- source value A → value B,
- relevant document removed,
- conflicting source introduced,
- access revoked,
- alias/paraphrase introduced,
- exact identifier added,
- required evidence split across two sources.

A retriever should change its evidence set when the underlying evidence changes.

The goal is not high similarity. The goal is **reliable delivery of the evidence required for the task**.
