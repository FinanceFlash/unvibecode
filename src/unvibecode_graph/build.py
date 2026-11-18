"""GraphBuilder: repository folder -> stage-one file graph (in memory).

Walks the repository (skipping IGNORE_DIRS and anything skip_dir rejects),
parses every known-language file, resolves imports to files and returns
    {"nodes": one per file, "edges": file -> file, "package_edges",
     "unresolved_imports", "unresolved_go_usages", "warnings", "summary", ...}
Files are processed in sorted path order, so the graph is deterministic."""
from __future__ import annotations

import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any
from collections.abc import Callable

from .config import IGNORE_DIRS, LANGUAGE_BY_EXTENSION, UNSUPPORTED_LANGUAGE_BY_EXTENSION
from .util import safe_read_text, to_posix_rel
from .parse_py import PythonAstAdapter
from .parse_ts import TREE_SITTER_BACKEND, TreeSitterAstAdapter
from .parse_web import CssAstAdapter, HtmlAstAdapter
from .resolve import ImportResolver
from .golinks import build_go_catalog, resolve_go_usages

TREE_SITTER_LANGUAGES = {"javascript", "jsx", "typescript", "tsx", "rust", "go", "php", "ruby"}
EDGE_KEY = ("source", "target", "type", "raw", "line", "symbol", "owner")
GO_UNRESOLVED_KEY = ("source", "line", "kind", "symbol", "receiver", "receiver_type", "owner", "reason")


def _dedupe(values: list[dict[str, Any]], fields: tuple[str, ...]) -> list[dict[str, Any]]:
    """Keep the first record for each combination of `fields`."""
    seen = set()
    out = []
    for value in values:
        key = tuple(value.get(field) for field in fields)
        if key not in seen:
            seen.add(key)
            out.append(value)
    return out


# -----------------------------------------------------------------------------
# Main builder
# -----------------------------------------------------------------------------
class GraphBuilder:
    """Stage one: parse source files and return the complete graph in memory."""

    def __init__(
        self,
        workspace_root: str,
        *,
        skip_dir: Callable[[Path], bool] | None = None,
        on_progress: Callable[..., None] | None = None,
    ) -> None:
        self.workspace_root = Path(workspace_root).resolve()
        self.skip_dir = skip_dir or (lambda _: False)  # extra folders to leave out
        self.on_progress = on_progress or (lambda *_: None)
        self.repo_name = self.workspace_root.name
        self.python_adapter = PythonAstAdapter()
        self.ts_adapter = TreeSitterAstAdapter()
        self.html_adapter = HtmlAstAdapter()
        self.css_adapter = CssAstAdapter()
        self.warnings: list[dict[str, Any]] = []

    def build(self) -> dict[str, Any]:
        if not self.workspace_root.is_dir():
            raise FileNotFoundError(f"Workspace not found: {self.workspace_root}")

        print(f"Scanning workspace: {self.workspace_root}")
        files = self._scan_files()
        self.on_progress("scan", 0, len(files))
        rel_files = [to_posix_rel(p.relative_to(self.workspace_root)) for p in files]
        resolver = ImportResolver(self.workspace_root, rel_files)

        print(f"Parsing source files: {len(files)}")
        nodes: list[dict[str, Any]] = []
        file_language_counts: dict[str, int] = defaultdict(int)
        for done, abs_file in enumerate(files, 1):
            language = self._detect_language(abs_file)
            file_language_counts[language] += 1
            source_text = safe_read_text(abs_file)
            self.on_progress("parse", done, len(files))
            nodes.append(self._file_node(abs_file, language, source_text, resolver))

        edges, package_edges, unresolved_imports, unresolved_go_usages = self._connect(nodes)
        symbol_edges = sum(1 for edge in edges if edge.get("type") in {"imports_symbol", "calls_symbol", "method_call"})
        graph = {
            "schema_version": "shipreadyv2.deep_graph.v1",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "workspace_root": str(self.workspace_root),
            "repo_name": self.repo_name,
            "tree_sitter_backend": TREE_SITTER_BACKEND,
            "summary": {
                "files_scanned": len(nodes),
                "edges": len(edges),
                "package_edges": len(package_edges),
                "unresolved_or_external_imports": len(unresolved_imports),
                "unresolved_go_usages": len(unresolved_go_usages),
                "go_symbol_edges": symbol_edges,
                "language_counts": dict(sorted(file_language_counts.items())),
                "nodes_with_parse_errors": sum(1 for n in nodes if n.get("parse_errors")),
                "nodes_without_ast_parser": sum(1 for n in nodes if n.get("parser_confidence") in {"none", "low"}),
            },
            "nodes": nodes,
            "edges": edges,
            "package_edges": package_edges,
            "unresolved_imports": unresolved_imports,
            "unresolved_go_usages": unresolved_go_usages,
            "warnings": self.warnings,
        }
        print(
            "[STAGE 1 COMPLETE] "
            f"{len(nodes):,} files, {len(edges):,} internal file edges, "
            f"{len(package_edges):,} package-level edges, "
            f"{len(unresolved_imports):,} unresolved/external imports, "
            f"{symbol_edges:,} symbol edges, "
            f"{len(unresolved_go_usages):,} unresolved Go usages"
        )
        self.on_progress("graph", len(files), len(files))
        return graph

    def _parse(self, language: str, rel_file: str, abs_file: Path, source_text: str) -> tuple[dict[str, Any], str, str]:
        """-> (extracted, parser_used, parser_confidence) from the adapter for this language."""
        if language == "python":
            extracted = self.python_adapter.parse(rel_file, abs_file, source_text)
            return extracted, self.python_adapter.parser_name, self.python_adapter.confidence
        if language in TREE_SITTER_LANGUAGES:
            extracted = self.ts_adapter.parse(language, rel_file, abs_file, source_text)
            return extracted, extracted.pop("parser_used", "tree_sitter"), extracted.pop("parser_confidence", "high")
        if language == "html":
            extracted = self.html_adapter.parse(rel_file, abs_file, source_text)
            return extracted, self.html_adapter.parser_name, self.html_adapter.confidence
        if language == "css":
            extracted = self.css_adapter.parse(rel_file, abs_file, source_text)
            return extracted, extracted.pop("parser_used", "css_parser"), extracted.pop("parser_confidence", "medium")
        message = f"Unsupported language detected: {language}. This language is not supported in this graph builder yet."
        return {"imports": [], "entities": [], "role_hints": [], "parse_errors": [message]}, "unsupported", "none"

    def _file_node(self, abs_file: Path, language: str, source_text: str, resolver: ImportResolver) -> dict[str, Any]:
        rel_file = to_posix_rel(abs_file.relative_to(self.workspace_root))
        extracted, parser_used, parser_confidence = self._parse(language, rel_file, abs_file, source_text)
        imports = [resolver.resolve(rel_file, language, imp) for imp in extracted.get("imports", [])]
        is_go = language == "go"
        return {
            "file": rel_file,
            "absolute_path": str(abs_file),
            "language": language,
            "extension": abs_file.suffix.lower(),
            "parser_used": parser_used,
            "parser_confidence": parser_confidence,
            "size_bytes": abs_file.stat().st_size,
            "line_count": source_text.count("\n") + 1 if source_text else 0,
            "role_hints": sorted(set(extracted.get("role_hints", []))),
            "entities": extracted.get("entities", []),
            "imports": imports,
            "go_usages": extracted.get("usages", []) if is_go else [],
            "go_shadow_names": extracted.get("shadow_names", []) if is_go else [],
            "imported_by": [],  # filled by _connect
            "parse_errors": extracted.get("parse_errors", []),
            "unresolved_import_count": sum(1 for imp in imports if not imp.get("internal")),
        }

    def _connect(self, nodes: list[dict[str, Any]]):
        """Nodes -> (file edges, Go package edges, unresolved imports, unresolved Go usages).
        Per file: its import edges first, then its Go symbol edges."""
        node_by_file = {n["file"]: n for n in nodes}
        go_catalog = build_go_catalog(nodes)
        edges: list[dict[str, Any]] = []
        package_edges: list[dict[str, Any]] = []
        unresolved_imports: list[dict[str, Any]] = []
        unresolved_go_usages: list[dict[str, Any]] = []
        for node in nodes:
            for imp in node.get("imports", []):
                if imp.get("internal") and imp.get("resolved_file") in node_by_file:
                    target = imp["resolved_file"]
                    edges.append(
                        {
                            "source": node["file"],
                            "target": target,
                            "type": "imports",
                            "raw": imp.get("raw"),
                            "import_style": imp.get("import_style"),
                            "line": imp.get("line"),
                            "confidence": imp.get("resolution_confidence", "medium"),
                            "resolution_strategy": imp.get("resolution_strategy"),
                        }
                    )
                    node_by_file[target].setdefault("imported_by", []).append(node["file"])
                elif imp.get("internal") and imp.get("resolution_kind") == "package" and imp.get("resolved_package") is not None:
                    package_edges.append(
                        {
                            "source": node["file"],
                            "target": imp["resolved_package"],
                            "type": "imports_package",
                            "raw": imp.get("raw"),
                            "module": imp.get("module"),
                            "import_style": imp.get("import_style"),
                            "alias": imp.get("alias"),
                            "line": imp.get("line"),
                            "confidence": imp.get("resolution_confidence", "medium"),
                            "resolution_strategy": imp.get("resolution_strategy"),
                            "package_files": imp.get("package_files", []),
                        }
                    )
                else:  # external or unresolved: kept, never dropped
                    unresolved_imports.append(
                        {
                            "source": node["file"],
                            "language": node["language"],
                            "raw": imp.get("raw"),
                            "module": imp.get("module"),
                            "import_style": imp.get("import_style"),
                            "line": imp.get("line"),
                            "reason": "external_or_unresolved",
                        }
                    )
            if node.get("language") == "go" and node.get("go_usages"):
                go_edges, go_unresolved = resolve_go_usages(node, go_catalog)
                edges.extend(_dedupe(go_edges, EDGE_KEY))
                unresolved_go_usages.extend(go_unresolved)

        for n in nodes:
            n["imported_by"] = sorted(set(n.get("imported_by", [])))
        return (
            _dedupe(edges, EDGE_KEY),
            _dedupe(package_edges, EDGE_KEY),
            unresolved_imports,
            _dedupe(unresolved_go_usages, GO_UNRESOLVED_KEY),
        )

    def _scan_files(self) -> list[Path]:
        files: list[Path] = []
        for root, dirs, filenames in os.walk(self.workspace_root):
            dirs[:] = [d for d in dirs if d.lower() not in IGNORE_DIRS and not self.skip_dir(Path(root) / d)]
            for filename in filenames:
                path = Path(root) / filename
                ext = path.suffix.lower()
                if ext in LANGUAGE_BY_EXTENSION or ext in UNSUPPORTED_LANGUAGE_BY_EXTENSION:
                    files.append(path)
        return sorted(files)

    def _detect_language(self, path: Path) -> str:
        ext = path.suffix.lower()
        if ext in LANGUAGE_BY_EXTENSION:
            return LANGUAGE_BY_EXTENSION[ext]
        if ext in UNSUPPORTED_LANGUAGE_BY_EXTENSION:
            return UNSUPPORTED_LANGUAGE_BY_EXTENSION[ext]
        return "unknown"
