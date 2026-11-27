from pathlib import Path

import pytest

from unvibecode_graph.resolve import ImportResolver

FILES = ["src/lib.rs", "src/glob.rs", "src/pathutil.rs"]


@pytest.mark.xfail(strict=True, reason="#371: pub use keeps the visibility prefix")
def test_pub_use_links_to_the_reexported_module(tmp_path):
    pytest.importorskip("tree_sitter_language_pack")
    from unvibecode_graph.parse_ts import TreeSitterAstAdapter

    source = (
        "mod glob;\nmod pathutil;\n\n"
        "pub use crate::glob::{Glob, GlobBuilder};\n"
        "pub(crate) use crate::pathutil::normalize;\n"
    )
    parsed = TreeSitterAstAdapter().parse("rust", "src/lib.rs", Path("lib.rs"), source)
    uses = [i for i in parsed["imports"] if i["import_style"] == "use"]
    resolver = ImportResolver(tmp_path, FILES)
    resolved = [
        resolver.resolve("src/lib.rs", "rust", i)["resolved_file"] for i in uses
    ]
    assert [i["raw"] for i in uses] == [
        "crate::glob::Glob",
        "crate::glob::GlobBuilder",
        "crate::pathutil::normalize",
    ]
    assert resolved == ["src/glob.rs", "src/glob.rs", "src/pathutil.rs"]
