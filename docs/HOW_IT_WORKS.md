# How UnvibeCode Works

UnvibeCode connects the business behaviour of a repository to the files and functions that implement it. Use the reports to understand what the product does, follow its implementation, and investigate the consequences of a change.

## 1. Map the repository locally

UnvibeCode reads supported source files and maps files, symbols, imports, calls and their static relationships. It divides source code into ordered sections and prepares connected context for analysis.

These relationships help you follow an implementation across files. They describe source-code connections, not a recording of a live application run.

## 2. Reconstruct business workflows

Structured code context is sent to the hosted UnvibeCode service for workflow and risk analysis. Repository scanning, graph construction and context preparation run locally. No customer OpenAI API key or activation key is required.

The workflow review connects entry points, decisions, state changes, external effects and outcomes. A workflow can span several files and functions.

The **Business Workflow Map** groups workflows by area. Each workflow explains what it does, its purpose, what it produces, who relies on it and why it matters, with supporting code you can inspect.

See [Data processing and privacy](DATA_PROCESSING.md) for the processing boundary.

## 3. Review business risks against the code

The risk review examines failures that can affect customers, permissions, data integrity, operations or other business outcomes. Accepted findings connect a trigger and the observed code behaviour to a business downside, supporting evidence, a proposed correction and an acceptance check.

Use a finding to investigate and test a specific path. A completed review with no accepted findings does not establish that every path is safe.

## 4. Explore the reports in this order

Open `00_unvibecode_results.html` in the generated results folder.

| Report tab | What to do |
| --- | --- |
| **Business Workflows** | Choose a workflow and understand its purpose, outcome and supporting code. |
| **Connected Code** | Find the files involved. Hover to preview connected code; click a file to choose downloadable context. |
| **Risk Findings** | Inspect reported failure paths, their code evidence and acceptance checks before changing behaviour. |
| **LLM Context** | Download the complete normalized repository context for further analysis. |

Keep the HTML files, context ZIP and any supporting folders together. The entry page loads companion files; it is not a self-contained copy of every report.

## 5. Continue with your AI assistant

In Connected Code, choose **Narrow**, **Optimal** or **Wider** context around a file. Start with Optimal, or choose Narrow for a smaller question. Give that context and the relevant HTML report to your assistant; in an editor such as Cursor, include the relevant repository files too.

Ask: “Explain this workflow from entry point to outcome. Cite the files and symbols, identify what my proposed change affects, and suggest tests for the reported failure paths.”

Use the complete repository ZIP when you need the broader context. Extract it and follow its README rather than assuming an assistant can read the entire archive in one prompt.

## Explore a real example

The [smolagents sample report](https://financeflash.github.io/unvibecode/gitdocs/smolagents/smolagents-main-unvibecode-analysis.html#business-workflows) contains **30 workflows across 15 areas**, including agent execution, memory and replay, and streaming. Open a workflow, inspect its supporting code, then switch to Connected Code or Risk Findings.

Those counts describe this sample; your repository will produce its own results.

## What happens with a large repository?

Under the [documented size limits](LIMITATIONS.md), repositories at or below approximately two million estimated source tokens are eligible for the full workflow and risk review. Above that threshold, UnvibeCode produces the Connected Code Map and Complete Repository Context without starting the deeper workflow and risk review.

Check the terminal and report status for the scope actually completed.

## Next steps

- [Install and run UnvibeCode](../README.md#try-unvibecode)
- [Understand each output and its files](OUTPUTS.md)
- [Troubleshoot installation and report problems](TROUBLESHOOTING.md)
