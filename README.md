# UnvibeCode

## Understand complex codebases by tracing business workflows, business logic, connected code, edge cases, and evidence-backed risks.

*Unvibe complex code. Trace what the business actually does.*

![UnvibeCode AI codebase analysis demo showing connected code, business workflows, and risk findings](docs/assets/unvibecode-codebase-analysis-demo.gif)

[![Quality checks](https://github.com/FinanceFlash/unvibecode/actions/workflows/test.yml/badge.svg)](https://github.com/FinanceFlash/unvibecode/actions/workflows/test.yml)
[![PyPI version](https://img.shields.io/pypi/v/unvibecode.svg)](https://pypi.org/project/unvibecode/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://pypi.org/project/unvibecode/)
[![License](https://img.shields.io/github/license/FinanceFlash/unvibecode.svg)](LICENSE)

### Your LLM helped write 100,000 lines of code. Now how do you understand what it actually built?

Reading files one by one does not show the complete business workflow. Pasting a large repository into an LLM can also lose the connections between entry points, state changes, dependencies, edge cases, and business outcomes.

**UnvibeCode reverse-engineers the codebase into connected code, business workflows, business logic, and evidence-backed risks.**

## Try UnvibeCode

### Windows

```powershell
python -m pip install --upgrade unvibecode
python -m unvibecode review --repository "D:\path\to\repository"
```

### macOS / Linux

```bash
python3 -m pip install --upgrade unvibecode
python3 -m unvibecode review --repository "/path/to/repository"
```

No activation key. No customer OpenAI API key. The repository path is the only required input.

If UnvibeCode is useful for a codebase you need to understand, **star the repository to save it for later**.

## One review. Four practical outputs.

### 1. Connected Code Map

See how files, symbols, imports, and calls work together. Select a file to trace its connected code and download a compact package for deeper LLM analysis.

![Interactive code dependency graph showing connected files and downloadable LLM context](docs/assets/connected_code_map.png)

### 2. LLM-ready repository context

Stop manually selecting files or pasting unrelated code into an LLM. UnvibeCode prepares complete and connected repository context with filenames, line references, verified relationships, and reusable selections.

### 3. Business Workflow Map

A file tree explains repository structure. It does not explain how the software performs a business operation.

UnvibeCode reconstructs entry points, decisions, state changes, external calls, and business outcomes into understandable workflows.

![Business workflow analysis connecting code paths to operational outcomes](docs/assets/business_workflow_map.png)

### 4. Evidence-backed Business Risk Findings

UnvibeCode reviews completed workflows for failures that may materially affect customers, money, permissions, data integrity, operations, or other important business outcomes.

Each published finding includes the affected workflow and supporting code evidence.

![Business risk finding with impact, remediation, acceptance check, and code evidence](docs/assets/business_risk_findings.png)

## Why UnvibeCode instead of stopping at code search, graphs, PR review, or LLM context?

Tools such as Probe, Graphify, PR-Agent / Qodo Merge, and Repomix solve useful parts of code understanding. UnvibeCode goes further by making **the business workflow implemented across the repository** the main unit of analysis.

| Tool | Strong at | Where UnvibeCode goes further |
| --- | --- | --- |
| [**Probe**](https://github.com/probelabs/probe) | AST-aware code search, extraction, and code context for AI agents | Search and retrieval help locate code; UnvibeCode reconstructs the end-to-end business workflow that crosses those files and functions |
| [**Graphify**](https://github.com/Graphify-Labs/graphify) | Building and querying a knowledge graph of code, documents, and relationships | A graph explains how things connect; UnvibeCode additionally reconstructs business workflows, edge cases, and evidence-backed business risks |
| [**PR-Agent / Qodo Merge**](https://github.com/The-PR-Agent/pr-agent) | Reviewing pull requests, describing changes, and suggesting improvements around a diff | PR review starts from changed code; UnvibeCode reverse-engineers the existing repository and its business workflows beyond a single change set |
| [**Repomix**](https://github.com/yamadashy/repomix) | Packaging a repository into AI-friendly context for LLMs | Repository context gives an LLM source material; UnvibeCode additionally reconstructs workflow logic, state changes, edge cases, and business consequences |
| **UnvibeCode** | **Connected code + business workflows + business logic + edge cases + evidence-backed business risks** | **The codebase is reviewed through the business workflows it implements, not only files, graphs, diffs, or context packages** |

**The core unit in UnvibeCode is not a file or a diff. It is the business workflow implemented across the codebase.**

## What developers found useful in real repository trials

Developer trials across public and personal repositories repeatedly highlighted three useful parts of the product:

- **Business risks that could be independently checked:** in a trial on the Rich Python library, a developer independently reproduced a Business Risk Finding surfaced by UnvibeCode.
- **Business workflows instead of only repository structure:** in a Django project, a developer found the Business Workflow Map useful for understanding workflows covering student records, API operations, registration, and authentication/dashboard delivery.
- **Useful output even when a repository is too large for the deeper review:** in a trial on a repository with about 12.6M estimated source tokens across 3,914 source files, UnvibeCode still produced the Connected Code Map and downloadable repository context while safely skipping the deeper workflow review.

## What is UnvibeCode?

UnvibeCode is an open-source codebase analysis tool that helps developers **understand complex codebases** by tracing business workflows, business logic, connected code, entry points, edge cases, and evidence-backed risks.

### How do you understand a complex codebase?

Start with **business workflows, not individual files**. UnvibeCode traces each workflow to its connected code, entry points, dependencies, state changes, and edge cases so developers can understand how the system actually works.

### How do you trace business workflows in a codebase?

UnvibeCode reconstructs **business workflows and business logic** across files and functions and connects each workflow to its entry points, decisions, dependencies, state changes, and supporting code evidence.

## Supported languages

UnvibeCode 0.3.3 supports connected-code mapping and LLM-context preparation for:

| Language | Recognized file types |
| --- | --- |
| Python | `.py` |
| JavaScript | `.js`, `.jsx`, `.mjs`, `.cjs` |
| TypeScript | `.ts`, `.tsx` |
| Rust | `.rs` |
| PHP | `.php` |
| Ruby | `.rb` |
| Web assets | `.html`, `.htm`, `.css` |

C, C++, Java, Go, C#, Kotlin, and Swift files are detected but are not yet included in full connected-code analysis.

## Documentation

- [Quick start for Windows, macOS, and Linux](docs/QUICKSTART.md)
- [Understanding the four outputs](docs/OUTPUTS.md)
- [How UnvibeCode works](docs/HOW_IT_WORKS.md)
- [Repository limits and responsible-use boundaries](docs/LIMITATIONS.md)
- [Data processing and privacy](docs/DATA_PROCESSING.md)
- [Troubleshooting and support](docs/TROUBLESHOOTING.md)
- [Public preview and public-repository reviews](docs/PUBLIC_PREVIEW.md)
- [UnvibeCode Engineering Challenge 2026](docs/UNVIBECODE_ENGINEERING_CHALLENGE_2026.md)
- [Contributor and challenge credentials](docs/OSS_Contributor_Credentials/README.md)

## Support and feedback

For reproducible package problems or feature requests, open a [GitHub issue](https://github.com/FinanceFlash/unvibecode/issues).

For product questions, public-repository review requests, or collaboration enquiries, email [divya.singaravelu@iiml.org](mailto:divya.singaravelu@iiml.org).

## Contributing and license

- Read the [contribution guidelines](.github/CONTRIBUTING.md) before proposing a change.
- Explore the [pre-built business workflow packs](prebuilt-workflow-paths/README.md) or contribute a new one using the MECE rules.
- Look for a focused starting point in [good first issues](https://github.com/FinanceFlash/unvibecode/labels/good%20first%20issue).
- Reuse and distribution are governed by the repository's [license](LICENSE).
