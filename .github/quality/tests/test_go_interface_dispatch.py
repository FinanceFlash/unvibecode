import json
import zipfile

import pytest

from unvibecode_graph.context import ContextBuilder
from unvibecode_graph.golinks import build_go_catalog, resolve_go_usages


def node(file, entities, usages=()):
    package = {"kind": "package", "name": "greet", "scope": "package"}
    return {
        "file": file,
        "language": "go",
        "entities": [package, *entities],
        "imports": [],
        "go_usages": list(usages),
    }


def entity(kind, name, line, owner=None):
    item = {
        "kind": kind,
        "name": name,
        "exported": True,
        "scope": "package",
        "line_range": {"start_line": line},
    }
    if owner:
        item["owner"] = owner
    return item


@pytest.mark.xfail(strict=True, reason="#573: interface dispatch is silently dropped")
def test_interface_call_is_listed_as_unresolved():
    usage = {
        "kind": "method_call",
        "receiver": "g",
        "receiver_type": {"kind": "named", "name": "Greeter", "qualifier": None},
        "symbol": "Greet",
        "line": 8,
    }
    service = node("service.go", [entity("interface", "Greeter", 3)], [usage])
    english = node(
        "english.go",
        [entity("struct", "English", 3), entity("method", "Greet", 5, "English")],
    )
    edges, unresolved = resolve_go_usages(service, build_go_catalog([service, english]))
    assert edges == []
    assert [
        (u["source"], u["line"], u["receiver"], u["symbol"], u["reason"])
        for u in unresolved
    ] == [("service.go", 8, "g", "Greet", "interface_dispatch")]
    assert unresolved[0]["candidates"] == [
        {"file": "english.go", "line": 5, "owner": "English"}
    ]


@pytest.mark.xfail(strict=True, reason="#573: Go unresolved usages are not exported")
def test_go_unresolved_usages_reach_the_context_bundle(tmp_path):
    row = {"source": "service.go", "line": 8, "symbol": "Greet"}
    row["reason"] = "interface_dispatch"
    graph = {"repo_name": "greet", "unresolved_go_usages": [row]}
    bundle = tmp_path / "context.zip"
    ContextBuilder(tmp_path, graph)._write_repository_bundle(
        bundle, file_records={}, relationships=[], skipped_files=[]
    )
    with zipfile.ZipFile(bundle) as archive:
        lines = archive.read("unresolved_relationships.jsonl").decode().splitlines()
    assert [json.loads(line) for line in lines] == [row]
