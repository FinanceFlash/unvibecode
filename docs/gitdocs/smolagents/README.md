# smolagents analysis pages

The public experience follows **Understand → Ask → Build**. It uses the supplied UnvibeCode export as its source of truth.

## Files

| Location | Purpose |
| --- | --- |
| `index.html` | Understand: all 12 original workflow areas and 26 workflow cards; initial Build section. |
| `ask.html` | Workflow questions, connected-code selection, context preview, JSON copy/download and full ZIP download. |
| `connected-code.html` | Embedded graph generated from the original report's visualization library, nodes, edges and layout. |
| `assets/` | Website styles and interaction code; generated workflow metadata. |
| `design/build.py` | Standard-library-only page generator. |
| `design/templates/` | Editable page layout templates. |
| `original/` | Unchanged reports, original context store and repository context ZIP. |

## Update the pages

From the repository root:

```sh
python docs/gitdocs/smolagents/design/build.py
```

Edit the Ask layout in `design/templates/ask.html` and its presentation/interaction in `assets/ask.css`, `assets/ask.js` and `assets/map.js`. The Understand wrapper remains in `design/build.py`. Rebuild and commit the generated HTML and `assets/workflows.js` alongside source edits. No root-level scripts folder is needed for these pages.

The generator derives workflow navigation, questions, answer excerpts and source references from the original workflow report. Answers are explicitly attributed excerpts, not new model-generated claims. The Understand renderer retains every original workflow section apart from added navigation IDs.

The graph retains the exported topology. Clicking it selects a starting file; JSON downloads happen only through the explicit action. The accessible file picker offers the same selection. Context sizes, ordered code chunks and cross-file connections come directly from `original/_support/fast_lane_context_store.js`. A copied/downloaded selection includes the user's question and source metadata. The original context ZIP remains unchanged.

Serve `docs/` through HTTP for local preview. Ask and its map use same-origin messaging with sender checks. The pages make no LLM requests. Session storage preserves selections and prompts within the browser tab; workflow/file/scope URLs can be bookmarked. Business risk findings remain in the original archive and are not linked or presented in Understand or Ask.

## Source notes

The supplied export records `smolagents-main`, but not a repository commit SHA. No runtime verification or performance benchmark is claimed. The original local-executor workflow uses sandbox wording; the executor's source docstring says it is not a security sandbox. These are source-review notes, not changes to the original report.
