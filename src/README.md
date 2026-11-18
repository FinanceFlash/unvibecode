# Unvibecode Graph

Build an interactive Connected Code Map for a repository on your computer. The scanner reads local source files, resolves connections and writes an HTML map, graph JSON and a repository context ZIP. You can run it without an Unvibecode account, API key or server.

## Run from your fork

Fork and clone the repository, or extract this ZIP. Open a terminal in the directory containing this README and pyproject.toml. Use Python 3.11 or newer.

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m unvibecode_graph src --out ../graph-results --open
```

**macOS or Linux**

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m unvibecode_graph src --out ../graph-results --open
```

This example maps the graph package itself. Replace `src` with the path to the local repository you want to analyze. Quote paths containing spaces. Choose an output directory outside the scanned repository. Installing dependencies requires access to a Python package index. Language-specific parsing also depends on available Tree-sitter grammars.

## Read the results

The command prints the path to `fast_lane_symbol_resolution_graph.html`. Open it to explore the map. Omit `--open` on a headless machine. The same run directory contains `shipreadyv2_resolved_graph.json` for programmatic use and `shipready_complete_repository_context.zip` with source context from the scanned repository.

The package lives in `src/unvibecode_graph/`. The editable install picks up Python source changes when you rerun the command.
