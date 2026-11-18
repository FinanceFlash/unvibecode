"""Python source -> imports, entities and role hints, using the stdlib ast module.

PythonAstAdapter.parse(rel_file, abs_file, source) returns
    {"imports": [...], "entities": [...], "role_hints": [...], "parse_errors": [...]}
A SyntaxError never raises: it comes back as one parse_errors entry."""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from .util import line_range_from_ast_node


# -----------------------------------------------------------------------------
# Python AST adapter
# -----------------------------------------------------------------------------
class PythonAstAdapter:
    parser_name = "python_ast"
    confidence = "high"

    def parse(self, rel_file: str, abs_file: Path, source_text: str) -> dict[str, Any]:
        imports: list[dict[str, Any]] = []
        entities: list[dict[str, Any]] = []
        role_hints: list[str] = []
        parse_errors: list[str] = []

        try:
            tree = ast.parse(source_text)
        except SyntaxError as exc:
            return {
                "imports": [],
                "entities": [],
                "role_hints": [],
                "parse_errors": [f"SyntaxError: {exc}"],
            }

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(
                        {
                            "raw": alias.name,
                            "module": alias.name,
                            "symbols": [],
                            "import_style": "import",
                            "relative_level": 0,
                            "line": getattr(node, "lineno", None),
                        }
                    )

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                raw = "." * int(node.level or 0) + module
                imports.append(
                    {
                        "raw": raw,
                        "module": module,
                        "symbols": [alias.name for alias in node.names],
                        "import_style": "from_import",
                        "relative_level": int(node.level or 0),
                        "line": getattr(node, "lineno", None),
                    }
                )

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                decorators = [self._decorator_name(d) for d in getattr(node, "decorator_list", [])]
                decorators = [d for d in decorators if d]
                kind = "async_function" if isinstance(node, ast.AsyncFunctionDef) else "function"
                route_hint = self._route_hint_from_decorators(decorators)
                if route_hint:
                    kind = "route_handler"
                    role_hints.append(route_hint)

                entities.append(
                    {
                        "name": node.name,
                        "kind": kind,
                        "line_range": line_range_from_ast_node(node),
                        "decorators": decorators,
                        "exported": not node.name.startswith("_"),
                    }
                )

            elif isinstance(node, ast.ClassDef):
                decorators = [self._decorator_name(d) for d in getattr(node, "decorator_list", [])]
                decorators = [d for d in decorators if d]
                bases = [self._expr_name(b) for b in getattr(node, "bases", [])]
                bases = [b for b in bases if b]
                entities.append(
                    {
                        "name": node.name,
                        "kind": "class",
                        "line_range": line_range_from_ast_node(node),
                        "decorators": decorators,
                        "bases": bases,
                        "exported": not node.name.startswith("_"),
                    }
                )

        role_hints.extend(self._path_role_hints(rel_file))
        return {
            "imports": imports,
            "entities": entities,
            "role_hints": sorted(set(role_hints)),
            "parse_errors": parse_errors,
        }

    def _decorator_name(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            base = self._decorator_name(node.value)
            return f"{base}.{node.attr}" if base else node.attr
        if isinstance(node, ast.Call):
            return self._decorator_name(node.func)
        return None

    def _expr_name(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            base = self._expr_name(node.value)
            return f"{base}.{node.attr}" if base else node.attr
        if isinstance(node, ast.Subscript):
            return self._expr_name(node.value)
        return None

    def _route_hint_from_decorators(self, decorators: list[str]) -> str | None:
        route_tokens = ("route", "get", "post", "put", "patch", "delete", "websocket")
        for dec in decorators:
            lower = dec.lower()
            if any(lower.endswith(f".{tok}") or lower == tok for tok in route_tokens):
                return "api_route"
        return None

    def _path_role_hints(self, rel_file: str) -> list[str]:
        p = rel_file.lower().replace("\\", "/")
        hints = []
        if any(part in p for part in ["route", "routes", "views", "controller", "api/"]):
            hints.append("api_or_controller_file")
        if any(part in p for part in ["model", "models", "schema"]):
            hints.append("data_model_file")
        if any(part in p for part in ["service", "services"]):
            hints.append("service_file")
        if any(part in p for part in ["auth", "login", "jwt", "session"]):
            hints.append("auth_related_file")
        if any(part in p for part in ["payment", "billing", "invoice", "order"]):
            hints.append("transaction_related_file")
        return hints
