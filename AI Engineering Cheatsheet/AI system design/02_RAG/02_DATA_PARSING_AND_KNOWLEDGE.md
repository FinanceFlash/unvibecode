# Data, Parsing, and Knowledge Representation

Bad parsing is data corruption upstream of retrieval.

If a table value, footnote, heading relationship, or access label is lost during ingestion, no retriever can reliably recover it later.

## 1. Start from source type

Do not choose one parser for every document.

| Source | Starting approach |
| --- | --- |
| Born-digital PDF | PyMuPDF or another text/layout-aware parser |
| Complex layout / tables | Structured document parser such as Docling |
| Scanned pages | Image extraction + OCR |
| Spreadsheet | Native structured parsing |
| HTML | DOM-aware extraction |
| Code | AST / symbol-aware parser |
| Database | Keep structured; do not convert to chunks |

The existing [RAG practical guide](../../../skills/unvibecode-rag-review/references/RAG_PRACTICAL_GUIDE.md) includes concrete parser guidance and a hybrid parser approach.

## 2. Preserve structure that changes meaning

Important structure can include:

- headings and sections,
- page numbers,
- table row/column relationships,
- footnotes,
- lists,
- code boundaries,
- source links,
- document version,
- effective date,
- ownership/tenant scope.

Text extraction that preserves words but destroys these relationships may still be unusable.

## 3. Treat OCR uncertainty explicitly

OCR is useful when the source is actually image-based.

It should not silently replace higher-quality text extraction when a good text layer already exists.

Validate critical fields separately:

- amounts,
- dates,
- IDs,
- units,
- negations,
- table cells.

Average OCR accuracy can look excellent while one corrupted amount breaks the answer.

## 4. Metadata is part of the retrieval contract

For large collections, metadata should answer:

- Which tenant/resource owns this?
- Which product or region does it apply to?
- What version is it?
- When did it become effective?
- When was it indexed?
- Is it active, superseded, or deleted?
- Which parser created this representation?

Use metadata to enforce eligibility before semantic ranking where it carries access or applicability rules.

## 5. Version knowledge, not only documents

A source can change while its filename remains the same.

Preserve enough identity to distinguish:

- original source version,
- parser version,
- chunk/index version,
- embedding version,
- retrieval timestamp.

Do not combine incompatible versions silently in one answer.

## 6. Build new indexes beside active ones

For important systems:

**build → validate → qualify → switch pointer → observe → retire old**

Do not destroy the active index before the replacement has been tested.

Validate:

- parse completeness,
- retrieval behavior,
- access filters,
- deletion propagation,
- source freshness,
- representative end-to-end questions.

## 7. Common production failures

### Parser upgrade changes tables

Infrastructure is healthy, but values move into the wrong columns.

**Control:** parser regression fixtures tied to original pages.

### Stale source remains searchable

A superseded policy ranks highly because it is semantically similar.

**Control:** explicit version/effective-date filters and precedence rules.

### Deletion removes source but not embeddings

Deleted content still appears through the index or cache.

**Control:** derivation links and deletion propagation across source, chunks, embeddings, caches, and summaries.

### Permission metadata is missing during ingestion

The system later treats the chunk as broadly visible.

**Control:** never index protected content without valid access metadata.

The parser is not a preprocessing detail. It is the first evidence-preservation boundary.
