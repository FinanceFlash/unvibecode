from pathlib import Path

import pytest

from unvibecode_graph.resolve import ImportResolver

FILES = [
    "src/lib.rs",
    "src/normal.rs",
    "src/feature.rs",
    "src/custom/feature_impl.rs",
    "app/src/lib.rs",
    "app/src/custom/feature_impl.rs",
    "tokio/src/process/mod.rs",
    "tokio/src/process/unix/mod.rs",
]


def mod_imports(source):
    pytest.importorskip("tree_sitter_language_pack")
    from unvibecode_graph.parse_ts import TreeSitterAstAdapter

    parsed = TreeSitterAstAdapter().parse("rust", "src/lib.rs", Path("lib.rs"), source)
    return [
        (i["raw"], i["import_style"])
        for i in parsed["imports"]
        if i["import_style"].startswith("mod")
    ]


@pytest.mark.xfail(strict=True, reason="#663: #[path] modules are not resolved")
@pytest.mark.parametrize(
    ("source_file", "raw", "expected"),
    [
        ("app/src/lib.rs", "custom/feature_impl.rs", "app/src/custom/feature_impl.rs"),
        ("tokio/src/process/mod.rs", "unix/mod.rs", "tokio/src/process/unix/mod.rs"),
    ],
)
def test_path_attribute_resolves_next_to_the_declaring_file(
    tmp_path, source_file, raw, expected
):
    imp = {"raw": raw, "import_style": "mod_path"}
    resolved = ImportResolver(tmp_path, FILES).resolve(source_file, "rust", imp)
    assert resolved["resolved_file"] == expected


@pytest.mark.xfail(strict=True, reason="#663: #[path] modules are not resolved")
def test_path_attribute_becomes_a_path_import():
    source = (
        'mod normal;\n\n#[path = "custom/feature_impl.rs"]\n'
        "#[cfg(unix)]\nmod feature;\n"
    )
    assert mod_imports(source) == [
        ("normal", "mod"),
        ("custom/feature_impl.rs", "mod_path"),
    ]


@pytest.mark.xfail(strict=True, reason="#663, #390: inline mod becomes a file import")
def test_inline_module_is_not_a_file_import():
    source = (
        "pub mod feature {\n    pub fn f() {}\n}\n\n"
        "#[cfg(test)]\nmod tests {\n    #[test]\n    fn t() {}\n}\n"
    )
    assert mod_imports(source) == []
