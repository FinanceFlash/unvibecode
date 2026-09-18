# UnvibeCode RAG Review

A reusable review skill, practical guide, checklist, and runnable example for developers building RAG systems.

| Start here | Purpose |
| --- | --- |
| [Practical guide](references/RAG_PRACTICAL_GUIDE.md) | Parser choices, hybrid parsing, deterministic retrieval, knowledge graphs, metadata, DB lookups, Python arithmetic, and RAGChecker |
| [Review checklist](references/RAG_REVIEW_CHECKLIST.md) | Evidence-based checks and regression scenarios |
| [Review skill](SKILL.md) | Instructions for an AI assistant reviewing an accessible design or implementation |
| [Python example](scripts/rag_review_example.py) | Reproducible synthetic demonstration with 21 regression tests |

## Use the review skill

Give your assistant access to this entire folder, including its references and scripts, and ask:

> Use skills/unvibecode-rag-review/SKILL.md to review this RAG design or repository. Cite the evidence for each finding and distinguish confirmed problems from unverified risks.

For clients that support skill installation, install the complete folder using that client's skill mechanism. Referencing a file alone does not install a skill or expose an MCP tool.

## Run the example

From the repository root, with Python 3.10 or newer:

```bash
python skills/unvibecode-rag-review/scripts/rag_review_example.py
```

On Windows, `py` can replace `python`. No extra packages, API keys, or network access are needed. The guide's shorter commands assume you are inside this folder's `scripts` directory.

The example demonstrates simulated routing to PyMuPDF, Docling, and PyMuPDF + DeepSeek OCR; metadata-filtered exact lookup; source-backed graph traversal; an actual in-memory SQLite query; and Python Decimal arithmetic. Its synthetic fixture yields 0.13 percentage points of headroom.

PDF extraction and OCR are simulated. The example does not run an LLM, a live external database, or a RAGChecker evaluation, and passing its tests does not validate your system.

## Prepare RAGChecker input

```bash
python skills/unvibecode-rag-review/scripts/rag_review_example.py --ragchecker-json > ragchecker_inputs.json
```

This exports a synthetic case in the documented input format. Configure and run [RAGChecker](https://github.com/amazon-science/RAGChecker) separately. No evaluation scores are produced by this example.

For the broader question-to-answer business workflow, see the [RAG workflow pack](../../prebuilt-workflow-paths/rag-question-answering-with-evidence-and-citations/README.md).
