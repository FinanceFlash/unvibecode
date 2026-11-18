"""Small helpers shared by every parser: POSIX paths, safe file reads and
tree-sitter node access (text, line ranges, children, depth-first walk)."""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Any
from collections.abc import Iterable


# -----------------------------------------------------------------------------
# Utility helpers
# -----------------------------------------------------------------------------
def to_posix_rel(path: str | Path) -> str:
    return str(path).replace("\\", "/")


def safe_read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def clean_string_literal(text: str) -> str:
    text = text.strip()
    if len(text) >= 2 and text[0] in {"'", '"', "`"} and text[-1] == text[0]:
        return text[1:-1]
    return text.strip("'\"`")


def node_text(node: Any, source_bytes: bytes) -> str:
    return source_bytes[node.start_byte : node.end_byte].decode("utf-8", errors="ignore")


def line_range_from_ast_node(node: ast.AST) -> dict[str, int | None]:
    return {
        "start_line": getattr(node, "lineno", None),
        "end_line": getattr(node, "end_lineno", getattr(node, "lineno", None)),
    }


def line_range_from_ts_node(node: Any) -> dict[str, int]:
    return {
        "start_line": int(node.start_point[0]) + 1,
        "end_line": int(node.end_point[0]) + 1,
    }


def walk_ts(node: Any) -> Iterable[Any]:
    yield node
    for child in getattr(node, "children", []) or []:
        yield from walk_ts(child)


def named_children(node: Any) -> list[Any]:
    return list(getattr(node, "named_children", []) or [])


def child_by_field_name(node: Any, field_name: str) -> Any | None:
    try:
        return node.child_by_field_name(field_name)
    except Exception:
        return None


def _posix(value: Any) -> str:
    return str(value or "").replace("\\", "/")
