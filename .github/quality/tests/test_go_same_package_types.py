from pathlib import Path

import pytest

from unvibecode_graph.golinks import build_go_catalog, resolve_go_usages

MODELS = "package store\n\ntype User struct {\n\tName string\n}\n"
SERVICE = 'package store\n\nfunc CreateUser() User {\n\treturn User{Name: "a"}\n}\n'


def node(file, entities, usages=()):
    package = {"kind": "package", "name": "store", "scope": "package"}
    return {
        "file": file,
        "language": "go",
        "entities": [package, *entities],
        "imports": [],
        "go_usages": list(usages),
    }


def user_type(file, line):
    return {
        "kind": "struct",
        "name": "User",
        "exported": True,
        "scope": "package",
        "line_range": {"start_line": line},
    }


@pytest.mark.xfail(strict=True, reason="#547: same-package type use gives no edge")
def test_same_package_type_links_to_its_file():
    models = node("store/models.go", [user_type("store/models.go", 3)])
    usage = {"kind": "same_package_type", "name": "User", "line": 3}
    service = node("store/service.go", [], [usage])
    edges, unresolved = resolve_go_usages(service, build_go_catalog([models, service]))
    assert [(e["target"], e["symbol"]) for e in edges] == [("store/models.go", "User")]
    assert not unresolved


@pytest.mark.xfail(strict=True, reason="#547: same-package type use gives no edge")
def test_same_package_type_declared_twice_is_ambiguous():
    a = node("store/a.go", [user_type("store/a.go", 3)])
    b = node("store/b.go", [user_type("store/b.go", 3)])
    usage = {"kind": "same_package_type", "name": "User", "line": 3}
    service = node("store/service.go", [], [usage])
    edges, unresolved = resolve_go_usages(service, build_go_catalog([a, b, service]))
    assert not edges
    assert [u["reason"] for u in unresolved] == ["ambiguous_same_package_type"]


def test_type_declared_in_the_same_file_gives_no_edge():
    usage = {"kind": "same_package_type", "name": "User", "line": 3}
    models = node("store/models.go", [user_type("store/models.go", 3)], [usage])
    edges, unresolved = resolve_go_usages(models, build_go_catalog([models]))
    assert not edges and not unresolved


@pytest.mark.xfail(strict=True, reason="#547: same-package type use gives no edge")
def test_parser_records_same_package_types_only():
    pytest.importorskip("tree_sitter_language_pack")
    from unvibecode_graph.parse_ts import TreeSitterAstAdapter

    source = (
        'package store\n\nimport "example.com/shop/db"\n\n'
        "func Save(u User, name string, conn db.Conn) error {\n"
        "\tvar n int\n\t_ = n\n\treturn nil\n}\n"
    )
    usages = TreeSitterAstAdapter().parse("go", "s.go", Path("s.go"), source)["usages"]
    names = sorted(u["name"] for u in usages if u["kind"] == "same_package_type")
    assert names == ["User"]
