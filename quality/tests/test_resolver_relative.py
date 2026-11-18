"""'../' references resolve in every resolver that joins relative paths.

Regression test for the bug kept in the goldens until the refactor was done:
pathlib collapses './' but not '../', so 'src/lazy/../utils' never matched
a scanned file.
"""

from __future__ import annotations

from pathlib import Path

from unvibecode_graph.resolve import ImportResolver  # noqa: E402

FILES = [
    "src/utils/index.ts",
    "src/lazy/chart.ts",
    "lib/greeter.rb",
    "app/main.rb",
    "css/site.css",
    "blog/post.html",
    "index.html",
]


def resolver(tmp_path: Path) -> ImportResolver:
    return ImportResolver(tmp_path, FILES)


def test_js_ts_parent_directory(tmp_path):
    r = resolver(tmp_path).resolve(
        "src/lazy/chart.ts", "typescript", {"raw": "../utils"}
    )
    assert r["resolved_file"] == "src/utils/index.ts"


def test_ruby_require_relative_parent_directory(tmp_path):
    r = resolver(tmp_path).resolve(
        "app/main.rb",
        "ruby",
        {"raw": "../lib/greeter", "import_style": "require_relative"},
    )
    assert r["resolved_file"] == "lib/greeter.rb"


def test_html_parent_directory(tmp_path):
    r = resolver(tmp_path).resolve("blog/post.html", "html", {"raw": "../css/site.css"})
    assert r["resolved_file"] == "css/site.css"


def test_climbing_above_the_repository_does_not_resolve(tmp_path):
    r = resolver(tmp_path).resolve("index.html", "html", {"raw": "../index.html"})
    assert r["resolved_file"] is None
