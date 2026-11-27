from pathlib import Path

import pytest

from unvibecode_graph.resolve import ImportResolver

FILES = ["src/lib.rs", "src/config.rs", "src/error.rs", "src/store.rs", "src/x.rs"]


@pytest.mark.parametrize(
    ("text", "paths"),
    [
        (
            "crate::{config::Config, error::Error, store::Store}",
            ["crate::config::Config", "crate::error::Error", "crate::store::Store"],
        ),
        (
            "crate::{\n    config::Config,\n    error::Error,\n};",
            ["crate::config::Config", "crate::error::Error"],
        ),
        (
            "crate::{config::{self, Config}, error::Error as E}",
            ["crate::config", "crate::config::Config", "crate::error::Error"],
        ),
        ("crate::store::*", ["crate::store::*"]),
        ("std::io::Read", ["std::io::Read"]),
    ],
)
def test_use_group_is_expanded_into_paths(text, paths):
    from unvibecode_graph.parse_ts import rust_use_paths

    assert rust_use_paths(text) == paths


def test_grouped_use_links_every_module(tmp_path):
    pytest.importorskip("tree_sitter_language_pack")
    from unvibecode_graph.parse_ts import TreeSitterAstAdapter

    source = (
        "use crate::{\n    config::Config,\n    error::Error,\n    store::Store,\n};\n"
    )
    parsed = TreeSitterAstAdapter().parse("rust", "src/x.rs", Path("src/x.rs"), source)
    resolver = ImportResolver(tmp_path, FILES)
    resolved = sorted(
        resolver.resolve("src/x.rs", "rust", imp)["resolved_file"]
        for imp in parsed["imports"]
    )
    assert resolved == ["src/config.rs", "src/error.rs", "src/store.rs"]
