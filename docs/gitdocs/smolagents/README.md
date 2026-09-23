# smolagents sample analysis

The homepage introduces three sample outputs: **Business workflows**, **Connected code map**, and **Download LLM context**. All three are available on `index.html` through same-page navigation.

## Page organization

| Path | Purpose |
| --- | --- |
| `smolagents-main-unvibecode-analysis.html` | Supplied entry-page redirect, connected to `full-report.html`; preserves the selected output hash. |
| `full-report.html` | Complete tabbed HTML report linked from the homepage hero; uses the existing original workflow, code-map, risk and ZIP exports. |
| `index.html` | Original business workflow section, followed by the connected-code map and context downloads. |
| `connected-code.html` | Embedded original graph, styled to match the website. |
| `ask.html` | Compatibility redirect for previously shared links. |
| `assets/outputs.css` | Context-control styling scoped to avoid changing workflow styling. |
| `assets/outputs.js` | File/context selection, preview, JSON copy/download, persistence and navigation. |
| `assets/map.js` | Same-origin graph selection bridge and graph styling. |
| `design/build.py` | Standard-library page generator. |
| `design/templates/outputs.html` | Editable connected-code and download section. |
| `original/` | Six unchanged source exports, including the context store and full ZIP. |

Rebuild from the repository root:

```sh
python docs/gitdocs/smolagents/design/build.py
```

The renderer preserves all 12 original workflow areas and 26 workflow cards, their descriptions, outcomes and supporting code. The workflow sidebar and its layout are preserved. The output wrapper and homepage summary provide access to the existing analysis rather than a separate Understand/Ask/Build journey.

The graph retains the exported nodes, edges and layout. Its file picker is an accessible alternative to graph selection. Each narrow/optimal/wider context selection uses the original ordered chunks and connections. Users can preview the payload, add a question, copy it or download JSON. The complete repository ZIP is unchanged. Browser session storage retains file, scope and question; URLs carry file/scope selections. No LLM request is made by these pages.

Serve `docs/` over HTTP for local preview; graph messaging validates the origin and sender. Business risk findings remain in the unchanged original exports but are not presented in this experience.

The export identifies `smolagents-main` without a commit SHA. No runtime or performance evaluation is claimed. Original wording is retained; the local executor's own code states that it is not a security sandbox.


The full report shell comes from the supplied `smolagents-main-unvibecode-analysis.html`. Its asset URLs are resolved to `original/`, and its workflow count matches those exports (26 workflows across 12 areas). It is maintained separately from the generated `index.html`; rebuilding that page does not overwrite it. The existing sample exploration links remain available.

