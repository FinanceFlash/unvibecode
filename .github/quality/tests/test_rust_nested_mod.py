import pytest

from unvibecode_graph.resolve import ImportResolver

FILES = [
    "src/lib.rs",
    "src/net.rs",
    "src/net/tcp.rs",
    "src/tcp.rs",
    "src/net/mod.rs",
    "src/net/ip.rs",
    "src/net/ip/v4.rs",
    "src/bin/tool.rs",
    "src/bin/util.rs",
    "tests/integration.rs",
    "tests/common/mod.rs",
    "src/shapes.rs",
]


def resolve(tmp_path, source_file, name):
    imp = {"raw": name, "import_style": "mod"}
    return ImportResolver(tmp_path, FILES).resolve(source_file, "rust", imp)[
        "resolved_file"
    ]


@pytest.mark.parametrize(
    ("source_file", "name", "expected"),
    [
        ("src/net.rs", "tcp", "src/net/tcp.rs"),
        ("src/net/ip.rs", "v4", "src/net/ip/v4.rs"),
    ],
)
def test_module_declared_in_name_rs_lives_in_its_folder(
    tmp_path, source_file, name, expected
):
    assert resolve(tmp_path, source_file, name) == expected


@pytest.mark.parametrize(
    ("source_file", "name", "expected"),
    [
        ("src/lib.rs", "shapes", "src/shapes.rs"),
        ("src/net/mod.rs", "ip", "src/net/ip.rs"),
        ("src/bin/tool.rs", "util", "src/bin/util.rs"),
        ("tests/integration.rs", "common", "tests/common/mod.rs"),
    ],
)
def test_crate_roots_and_mod_rs_keep_their_own_folder(
    tmp_path, source_file, name, expected
):
    assert resolve(tmp_path, source_file, name) == expected
