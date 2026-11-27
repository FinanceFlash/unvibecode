from pathlib import Path

import pytest

from unvibecode_graph.golinks import build_go_catalog, resolve_go_usages

MODELS = (
    "package shop\n\ntype ID string\n\n"
    "func (i ID) Key() string { return string(i) }\n\n"
    "type User struct{}\n\nfunc (u *User) Save() error { return nil }\n\n"
    "func ListUsers() []*User { return nil }\n\n"
    "type Routes map[string][]User\n\nfunc (r Routes) Save() error { return nil }\n"
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


def method_links(main_source):
    models = parse("models.go", MODELS)
    main = parse("main.go", main_source)
    edges, _ = resolve_go_usages(main, build_go_catalog([models, main]))
    return sorted(
        (e["target"], e["symbol"]) for e in edges if e["type"] == "method_call"
    )


def test_collection_return_types_name_the_element():
    source = (
        "package shop\n\ntype User struct{}\n\n"
        "func ListUsers() ([]*User, error) { return nil, nil }\n"
        "func UserMap() map[string]*User { return nil }\n"
        "func Fixed() [3]User { return [3]User{} }\n"
        "func Stream() chan *User { return nil }\n"
        "func One() *User { return nil }\n"
    )
    entities = parse("m.go", source)["entities"]
    returns = {e["name"]: e.get("returns") for e in entities if e["kind"] == "function"}
    assert returns == {
        "ListUsers": "User",
        "UserMap": "User",
        "Fixed": "User",
        "Stream": "User",
        "One": "User",
    }


def test_range_over_returned_slice_links_to_the_method():
    main = (
        "package shop\n\nfunc SaveAll() {\n"
        "\tfor _, u := range ListUsers() {\n\t\tu.Save()\n\t}\n}\n"
    )
    assert method_links(main) == [("models.go", "Save")]


def test_range_over_map_types_the_value_not_the_key():
    main = (
        "package shop\n\nfunc SaveAll(m map[ID]*User) {\n"
        "\tfor k, v := range m {\n\t\tk.Key()\n\t\tv.Save()\n\t}\n}\n"
    )
    assert method_links(main) == [("models.go", "Save")]


def test_range_over_named_map_type_does_not_reuse_the_map_type():
    main = (
        "package shop\n\nfunc SaveAll(r Routes) {\n"
        "\tfor _, users := range r {\n\t\tusers.Save()\n\t}\n}\n"
    )
    assert method_links(main) == []


def test_method_on_the_collection_itself_is_not_linked_to_the_item():
    main = (
        "package shop\n\nfunc SaveAll() {\n\tusers := ListUsers()\n\tusers.Save()\n}\n"
    )
    assert method_links(main) == []


def test_range_over_variadic_parameter_types_the_item():
    main = (
        "package shop\n\nfunc SaveAll(users ...*User) {\n"
        "\tfor _, u := range users {\n\t\tu.Save()\n\t}\n}\n"
    )
    assert method_links(main) == [("models.go", "Save")]
