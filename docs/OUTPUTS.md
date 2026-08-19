# Understanding UnvibeCode Outputs

For a supported repository, UnvibeCode produces four customer-facing deliverables.

## 1. Connected Code Map for LLMs

`01_connected_code_map_for_llm.html`

The interactive graph shows meaningful file, symbol, import, and call relationships.

Use it to:

- Explore a complex codebase visually
- Hover over a file to preview its context
- Click a file to trace connected code
- Download a focused LLM-ready code package
- Choose narrow, optimal, or wider connected context

The graph layout is an exploration interface. Downloaded context is selected from the complete resolved graph rather than from a reduced visual subset.

## 2. Complete Repository Context

`complete_repository_context_for_llm.zip`

This normalized bundle stores source chunks once and preserves the information required to assemble contexts later.

```text
complete_repository_context_for_llm.zip
├── manifest.json
├── chunks.jsonl
├── connections.jsonl
├── selections.jsonl
└── README.md
```

The ZIP is intended for storage, automation, and later LLM or API workflows. It should not normally be sent to an LLM as one large prompt.

## 3. Business Workflow Map

`02_business_workflow_map.html`

The workflow report connects technical implementation paths to understandable business operations. It shows:

- What starts a workflow
- Important decisions and state changes
- External calls and material effects
- The business object being changed
- The resulting customer or operational outcome

## 4. Business Risk Findings

`03_business_risk_findings.html`

The risk report identifies critical business workflow risks and shows the supporting code evidence. Each accepted finding explains:

- Trigger
- Current code behaviour
- Business rule
- Business downside
- Affected customer, asset, or operation
- Recommended correction
- Acceptance check
- Supporting files, symbols, and line references

If no candidate passes the evidence threshold, the report records a clear no-findings outcome for the completed review scope.

## Results directory

UnvibeCode's reports are generated under the `shipready_results/` folder — this is expected, not an error:
```text
shipready_results/
└── analysis_<timestamp>/
    └── customer_results/
        ├── 01_connected_code_map_for_llm.html
        ├── complete_repository_context_for_llm.zip
        ├── 02_business_workflow_map.html
        └── 03_business_risk_findings.html
```

