"""Go calls must not also become file_import relationships (#498).

Go files in one package never import each other, so a call or method call
between them is a symbol relationship only. A real import still gives one
file_import relationship.
"""

import pytest

from unvibecode_graph.chunk import ChunkGraphBuilder, CodeChunk


def chunk(file, chunk_id):
    return CodeChunk(
        chunk_id=chunk_id,
        file=file,
        language="go",
        start_line=1,
        end_line=10,
        kind="whole_file",
        entity=None,
        qualified_name=None,
        parent_entity_id=None,
        tokens=10,
        code="",
        file_prelude="",
    )


def relationships(edges):
    chunks = [chunk("a.go", "chunk_a"), chunk("b.go", "chunk_b")]
    graph = {"edges": edges, "symbol_edges": [], "global_symbol_index": {}}
    return sorted(
        edge.relationship for edge in ChunkGraphBuilder(graph, chunks).build()
    )


@pytest.mark.xfail(strict=True, reason="#498: Go calls become phantom file_import")
@pytest.mark.parametrize("edge_type", ["calls_symbol", "method_call", "imports_symbol"])
def test_go_symbol_edge_is_not_a_file_import(edge_type):
    edge = {"source": "a.go", "target": "b.go", "type": edge_type, "line": 3}
    assert "file_import" not in relationships([edge])


def test_real_import_is_still_a_file_import():
    edge = {"source": "a.go", "target": "b.go", "type": "imports", "line": 3}
    assert relationships([edge]) == ["file_import"]
