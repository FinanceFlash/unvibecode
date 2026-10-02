# Understanding UnvibeCode Outputs

Open `00_unvibecode_results.html` in your results folder. Start with **Business Workflows**, then explore **Connected Code**, **Risk Findings** and **LLM Context**.

[Explore the complete smolagents sample report](https://financeflash.github.io/unvibecode/gitdocs/smolagents/smolagents-main-unvibecode-analysis.html#business-workflows): **30 workflows across 15 areas**, with supporting code and downloadable context.

## 1. Business Workflows — Business Workflow Map

**File:** `02_business_workflow_map.html`

Choose a workflow area, then read a workflow to understand:

- What it does and why it exists.
- What it produces and who relies on it.
- Why the workflow matters.
- Which code supports the explanation.

Use this view to connect product behaviour to implementation before reading files individually. In the smolagents sample, you can explore agent memory and replay, multi-step agent execution, and UI streaming.

[Explore business workflows](https://financeflash.github.io/unvibecode/gitdocs/smolagents/smolagents-main-unvibecode-analysis.html#business-workflows)

## 2. Connected Code — Connected Code Map

**File:** `01_connected_code_map_for_llm.html`

The interactive map shows static relationships between files and symbols. Hover over a file to preview connected code. Click a file to choose the context to download for your AI assistant.

| Context size | Approximate token budget | When to choose it |
| --- | --- | --- |
| **Narrow** | 30K | A focused question about a file and its nearby context. |
| **Optimal** | 45K | The recommended starting point for understanding connected implementation. |
| **Wider** | 75K | A question needing more surrounding code. |

These are context budgets, not a promise that every download contains that many tokens. Inspect the selection and use a size your assistant can accept.

Use the map to answer “Which code belongs with this file?” Then give the downloaded context to your assistant to investigate a workflow or proposed change.

[Explore connected code](https://financeflash.github.io/unvibecode/gitdocs/smolagents/smolagents-main-unvibecode-analysis.html#connected-code)

## 3. Risk Findings — Business Risk Findings

**File:** `03_business_risk_findings.html`

Read each finding through its trigger, code behaviour and business consequence. The report can include:

- Trigger and what the code does.
- Business rule, downside and impact.
- The code path that reaches the outcome.
- What to change and an acceptance check.
- Supporting files, symbols and code references.

The report may also identify additional code areas worth reviewing. Treat these review suggestions separately from the reported business flaws.

For example, the smolagents sample reports a timeout path where Python execution can continue occupying the local runner. Inspect the evidence and acceptance check before deciding how to address it.

A no-findings result applies to the completed review scope; it does not prove the repository is defect-free.

[Explore risk findings](https://financeflash.github.io/unvibecode/gitdocs/smolagents/smolagents-main-unvibecode-analysis.html#risk-findings)

## 4. LLM Context — Complete Repository Context

**File:** `complete_repository_context_for_llm.zip`

This bundle contains normalized source sections, connections and context selections for later analysis.

| File inside the ZIP | Contents |
| --- | --- |
| `manifest.json` | Repository identity, counts and bundle metadata. |
| `chunks.jsonl` | Source-code sections with file and line information. |
| `connections.jsonl` | Connections between code sections. |
| `selections.jsonl` | Precomputed context selections by file and scope. |
| `README.md` | Instructions for using the bundle. |

Use Connected Code for a focused download. Use the complete ZIP for broader repository analysis, API workflows or a reusable handoff. Extract it and read its README; avoid pasting the entire bundle into one prompt without checking your assistant's limits.

[Open repository context downloads](https://financeflash.github.io/unvibecode/gitdocs/smolagents/smolagents-main-unvibecode-analysis.html#llm-context)

## Keep the report files together

Results are saved under `shipready_results/analysis_<timestamp>/customer_results/` as described in the [quick start](QUICKSTART.md). Open the entry file in that folder.

Keep these files together when moving or sharing a review:

- `00_unvibecode_results.html` and any report page it redirects to.
- The three numbered report HTML files listed above.
- `complete_repository_context_for_llm.zip`.
- Any companion folders, including `_support/` when present.

The published smolagents entry page is `smolagents-main-unvibecode-analysis.html`. Downloading only that page does not download the reports it displays.

If an output is missing, check the review status and [repository limits](LIMITATIONS.md), then follow [Troubleshooting](TROUBLESHOOTING.md).
