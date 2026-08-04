# UnvibeCode

**Unvibe complex code. Trace business workflows.**

Complex code hides connections, workflows, and business risks.

**Unvibe it.**

![UnvibeCode AI codebase analysis demo showing connected code, business workflows, and risk findings](docs/assets/unvibecode-demo.gif)

Explore connected code in an interactive graph, give LLMs the right context, trace business workflows, and identify critical business risks.

## Review your codebase in two commands

```bash
pip install unvibecode
python -m unvibecode review --repository "/path/to/repository"
```

Windows example:

```powershell
python -m unvibecode review --repository "D:\upstox"
```

No activation key. No OpenAI API key. The repository path is the only required input.

UnvibeCode displays live progress, opens the completed reports, and saves the results automatically under `./shipready_results`.

## One review. Four practical outputs.

### 1. Understand complex code connections

The **Connected Code Map for LLMs** shows how files, symbols, imports, and calls work together.

Hover over a file to preview it. Click the file to trace its connected code and download the relevant code as one compact, LLM-ready package.

![Interactive code dependency graph showing connected files and downloadable LLM context](docs/assets/connected-code-map.png)

### 2. Give LLMs the right repository context

Stop manually selecting files or pasting unrelated code into an LLM.

The **Complete Repository Context** organizes code into reusable chunks with filenames, line references, verified connections, and contextual selections. Use the complete ZIP later, or download a smaller connected-code package directly from the graph.

```text
complete_repository_context_for_llm.zip
├── manifest.json
├── chunks.jsonl
├── connections.jsonl
├── selections.jsonl
└── README.md
```

### 3. Trace code as business workflows

A file tree explains repository structure, but it does not explain how the software performs business operations.

The **Business Workflow Map** connects entry points, decisions, state changes, external calls, and business outcomes into understandable workflows.

![Business workflow analysis connecting code paths to operational outcomes](docs/assets/business-workflow-map.png)

### 4. Identify critical business workflow risks

The **Business Risk Findings** report identifies critical workflow risks in the code and shows the supporting evidence.

Each finding explains:

- What triggers the risk
- What the code currently does
- The affected business workflow
- The potential business impact
- What should change
- How to verify the correction
- The exact supporting code evidence

If no finding passes the evidence threshold, the report clearly records a no-findings outcome for the completed review scope.

![Business risk finding with impact, remediation, acceptance check, and code evidence](docs/assets/business-risk-findings.png)

## How UnvibeCode works

### 1. Map the repository locally

UnvibeCode scans supported source files and resolves meaningful file, symbol, import, and call relationships.

### 2. Build connected LLM context

Code is organized into reusable chunks and connected packages. Selecting a file retrieves the surrounding code needed to understand it without sending the entire repository to an LLM.

### 3. Reconstruct business workflows

Related code paths are interpreted as workflows containing triggers, decisions, state changes, external effects, and business outcomes.

### 4. Review critical business risks

Completed workflows are checked for failures that may affect customers, payments, permissions, data integrity, operations, or other important business outcomes.

### 5. Produce customer-ready results

For a supported repository, the automatically created results folder contains:

```text
shipready_results/
└── analysis_<timestamp>/
    └── customer_results/
        ├── 01_connected_code_map_for_llm.html
        ├── complete_repository_context_for_llm.zip
        ├── 02_business_workflow_map.html
        └── 03_business_risk_findings.html
```

## Repository-size behaviour

Supported repositories receive the complete code, workflow, and risk review.

Repositories above approximately two million estimated source tokens receive the Connected Code Map and Complete Repository Context. The deeper Business Workflow and Risk Review does not run above that threshold.

Read [How UnvibeCode works](docs/HOW_IT_WORKS.md) for details.

## Data processing

Repository parsing, dependency mapping, connected-context preparation, and report rendering run locally.

Structured context required for business workflow and risk analysis is securely sent to the hosted UnvibeCode service. Provider credentials remain server-side.

Review only repositories you are authorized to process.

Read the complete [data-processing explanation](docs/DATA_PROCESSING.md).

## Requirements

- Python 3.11 or newer
- Internet access for hosted business analysis
- Read access to the repository being reviewed

## Documentation

- [Quick start for Windows, macOS, and Linux](docs/QUICKSTART.md)
- [Understanding the four outputs](docs/OUTPUTS.md)
- [How UnvibeCode works](docs/HOW_IT_WORKS.md)
- [Data processing and privacy](docs/DATA_PROCESSING.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Public preview policy](docs/PUBLIC_PREVIEW.md)
- [Version history](CHANGELOG.md)

## Contributing, security, and license

- Read the [contribution guidelines](CONTRIBUTING.md) before proposing a change.
- Report vulnerabilities through the process described in [SECURITY.md](SECURITY.md).
- Reuse and distribution are governed by the repository's [license](LICENSE).

