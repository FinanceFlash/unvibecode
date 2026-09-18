# UnvibeCode: Practical RAG Implementation Guide

This guide develops the six lessons from the [RAG forum discussion](https://www.reddit.com/r/Rag/comments/1wivnlx/15_years_of_rag_in_fintech_what_actually_worked/): parse correctly, retrieve facts with minimal rewriting, follow connected evidence, track source versions, preserve code structure, and separate documents, memory, live data, and calculations. The implementation details below turn those lessons into a practical starting plan.

## Which PDF parser should I use?

| PDF type | Parser approach | What to inspect |
|---|---|---|
| Digital PDF with usable text | **PyMuPDF** | Reading order, missing text, headings, page references |
| Layout-heavy PDF with tables or multiple columns | **Docling** | Rows, column headers, merged cells, units, footnotes |
| Scanned PDF or image-based content | **PyMuPDF + DeepSeek OCR** | Render pages or image regions with PyMuPDF, then send those images to DeepSeek OCR; verify the extracted text and numbers |

In the third approach, PyMuPDF opens/renders the PDF and DeepSeek OCR reads the resulting images. This is an integration you assemble; DeepSeek OCR is not PyMuPDF's built-in OCR backend. Use DeepSeek's documented model setup and image inference path. A PyMuPDF installation alone does not install or run the model. Sources: [PyMuPDF page rendering](https://pymupdf.readthedocs.io/en/latest/recipes-images.html), [Docling](https://docling-project.github.io/docling/), [DeepSeek OCR](https://github.com/deepseek-ai/DeepSeek-OCR).

## How do I use a hybrid parser?

Use different extraction paths within the same document, depending on the page or region. This is different from hybrid retrieval, which combines search methods.

1. Open the PDF with PyMuPDF and inspect each page's text layer and visual content. Selectable text is a starting signal, not proof of correct extraction.
2. Keep PyMuPDF output for clean digital text when reading order and content checks pass.
3. Route layout-heavy pages or tables to Docling when simple extraction loses structure.
4. Render scanned pages or image-only regions with PyMuPDF and pass those images to DeepSeek OCR. For mixed pages, process only the regions that need OCR where practical.
5. Normalize accepted output into common records: document ID, version, page, section, content type, text/table content, extraction method, and quality-review status.
6. Merge by original page and reading order. If two parsers covered the same region, choose the validated result rather than indexing both as independent evidence. Preserve the original page/crop for disputed results.
7. Check numeric values, minus signs, decimals, units, table headers, and footnotes before indexing. Flag uncertain pages for review or reprocessing.

For example, a report may use PyMuPDF for narrative pages, Docling for a multi-column table, and PyMuPDF + DeepSeek OCR for a scanned appendix. Keep table rows associated with their headers and units when creating chunks.

ML-based OCR helps recover text from page images. It does not guarantee correct table relationships or recover information that is unreadable in the source. For poor scans, check rotation and resolution and compare output against the original. For multilingual documents, validate the actual languages and mixed-script pages in your corpus; do not assume uniform accuracy. Keep transcription and translation separate.

## When should I use knowledge graphs?

Use them when answering requires following **multiple connected facts** across documents or code, as described in the forum. For example, explaining why a strategy was disabled may require connecting the strategy, eligibility rule, liquidity threshold, exchange restriction, and current instrument state. Retrieving a few similar passages may miss a necessary relationship.

They are also useful for questions such as: which strategies are affected if this risk rule changes? Represent the dependencies explicitly and follow the relevant links. For business logic spread across several code files, preserve connections between the relevant functions, rules, and workflows.

If the answer comes from a directly relevant passage and does not require following relationships, ordinary retrieval may be enough. The reason to use a graph is the connected evidence requirement, not simply the size of the corpus or the number of documents.

Implementation: assign stable entity IDs; store typed relationships such as `depends_on`, `restricted_by`, and `implemented_in`; attach the supporting document span or code location to each relationship. Keep source version and access scope with the evidence. Retrieve a relevant starting entity, follow a bounded set of links, and return the connected evidence. If a necessary link is missing, make that gap explicit instead of inventing it.

## How do I retrieve facts deterministically wherever possible?

When the record, clause, table cell, or source span is known, retrieve it through its stable identifier and return the relevant original content with minimal rephrasing. Use an LLM to locate candidate evidence or explain it where useful; let application code fetch the exact stored content.

For example, after identifying a policy clause, retrieve it by document version and clause ID. If it states that positions must be reduced above 80% margin utilisation, preserve the threshold, condition, and action. Do not let stylistic rewriting change them.

The forum also describes separating source-backed statements from model inference, retrieving the original statements with Python, and keeping inference distinct. To implement this reliably, retain source offsets or span IDs and validate the model's proposed references. Copying text exactly prevents rewriting errors but does not fix selection of an irrelevant or obsolete source.

## How do DB retrieval and Python calculations fit in?

Use the DB for current structured numbers and Python for arithmetic. Document retrieval supplies explanatory or policy evidence; conversation memory supplies earlier discussion context.

Example question: what is Strategy X's current exposure and how much headroom remains before a 2% limit?

| Needed item | Source/operation |
|---|---|
| Current exposure: 1.37% | Authorized DB lookup with snapshot time |
| Applicable limit: 2% | Versioned rules DB or validated policy record |
| Remaining headroom: 0.63 percentage points | Python subtraction after validating units and applicable date |
| Explanation and supporting references | LLM using those returned facts |

Use allowlisted, parameterized DB operations. Validate entity ID, permissions, timestamps, and units. If a required value is missing, do not substitute zero. For decimal-sensitive arithmetic, use Python `Decimal`. Keep percent and percentage points distinct. An explanation of headroom is not itself authorization to execute an action.

## How should metadata work for large files and collections?

Do not embed a large file as one block or rely on a filename alone. Preserve a document record and attach inherited plus local metadata to each section/chunk. The following is a suggested schema, to adapt to the corpus:

| Level | Suggested metadata | How it helps |
|---|---|---|
| Document | `document_id`, `source_uri`, `content_hash`, `document_type`, `owner`, `access_scope` | Identify sources, detect duplicates, enforce access |
| Version | `version_id`, `effective_from`, `effective_to`, `status`, `ingested_at` | Separate applicable policy from obsolete evidence; support historical queries |
| Section/chunk | `chunk_id`, `parent_section_id`, `section_path`, `page_start`, `page_end`, source offsets or region coordinates | Retrieve exact spans, expand parent context, produce traceable citations |
| Content | `language`, `content_type`, `entity_ids`, optional table ID/header/unit metadata | Select relevant material and preserve numeric meaning |
| Processing | `parser`, `parser_version`, `extraction_status`, chunk hash | Reprocess failures and identify changes without rebuilding everything |
| Relationships | Source/target entity IDs, relation type, supporting span, source version | Follow and inspect linked evidence |

Metadata helps in four places: **before retrieval**, filter by authorized scope and applicable dates; **during retrieval**, narrow by document type or entity when justified; **after retrieval**, recover adjacent/parent content and precise citations; **during updates**, identify chunks and links to replace or invalidate.

Example: for a question about the current Strategy X policy, first enforce access, then apply the relevant business-date interval and strategy identifier, and finally retrieve within that scope. For a historical question, select the historically applicable version rather than filtering only to today's active status. `ingested_at` is not the effective date. If versions overlap, flag a conflict.

For 200 GB of files, inventory formats and permissions, deduplicate by content hash, and process in restartable batches. Keep a manifest with file ID, hash, processing status, parser version, and last successful checkpoint. Retry failed files separately. Reindex changed files and invalidate dependent chunks, graph links, and caches. Start with a representative subset and measure extraction/retrieval quality before scaling. Incorrect metadata can exclude correct evidence, so validate extracted labels and dates.

## A practical implementation plan

### Step 1: Inventory and choose the correct parser

Group representative pages into digital text, complex layout, and scans. Use the three parser approaches above. Establish a reviewed sample containing difficult tables, multilingual scans, and mixed pages. Record failures explicitly and retain originals.

**Output:** normalized text/table records with page references, extraction method, and review status.

### Step 2: Add metadata and preserve versions

Create document and version records before chunking. Chunk at meaningful headings, paragraphs, and table boundaries. Attach stable IDs, section/page references, entity tags where reliable, effective dates, and access scope. Keep table headers and units with the values. For code, retain function/class boundaries and qualified symbols using AST-based parsing; unresolved dynamic relationships remain explicit.

**Output:** traceable, versioned chunks; structured tables/records for exact lookup; code symbols where applicable.

### Step 3: Set up deterministic retrieval paths

Index clause IDs, entity IDs, table keys, and source spans for direct lookup. When a question identifies an exact item, retrieve that record. When discovery needs semantic or lexical retrieval, use it to locate evidence and then fetch the validated original span. Separate quotations/facts from inference in the answer.

**Output:** exact evidence text with document version and location; explicit missing/conflicting-source outcomes.

### Step 4: Add knowledge-graph retrieval for multi-linkage questions

Select the workflows where answers depend on relationships. Extract or curate entities and edges, validate their evidence, and preserve versions. Route relationship questions to bounded traversal. Retrieve the supporting document/code evidence for the returned path, rather than returning a bare graph assertion.

**Output:** connected evidence paths and visible missing links. Use ordinary retrieval for questions that do not need traversal.

### Step 5: Connect DB numbers and Python arithmetic

Define approved lookups for live quantities and structured rules. Require entity ID, access scope, and freshness checks. Retrieve values, normalize compatible units, and calculate with Python. Store the operands, formula, result, and snapshot in the response trace.

**Output:** a deterministic result that the LLM can explain without recomputing or replacing its inputs.

### Step 6: Assemble an answer from the right sources

Identify which parts of the question need documents, linked evidence, code, live DB values, or previous conversation. Execute those bounded operations and combine their results. Keep memory separate from current authority. Ask for clarification or state insufficient evidence if a required input is unavailable. Cite source versions and preserve material qualifiers.

**Output:** factual answer plus clearly distinguished inference, evidence, and unresolved gaps.

### Step 7: Evaluate with RAGChecker and targeted checks

Use **[RAGChecker](https://github.com/amazon-science/RAGChecker)** for retrieval/generation diagnosis. Prepare records containing the question, reference answer, retrieved context with document IDs/text, and generated response, using the framework's documented schema. Configure its claim-extraction/checking models as documented. Inspect retrieval and generation metrics together to locate where evidence was lost or unsupported claims appeared.

Start with human-reviewed cases. Include wrong policy versions, incomplete linked evidence, damaged table headers, missing DB values, and questions that should abstain. Compare RAGChecker results with human judgments, investigate disagreements, and rerun the same cases after parser/retriever/prompt changes.

RAGChecker does not replace checking OCR text against page images or testing Python calculations directly. Check table-cell accuracy, version selection, authorization, and arithmetic with explicit expected outcomes. Keep a held-out set and record model/parser/index versions. Do not treat generated questions or model judgments as unquestionable reference labels.

**Output:** diagnosed retrieval/generation failures plus focused regression checks for the non-LLM stages.

## Reproduce the small example

Run `python rag_review_example.py` or `py rag_review_example.py` on Windows. It uses Python 3.10+ standard library only, synthetic inputs, and no network or API keys.

The example's separate fixture uses a 1.50% limit and 1.37% exposure, producing **0.13 percentage points**. Its naive branch uses superseded policy and old memory, producing 0.20. The regression tests cover versions, units, missing inputs, tenant scope, table associations, linked evidence, syntax IDs, and routing.

The example demonstrates controls; it does not execute the PDF parsers, DeepSeek OCR, RAGChecker, a live DB, or an LLM. Those are integration steps in the plan above. Use the companion RAG_REVIEW_CHECKLIST.md to review your implementation.
