# UnvibeCode: RAG Review Checklist

Use with a design, repository, or failed answer. Record evidence beside every check. Status: verified / finding / unverified / not applicable. Unchecked does not mean broken. This is practical guidance, not certification.

## 1. Parsing and ingestion

- [ ] Use PyMuPDF for clean digital text, Docling for complex layouts/tables, and PyMuPDF rendering + DeepSeek OCR for scans.
- [ ] For mixed files, route individual pages/regions; normalize outputs, restore reading order, and avoid duplicate evidence from overlapping extraction.
- [ ] Treat DeepSeek OCR as a separate model integration, not a built-in PyMuPDF backend.
- [ ] Classify pages as digital text, scans, or mixed; retain originals for inspection.
- [ ] Compare reading order, headings, table cells/headers, merged cells, units, footnotes, signs, and decimals against original pages.
- [ ] Evaluate multilingual and poor scans separately; quarantine ambiguous extraction.
- [ ] Preserve document ID, page/location, content hash, extraction method/version, and failure status.
- [ ] Chunk after structural checks, retaining table and parent-heading context.

Test: detach headers from table values. Expected: ambiguous attribution is flagged before indexing; no confident year/segment attribution.

## 2. Deterministic facts and calculations

- [ ] Fetch known clauses, table cells, and source spans by stable ID; preserve original wording and qualifiers with minimal rewriting.
- [ ] Use parameterized, approved DB lookups for structured numbers and Python Decimal for decimal-sensitive arithmetic.
- [ ] Obtain current quantities from authoritative stores with snapshot times and units.
- [ ] Validate applicable rules, operands, schemas, units, and freshness before arithmetic.
- [ ] Use exact arithmetic where needed; distinguish percent from percentage points.
- [ ] Separate supported facts from model inference; verify quotation relevance and source version.
- [ ] Missing, stale, or conflicting inputs cause explicit failure, never guessed values or substituted zero.

Test: limit 1.50% minus exposure 1.37% equals 0.13 percentage points. Remove exposure: return missing-data result, not 1.50% headroom.

## 3. Retrieval and connected evidence

- [ ] Use knowledge graphs when answers require multiple linked facts or dependencies; corpus size alone is not the reason.
- [ ] Return the supporting source spans and versions for each graph edge, not just entity names or relationship assertions.
- [ ] Label representative questions by required evidence: exact lookup, semantic passage, aggregation, relationships, or code.
- [ ] Compare retrieval alternatives using evidence coverage and answer correctness.
- [ ] Preserve entity IDs, edge provenance, and necessary hops for linked questions; multiple documents do not automatically require a graph.
- [ ] Keep missing hops and conflicts explicit; bound traversal/retries.
- [ ] Enforce authorization before exposing text, metadata, graph edges, or caches.

Test: strategy -> eligibility rule -> exchange restriction. Remove the last edge: report incomplete evidence rather than inventing the reason.

## 4. Knowledge versioning

- [ ] Attach document/version/chunk IDs, source URI, content hash, section/page location, parser/version, and review status to extracted records.
- [ ] For large files, chunk by structure and retain parent section, table headers, units, language, and reliable entity tags.
- [ ] Apply access and effective-date filters before retrieval; use metadata afterward for parent context and precise citations. Ingestion date is not effective date.
- [ ] For large collections, keep a restartable batch manifest; deduplicate by hash, retry failures, and reindex changed documents and dependent graph links/caches.
- [ ] Define current/historical queries, effective intervals, supersession, tenant, and source authority.
- [ ] Resolve applicable versions; retrieval similarity is not authority.
- [ ] Detect overlapping applicable policies rather than silently selecting one.
- [ ] Bind chunks, citations, and cache to snapshots; propagate deletion and permission changes.
- [ ] Make mid-request updates and source conflicts visible.

Test: v3 expires when v4 starts. Select by query date; overlapping versions cause explicit conflict.

## 5. Code retrieval

- [ ] Preserve language-aware function/class boundaries and source revision/location.
- [ ] Inspect imports, callers, configuration, background jobs, and relevant tests.
- [ ] Mark dynamic dispatch, reflection, generated code, and unresolved imports as limitations.
- [ ] Separate syntax matches from proven execution and inferred intent.
- [ ] Detect stale indexes after committed and uncommitted edits.

Test: two modules contain the same function name. Preserve qualified identities rather than merging them.

## 6. Context, memory, and live data

- [ ] Map each requested fact to live DB, versioned documents, code, or conversation context.
- [ ] Validate bounded router outputs and arguments before executing operations.
- [ ] Prevent memory from overriding current authoritative data or permissions.
- [ ] Provide clarification, abstention, and error outcomes for ambiguity/unavailable tools.
- [ ] Track freshness; distinguish explaining a result from authorizing a business action.

Test: memory says exposure 0.80%, DB says 1.37%. Use DB for current exposure; memory explains only the prior discussion.

## Findings worksheet

| Module | Status | Evidence/location | Consequence | Smallest correction | Regression scenario |
|---|---|---|---|---|---|
| Versioning example | Confirmed | Trace uses expired v3 | Wrong rule | Effective-date filter | Current/historical query pair |

## Cross-cutting checks

- [ ] Use **RAGChecker only** as the retrieval/generation evaluation framework; retain question, reference answer, response, and actual retrieved context.
- [ ] Configure its checking models separately; compare its judgments with human-reviewed cases. Do not report scores without running the evaluator.
- [ ] Keep direct OCR/table comparisons and Python arithmetic checks alongside RAGChecker; these are component tests, not additional RAG evaluation frameworks.
- [ ] Include unauthorized sources, prompt injection, empty retrieval, timeout, revocation, and broken citations.
- [ ] Measure extraction fidelity, retrieval coverage, unsupported claims, completeness, abstention, latency, and cost separately.
- [ ] Maintain human-reviewed held-out cases. Generated questions are candidate tests, not automatic gold labels.
- [ ] Record parser, model, prompt, index, and configuration versions for regression checks.

Companion: RAG_PRACTICAL_GUIDE.md. Executable synthetic demonstration: rag_review_example.py.

## Implementation order and example

1. Inspect representative pages and choose the three parser routes above.
2. Validate extraction, attach metadata, preserve versions, and chunk by structure.
3. Implement exact source lookups wherever IDs/keys are known.
4. Add evidence-backed graph traversal for questions with multiple linkages.
5. Retrieve structured numbers from the DB and calculate in Python.
6. Assemble cited facts with inference clearly separated; keep memory separate from current authority.
7. Evaluate retrieval/generation with [RAGChecker](https://github.com/amazon-science/RAGChecker), alongside component regression checks.

Run `python rag_review_example.py` to see simulated hybrid parser routing, metadata filtering, exact retrieval, an in-memory SQLite lookup, linked evidence, arithmetic, and regression tests. No actual PDF extraction, OCR, or LLM evaluation runs. To export the demonstration's RAGChecker input, use `python rag_review_example.py --ragchecker-json > ragchecker_inputs.json`; configure and run RAGChecker separately following its official instructions. The synthetic export demonstrates the format, not a quality benchmark.
