from pathlib import Path

import pytest

from unvibecode_graph.chunk import BoundaryChunker, FastContextTokenCounter


def method(index):
    body = "".join(f"        let v{k} = value + {k} * self.base;\n" for k in range(12))
    return (
        f"    /// Method {index}.\n"
        f"    pub fn method_{index}(&self, value: usize) -> usize {{\n"
        f"{body}        v0 + v11 + {index}\n    }}\n\n"
    )


SOURCE = (
    "pub struct HiArgs {\n    base: usize,\n}\n\nimpl HiArgs {\n"
    + "".join(method(i) for i in range(40))
    + "}\n"
)


def chunks(tmp_path):
    pytest.importorskip("tree_sitter_language_pack")
    from unvibecode_graph.parse_ts import TreeSitterAstAdapter

    (tmp_path / "lib.rs").write_text(SOURCE, encoding="utf-8", newline="")
    parsed = TreeSitterAstAdapter().parse("rust", "lib.rs", Path("lib.rs"), SOURCE)
    graph = {"nodes": [{"file": "lib.rs", "language": "rust", **parsed}]}
    return BoundaryChunker(tmp_path, graph, FastContextTokenCounter()).build()


def code(chunk):
    return "\n".join(line.split(" | ", 1)[1] for line in chunk.code.splitlines())


def test_large_impl_gives_one_chunk_per_method(tmp_path):
    methods = [c for c in chunks(tmp_path) if c.kind == "function"]
    assert [c.entity for c in methods] == [f"method_{i}" for i in range(40)]


def test_method_chunks_are_valid_rust_and_do_not_overlap(tmp_path):
    result = sorted(chunks(tmp_path), key=lambda c: c.start_line)
    parser = pytest.importorskip("tree_sitter_language_pack").get_parser("rust")
    for chunk in result:
        if chunk.kind == "function":
            assert not parser.parse(code(chunk).encode()).root_node.has_error
    assert all(a.end_line < b.start_line for a, b in zip(result, result[1:]))
    assert not [c for c in result if c.kind == "impl_segment"]
