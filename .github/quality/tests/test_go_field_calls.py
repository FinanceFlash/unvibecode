from pathlib import Path

import pytest

from unvibecode_graph.golinks import build_go_catalog, resolve_go_usages

STORE = (
    "package shop\n\ntype OrderStore struct{ rows map[string]int }\n\n"
    "func (s *OrderStore) Insert(id string) error { return nil }\n"
)
SERVICE = (
    'package shop\n\nimport "example.com/shop/db"\n\n'
    "type OrderService struct {\n\tstore *OrderStore\n\titems []*OrderStore\n"
    "\tconn *db.Conn\n}\n\n"
    "func (o *OrderService) Place(id string) error {\n\treturn o.store.Insert(id)\n}\n"
)


def parse(file, source):
    pytest.importorskip("tree_sitter_language_pack")
    from unvibecode_graph.parse_ts import TreeSitterAstAdapter

    extracted = TreeSitterAstAdapter().parse("go", file, Path(file), source)
    return {
        "file": file,
        "language": "go",
        "entities": extracted["entities"],
        "imports": [],
        "go_usages": extracted["usages"],
    }


def resolve(file, source):
    nodes = [parse("store.go", STORE), parse("service.go", SERVICE)]
    if file != "service.go":
        nodes.append(parse(file, source))
    node = next(n for n in nodes if n["file"] == file)
    edges, unresolved = resolve_go_usages(node, build_go_catalog(nodes))
    links = sorted(
        (e["target"], e["symbol"]) for e in edges if e["type"] == "method_call"
    )
    return links, [(u["symbol"], u["reason"]) for u in unresolved]


@pytest.mark.xfail(strict=True, reason="#831: calls through a struct field are dropped")
def test_call_through_a_field_links_to_the_method():
    assert resolve("service.go", SERVICE)[0] == [("store.go", "Insert")]


@pytest.mark.xfail(strict=True, reason="#831: calls through a struct field are dropped")
def test_call_through_two_fields_links_to_the_method():
    handler = (
        "package shop\n\ntype Handler struct {\n\tsvc *OrderService\n}\n\n"
        'func (h *Handler) Run() error {\n\treturn h.svc.store.Insert("a")\n}\n'
    )
    assert resolve("handler.go", handler)[0] == [("store.go", "Insert")]


@pytest.mark.xfail(strict=True, reason="#831: calls through a struct field are dropped")
def test_call_on_an_indexed_item_links_to_the_method():
    batch = (
        "package shop\n\nfunc Run(list []*OrderStore, byID map[string]*OrderStore, "
        'o *OrderService) {\n\tlist[0].Insert("a")\n\tbyID["x"].Insert("b")\n'
        '\to.items[1].Insert("c")\n}\n'
    )
    links = resolve("batch.go", batch)[0]
    assert links == [("store.go", "Insert")] * 3


@pytest.mark.xfail(strict=True, reason="#831: calls through a struct field are dropped")
def test_field_from_another_package_is_listed_as_unresolved():
    other = (
        "package shop\n\nfunc (s *OrderStore) Close() error { return nil }\n\n"
        "func Shut(o *OrderService) error {\n\treturn o.conn.Close()\n}\n"
    )
    links, unresolved = resolve("other.go", other)
    assert links == []
    assert ("Close", "cross_package_field_type") in unresolved


def test_package_selector_chain_is_not_a_method_call():
    source = "package shop\n\nfunc Run() {\n\thttp.DefaultClient.Do(nil)\n}\n"
    usages = parse("run.go", source)["go_usages"]
    assert [u for u in usages if u["kind"] == "method_call"] == []
