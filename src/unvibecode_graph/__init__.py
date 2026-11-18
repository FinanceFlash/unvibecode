"""UnvibeCode connected code graph (the fast lane).

Read the modules in import order; each one only imports the ones above it:

  config     settings and language tables
  util       path, text and syntax-tree helpers
  parse_py   Python      -> imports, symbols, entities   (stdlib ast)
  parse_go   Go syntax helpers + usage collector (for golinks)
  parse_ts   JS/TS/Go/Rust/PHP/Ruby -> same               (tree-sitter)
  parse_web  HTML/CSS    -> links, scripts, @import, url()
  resolve    import string -> repository file
  golinks    Go package catalog -> cross-file Go symbol edges
  build      repository  -> file graph                   (stage one)
  link       file graph  -> resolved symbol graph        (stage two)
  chunk      files       -> code chunks + chunk graph
  context    chunks      -> per-file connected-code downloads
  render     interactive graph HTML + repository profile
  pipeline   run(): the order everything above runs in

Use:

    from unvibecode_graph import Config, run
    result = run("path/to/repo", "out")          # -> Result(run_dir, resolved_graph, timing)

or from a shell: python -m unvibecode_graph path/to/repo --out out
"""

from .config import Config
from .pipeline import Result, run

__all__ = ["Config", "Result", "run"]
