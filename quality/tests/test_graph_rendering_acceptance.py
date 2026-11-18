"""Presentation-only graph regressions; no hosted model calls."""

import copy
import pytest
from unvibecode_graph import render as graph_render


from graph_test_helpers import Network


@pytest.fixture(scope="module")
def module():
    return graph_render


def render(module, tmp_path, files, symbols=(), edges=()):
    graph = {
        "nodes": [{"file": f, "language": "python"} for f in files],
        "symbol_edges": list(symbols),
        "edges": list(edges),
    }
    before = copy.deepcopy(graph)
    result = module._render_symbol_graph(
        Network, graph, tmp_path / "map.html", context_store_filename="context.js"
    )
    assert graph == before
    return Network.last, result


def link(a, b, **kwargs):
    return dict(source=a, target=b, confidence="high", **kwargs)


@pytest.mark.parametrize(
    "files",
    [
        [],
        ["a.py"],
        ["a.py", "b.py"],
        [".github/a.py", "x/a.py", "y/a.py", "项目.py", "A.py"],
    ],
)
def test_complete_inventory(module, tmp_path, files):
    net, result = render(module, tmp_path, files)
    assert {n["id"] for n in net.nodes} == set(files)
    assert len(net.nodes) == len(files) and not net.edges
    assert result["rendered_file_nodes"] == len(files)


def test_symbols_do_not_suppress_other_file_imports(module, tmp_path):
    net, _ = render(
        module,
        tmp_path,
        ["a", "b", "c", "isolated"],
        [link("a", "b", symbol="foo", line=1)],
        [link("b", "c", line=2)],
    )
    assert len(net.nodes) == 5
    assert any(e["from_"] == "b" and e["to"] == "c" for e in net.edges)
    assert not any(e["from_"] == "a" and e["to"] == "c" for e in net.edges)
    assert not any(e["from_"] == "isolated" or e["to"] == "isolated" for e in net.edges)


@pytest.mark.parametrize(
    "metadata,expected",
    [
        ({"confidence": "high"}, False),
        ({"confidence": "medium"}, True),
        ({"confidence": "low"}, True),
        ({}, True),
        ({"confidence": "high", "is_uncertain": True}, True),
        ({"confidence": "high", "uncertain": True}, True),
        ({"confidence": "high", "resolution_status": "ambiguous"}, True),
        ({"confidence": "high", "status": "unresolved"}, True),
    ],
)
def test_certainty_mapping(module, metadata, expected):
    assert module._is_uncertain(metadata) is expected


def test_shared_symbols_do_not_promote_uncertainty(module, tmp_path):
    net, _ = render(
        module,
        tmp_path,
        ["a", "b", "target"],
        [
            link("a", "target", symbol="foo"),
            link("b", "target", symbol="foo", uncertain=True),
        ],
    )
    symbols = [n for n in net.nodes if n["shape"] == "diamond"]
    assert len(symbols) == 2
    for source, uncertain in [("a", False), ("b", True)]:
        first = next(e for e in net.edges if e["from_"] == source)
        second = next(e for e in net.edges if e["from_"] == first["to"])
        assert first["dashes"] == second["dashes"] == uncertain


def test_visual_duplicates_keep_records_and_separate_symbols(module, tmp_path):
    e = link("a", "b", symbol="foo", line=4)
    net, _ = render(
        module,
        tmp_path,
        ["a", "b"],
        [e, e, link("a", "b", symbol="bar", line=4)],
        [link("a", "b", line=4)],
    )
    assert len(net.edges) == 4
    assert len(net.shipready_presentation["file_imports_represented_by_symbols"]) == 1
    assert max(len(e["relationship_records"]) for e in net.edges) == 2


def test_cycles_self_links_and_absent_targets(module, tmp_path):
    net, _ = render(
        module,
        tmp_path,
        ["a", "b"],
        edges=[link("a", "b"), link("b", "a"), link("a", "a"), link("a", "missing")],
    )
    assert {(e["from_"], e["to"]) for e in net.edges} == {
        ("a", "b"),
        ("b", "a"),
        ("a", "a"),
    }


def test_above_historical_caps(module, tmp_path):
    files = [f"dir/f{i}.py" for i in range(801)]
    symbols = [
        link(files[i % 801], files[(i + 1) % 801], symbol=f"s{i}") for i in range(1001)
    ]
    edges = [link(files[i % 801], files[(i + 2) % 801], line=i) for i in range(1601)]
    net, result = render(module, tmp_path, files, symbols, edges)
    assert (
        result["rendered_file_nodes"] == 801 and result["rendered_symbol_edges"] == 1001
    )
    assert result["complete_file_edges"] == 1601
    assert sum(len(e["relationship_records"]) for e in net.edges) == 2 * 1001 + 1601
    assert net.options["physics"]["enabled"] is False
    assert all("x" in n and "y" in n for n in net.nodes)


def test_search_and_small_legend_without_confidence_panels(module, tmp_path):
    render(module, tmp_path, ["a.py"])
    text = (tmp_path / "map.html").read_text(encoding="utf-8")
    assert "uvc-file-search" in text and "uvc-file-results" in text
    assert "Solid: established · Dotted: uncertain" in text
    assert "Confidence:" not in text
    assert "(~45K tokens)" not in text
    assert "No downloadable context is available for this file." in text
    assert "No indexed files to display" in text
    assert "Context downloads could not load." in text


def test_embedded_inventory_escapes_script_text(module, tmp_path):
    render(module, tmp_path, ["x</script><script>alert(1)</script>.py"])
    text = (tmp_path / "map.html").read_text(encoding="utf-8")
    assert "x</script><script>alert(1)" not in text
    assert "\\u003c/script>" in text


def test_large_graph_with_real_pyvis(module, tmp_path):
    # Real PyVis changes options from an Options object to a dict after the
    # first set_options call; a fake network cannot catch a second-call crash.
    pyvis = pytest.importorskip("pyvis.network", reason="requires graph dependencies")

    graph = {
        "nodes": [{"file": f"file_{i}.py"} for i in range(401)],
        "edges": [],
        "symbol_edges": [],
    }
    out = tmp_path / "map.html"
    result = module._render_symbol_graph(
        pyvis.Network, graph, out, context_store_filename="context.js"
    )
    assert result["rendered_file_nodes"] == 401
    assert '"static_layout": true' in out.read_text(encoding="utf-8")
