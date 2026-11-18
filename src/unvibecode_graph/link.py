"""Stage two: stage-one graph -> resolved symbol graph (shipreadyv2_resolved_graph.json).

Linker connects an import or call in one file to the definition it uses in
another, adding symbol_edges, linker_resolution, global_symbol_index and
unresolved_linker_imports. It links only what the source proves (exact
importable names); guessing by a bare name elsewhere in the repository is
off unless allow_global_symbol_fallback=True."""
from __future__ import annotations

import ast
import copy
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any
from collections.abc import Iterable, Mapping, Sequence

from .util import _posix


# -----------------------------------------------------------------------------
# Stage two: safe linker resolution
# -----------------------------------------------------------------------------
DEFAULT_OUTPUT_NAME = "shipreadyv2_resolved_graph.json"
SCHEMA_VERSION = "shipreadyv2.resolved_graph.v1"


def _canonical_symbol(value: Any) -> str:
    """Return an exact, conservative symbol key.

    No case folding is performed because most supported languages are case
    sensitive. Import aliases are intentionally not guessed.
    """

    return str(value or "").strip()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _json_key(value: Mapping[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


@dataclass(frozen=True)
class SymbolDefinition:
    name: str
    source_file: str
    kind: str | None
    start_line: int | None
    end_line: int | None
    exported: bool | None
    qualified_name: str | None = None
    owner: str | None = None
    scope: str | None = None
    importable: bool | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_file": self.source_file,
            "kind": self.kind,
            "line_range": {
                "start_line": self.start_line,
                "end_line": self.end_line,
            },
            "exported": self.exported,
            "qualified_name": self.qualified_name,
            "owner": self.owner,
            "scope": self.scope,
            "importable": self.importable,
        }


class _ImportContextVisitor(ast.NodeVisitor):
    """Records, for each import line, why it may not always run (inside if/try/loop/def,
    TYPE_CHECKING, wildcard), and collects importlib/__import__ calls as dynamic imports."""

    def __init__(self, extractor: "PythonSemanticExtractor") -> None:
        self.extractor = extractor
        self.context: list[str] = []
        self.scope_depth = 0

    def _mark(self, node: ast.AST, extra: str | None = None) -> None:
        line = int(getattr(node, "lineno", 0) or 0)
        if not line:
            return
        self.extractor.import_uncertainty_by_line[line].update(self.context)
        if self.scope_depth:
            self.extractor.import_uncertainty_by_line[line].add("non_module_scope_import")
        if extra:
            self.extractor.import_uncertainty_by_line[line].add(extra)

    def visit_Import(self, node: ast.Import) -> None:
        self._mark(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        wildcard = any(alias.name == "*" for alias in node.names)
        self._mark(node, "wildcard_import" if wildcard else None)

    def visit_Call(self, node: ast.Call) -> None:
        func_name = PythonSemanticExtractor._expression_name(node.func)
        if func_name in {"importlib.import_module", "__import__"}:
            raw, expression = self._dynamic_target(node)
            reasons = set(self.context)
            reasons.add("dynamic_import")
            if self.scope_depth:
                reasons.add("non_module_scope_import")
            self.extractor.dynamic_imports.append(
                {
                    "raw": raw or expression,
                    "module": raw or "",
                    "symbols": [],
                    "import_style": "dynamic_import",
                    "line": getattr(node, "lineno", None),
                    "is_uncertain": True,
                    "uncertainty_reasons": sorted(reasons),
                    "resolution_eligible": False,
                    "dynamic_expression": expression if not raw else None,
                }
            )
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        reason = "type_checking_only" if self._is_type_checking(node.test) else "conditional_import"
        self.context.append(reason)
        for item in [*node.body, *node.orelse]:
            self.visit(item)
        self.context.pop()

    def visit_Try(self, node: ast.Try) -> None:
        self.context.append("try_import_fallback")
        for item in [*node.body, *node.handlers, *node.orelse, *node.finalbody]:
            self.visit(item)
        self.context.pop()

    def visit_For(self, node: ast.For | ast.AsyncFor | ast.While) -> None:
        self.context.append("conditional_import")
        for item in [*node.body, *node.orelse]:
            self.visit(item)
        self.context.pop()

    visit_AsyncFor = visit_While = visit_For

    def visit_Match(self, node: ast.Match) -> None:
        self.context.append("conditional_import")
        for case in node.cases:
            for item in case.body:
                self.visit(item)
        self.context.pop()

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        for item in node.body:
            self.visit(item)

    def visit_FunctionDef(self, node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> None:
        self.scope_depth += 1
        for item in node.body:
            self.visit(item)
        self.scope_depth -= 1

    visit_AsyncFunctionDef = visit_ClassDef = visit_FunctionDef

    def _dynamic_target(self, node: ast.Call) -> tuple[str | None, str]:
        if not node.args:
            return None, "<missing_argument>"
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            return first.value, first.value
        try:
            return None, ast.unparse(first)
        except Exception:
            return None, "<dynamic_expression>"

    def _is_type_checking(self, test: ast.AST) -> bool:
        name = PythonSemanticExtractor._expression_name(test)
        return name in {"TYPE_CHECKING", "typing.TYPE_CHECKING"}


class PythonSemanticExtractor:
    """Extract import-safe Python entities and import uncertainty metadata."""

    def __init__(self) -> None:
        self.entities: list[dict[str, Any]] = []
        self.import_uncertainty_by_line: defaultdict[int, set[str]] = defaultdict(set)
        self.dynamic_imports: list[dict[str, Any]] = []

    def extract(self, source_text: str) -> dict[str, Any]:
        tree = ast.parse(source_text)
        self._walk_body(tree.body, owners=[], parent_scope="module")
        self._scan_imports(tree)
        return {
            "entities": self.entities,
            "import_uncertainty_by_line": {
                line: sorted(reasons) for line, reasons in self.import_uncertainty_by_line.items()
            },
            "dynamic_imports": self.dynamic_imports,
        }

    def _walk_body(self, body: Sequence[ast.stmt], owners: list[str], parent_scope: str) -> None:
        for statement in body:
            if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if parent_scope == "module":
                    kind = "async_function" if isinstance(statement, ast.AsyncFunctionDef) else "function"
                    scope = "module"
                    importable = True
                elif parent_scope == "class":
                    kind = "method"
                    scope = "class"
                    importable = False
                else:
                    kind = "nested_function"
                    scope = "function"
                    importable = False
                self.entities.append(
                    self._entity(
                        statement,
                        name=statement.name,
                        kind=kind,
                        owners=owners,
                        scope=scope,
                        importable=importable,
                    )
                )
                self._walk_body(statement.body, owners=owners + [statement.name], parent_scope="function")
                continue

            if isinstance(statement, ast.ClassDef):
                scope = "module" if parent_scope == "module" else parent_scope
                importable = parent_scope == "module"
                kind = "class" if importable else "nested_class"
                entity = self._entity(
                    statement,
                    name=statement.name,
                    kind=kind,
                    owners=owners,
                    scope=scope,
                    importable=importable,
                )
                entity["bases"] = [self._expression_name(base) for base in statement.bases]
                entity["bases"] = [base for base in entity["bases"] if base]
                self.entities.append(entity)
                self._walk_body(statement.body, owners=owners + [statement.name], parent_scope="class")
                continue

            if parent_scope == "module" and isinstance(statement, (ast.Assign, ast.AnnAssign)):
                self.entities.extend(self._safe_constants(statement))

            # Definitions inside control-flow blocks remain module-owned when the
            # block itself is at module level, but they are conditionally defined.
            child_bodies = self._statement_bodies(statement)
            for child_body in child_bodies:
                self._walk_body(child_body, owners=owners, parent_scope=parent_scope)

    def _entity(
        self,
        node: ast.AST,
        *,
        name: str,
        kind: str,
        owners: Sequence[str],
        scope: str,
        importable: bool,
    ) -> dict[str, Any]:
        qualified_name = ".".join([*owners, name]) if owners else name
        return {
            "name": name,
            "qualified_name": qualified_name,
            "owner": ".".join(owners) if owners else None,
            "kind": kind,
            "scope": scope,
            "importable": bool(importable),
            "exported": bool(importable and not name.startswith("_")),
            "line_range": {
                "start_line": getattr(node, "lineno", None),
                "end_line": getattr(node, "end_lineno", getattr(node, "lineno", None)),
            },
        }

    def _safe_constants(self, statement: ast.stmt) -> list[dict[str, Any]]:
        if isinstance(statement, ast.Assign):
            targets = [target for target in statement.targets if isinstance(target, ast.Name)]
            value = statement.value
        elif isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
            targets = [statement.target]
            value = statement.value
        else:
            return []
        if value is None:
            return []
        try:
            literal_value = ast.literal_eval(value)
        except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
            return []

        out: list[dict[str, Any]] = []
        for target in targets:
            name = target.id
            if not name.isidentifier() or not name.isupper() or name.startswith("_"):
                continue
            entity = self._entity(
                statement,
                name=name,
                kind="constant",
                owners=[],
                scope="module",
                importable=True,
            )
            entity["value_type"] = type(literal_value).__name__
            entity["literal_value_omitted"] = True
            out.append(entity)
        return out

    def _scan_imports(self, tree: ast.AST) -> None:
        _ImportContextVisitor(self).visit(tree)

    @staticmethod
    def _expression_name(node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            base = PythonSemanticExtractor._expression_name(node.value)
            return f"{base}.{node.attr}" if base else node.attr
        return None

    @staticmethod
    def _statement_bodies(statement: ast.stmt) -> list[Sequence[ast.stmt]]:
        bodies: list[Sequence[ast.stmt]] = []
        for field in ("body", "orelse", "finalbody"):
            value = getattr(statement, field, None)
            if isinstance(value, list):
                bodies.append(value)
        for handler in getattr(statement, "handlers", []) or []:
            bodies.append(getattr(handler, "body", []) or [])
        for case in getattr(statement, "cases", []) or []:
            bodies.append(getattr(case, "body", []) or [])
        return bodies


class Linker:
    """Stage two: resolve symbols from graph documents already held in memory."""

    def __init__(
        self,
        graph_paths: Sequence[Path] = (),
        *,
        graph_documents: Sequence[Mapping[str, Any]] | None = None,
        allow_global_symbol_fallback: bool = False,
        strict_hard_path: bool = False,
        deep_relative_parent_hops: int = 3,
        enrich_python: bool = True,
    ) -> None:
        if not graph_paths and not graph_documents:
            raise ValueError("At least one graph path or in-memory graph document is required.")
        self.graph_paths = [Path(p).resolve() for p in graph_paths]
        # Keep in-memory documents by shallow top-level reference. Individual
        # nodes are copied once during merge, avoiding several full-graph copies
        # for very large repositories.
        self.graph_documents = [dict(document) for document in graph_documents or ()]
        self.allow_global_symbol_fallback = bool(allow_global_symbol_fallback)
        self.strict_hard_path = bool(strict_hard_path)
        self.deep_relative_parent_hops = max(1, int(deep_relative_parent_hops))
        self.enrich_python = bool(enrich_python)

        self._documents: list[dict[str, Any]] = []
        self._nodes: list[dict[str, Any]] = []
        self._node_by_file: dict[str, dict[str, Any]] = {}
        self._symbol_index: defaultdict[str, list[SymbolDefinition]] = defaultdict(list)
        self._workspace_root: Path | None = None
        self._python_enrichment_summary: Counter[str] = Counter()
        self.resolved_document: dict[str, Any] | None = None

    def _link_node_imports(self, node, counters, symbol_edges, unresolved_log) -> list[dict[str, Any]]:
        """Resolve one node's imports; appends edges and unresolved records, counts outcomes."""
        source_file = _posix(node.get("file"))
        augmented_imports: list[dict[str, Any]] = []
        for import_object in node.get("imports", []) or []:
            counters["imports_total"] += 1
            augmented, edges, unresolved = self._resolve_import(source_file, import_object)
            augmented_imports.append(augmented)
            symbol_edges.extend(edges)
            counters[f"imports_{augmented['resolution_status']}"] += 1
            if augmented.get("is_uncertain"):
                counters["imports_with_uncertainty"] += 1
            resolutions = augmented.get("symbol_resolutions", [])
            counters["symbols_total"] += len(resolutions)
            counters["symbols_resolved"] += sum(1 for item in resolutions if item.get("resolved_path"))
            counters["symbols_unresolved"] += sum(1 for item in resolutions if not item.get("resolved_path"))
            if unresolved:
                unresolved_log.append(unresolved)
        return augmented_imports

    def _summary(self, result, counters, symbol_edges, go_symbol_edges) -> dict[str, Any]:
        ambiguous_symbol_names = sum(1 for definitions in self._symbol_index.values() if len(definitions) > 1)
        unique_symbol_names = sum(1 for definitions in self._symbol_index.values() if len(definitions) == 1)

        return {
            "source_graph_files": len(self.graph_paths) + len(self.graph_documents),
            "files_indexed": len(result.get("nodes", [])),
            "symbol_definitions": sum(len(v) for v in self._symbol_index.values()),
            "unique_symbol_names": unique_symbol_names,
            "ambiguous_symbol_names": ambiguous_symbol_names,
            "imports_total": counters["imports_total"],
            "imports_resolved": counters["imports_resolved"] + counters["imports_resolved_multi_target"],
            "imports_resolved_package": counters["imports_resolved_package"],
            "imports_partial": counters["imports_partial"],
            "imports_unresolved": counters["imports_unresolved"],
            "imports_hard_path_skipped": counters["imports_hard_path_skipped"],
            "imports_uncertain": counters["imports_uncertain"],
            "imports_with_uncertainty": counters["imports_with_uncertainty"],
            "symbols_total": counters["symbols_total"],
            "symbols_resolved": counters["symbols_resolved"],
            "symbols_unresolved": counters["symbols_unresolved"],
            "symbol_edges_added": len(symbol_edges),
            "go_symbol_edges_promoted": len(go_symbol_edges),
            "go_usages_unresolved": len(result.get("unresolved_go_usages", []) or []),
            "python_files_enriched": self._python_enrichment_summary["files_enriched"],
            "python_files_skipped": self._python_enrichment_summary["files_skipped"],
            "python_safe_constants_added": self._python_enrichment_summary["safe_constants"],
            "python_dynamic_imports_added": self._python_enrichment_summary["dynamic_imports"],
        }

    def resolve_to(self, output_path: Path) -> dict[str, Any]:
        output_path = Path(output_path).resolve()
        if output_path in self.graph_paths:
            raise ValueError("Output path must differ from every input graph path.")

        input_hashes_before = {str(path): _sha256(path) for path in self.graph_paths}
        in_memory_sources = [
            {
                "source": "in_memory_stage_1",
                "sha256": None,
                "integrity": "same_process_memory_handoff",
            }
            for document in self.graph_documents
        ]
        self._load_and_merge()
        if self.enrich_python:
            self._enrich_python_nodes()
        self._build_symbol_index()

        result = self._base_output_document()
        counters: Counter[str] = Counter()
        unresolved_log: list[dict[str, Any]] = []
        go_symbol_edges: list[dict[str, Any]] = [
            copy.deepcopy(dict(edge))
            for edge in result.get("edges", []) or []
            if isinstance(edge, Mapping)
            and edge.get("type") in {"imports_symbol", "calls_symbol", "method_call"}
            and edge.get("source")
            and edge.get("target")
        ]
        symbol_edges: list[dict[str, Any]] = list(go_symbol_edges)
        for node in result.get("nodes", []):
            node["imports"] = self._link_node_imports(node, counters, symbol_edges, unresolved_log)
        symbol_edges = self._dedupe_dicts(
            symbol_edges,
            fields=("source", "target", "type", "symbol", "line", "owner"),
        )
        summary = self._summary(result, counters, symbol_edges, go_symbol_edges)

        result["schema_version"] = SCHEMA_VERSION
        result["linker_resolution"] = {
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "source_graphs": [
                {"path": str(path), "sha256": input_hashes_before[str(path)]}
                for path in self.graph_paths
            ] + in_memory_sources,
            "policy": {
                "mode": "safe_exact_symbol_resolution",
                "hard_path_prefixes": ["@/", "~/"],
                "deep_relative_parent_hops": self.deep_relative_parent_hops,
                "strict_hard_path": self.strict_hard_path,
                "allow_global_symbol_fallback": self.allow_global_symbol_fallback,
                "existing_valid_resolved_file_precedence": not self.strict_hard_path,
                "ambiguous_symbol_policy": "skip_and_log",
                "python_index_policy": "module_scope_importable_classes_functions_and_safe_constants_only",
            },
            "summary": summary,
            "graph_artifacts": {"status": "not_emitted_json_only_pipeline"},
        }
        result["global_symbol_index"] = {
            name: [definition.as_dict() for definition in definitions]
            for name, definitions in sorted(self._symbol_index.items())
        }
        result["symbol_edges"] = symbol_edges
        result["unresolved_linker_imports"] = unresolved_log

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

        input_hashes_after = {str(path): _sha256(path) for path in self.graph_paths}
        if input_hashes_before != input_hashes_after:
            output_path.unlink(missing_ok=True)
            raise RuntimeError("Input integrity check failed: an input graph changed during resolution.")

        self.resolved_document = result
        self._print_summary(output_path, summary)
        return summary

    def _load_and_merge(self) -> None:
        documents: list[dict[str, Any]] = list(self.graph_documents)
        for index, document in enumerate(documents, start=1):
            if not isinstance(document.get("nodes"), list):
                raise ValueError(f"In-memory graph {index} must contain a top-level nodes list.")
        for path in self.graph_paths:
            if not path.is_file():
                raise FileNotFoundError(f"Graph JSON not found: {path}")
            with path.open("r", encoding="utf-8") as handle:
                document = json.load(handle)
            if not isinstance(document, dict):
                raise ValueError(f"Graph root must be a JSON object: {path}")
            if not isinstance(document.get("nodes"), list):
                raise ValueError(f"Graph must contain a top-level nodes list: {path}")
            documents.append(document)

        workspace_roots = {
            str(document.get("workspace_root"))
            for document in documents
            if document.get("workspace_root")
        }
        repo_names = {
            str(document.get("repo_name"))
            for document in documents
            if document.get("repo_name")
        }
        if len(workspace_roots) > 1 or (not workspace_roots and len(repo_names) > 1):
            raise ValueError(
                "Input graphs appear to belong to different repositories. "
                "Resolve each repository separately to avoid relative-path collisions."
            )
        if len(workspace_roots) == 1:
            candidate_root = Path(next(iter(workspace_roots))).expanduser()
            if candidate_root.is_dir():
                self._workspace_root = candidate_root.resolve()

        node_by_file: dict[str, dict[str, Any]] = {}
        for document in documents:
            for raw_node in document.get("nodes", []) or []:
                if not isinstance(raw_node, dict):
                    continue
                source_file = _posix(raw_node.get("file"))
                if not source_file:
                    continue
                candidate = copy.deepcopy(raw_node)
                if source_file not in node_by_file:
                    node_by_file[source_file] = candidate
                else:
                    node_by_file[source_file] = self._merge_nodes(node_by_file[source_file], candidate)

        self._documents = documents
        self._node_by_file = node_by_file
        self._nodes = [node_by_file[path] for path in sorted(node_by_file)]

    def _enrich_python_nodes(self) -> None:
        """Re-read every Python file with the semantic extractor: exact entities,
        why each import may not always run, and importlib/__import__ calls."""
        python_nodes = [node for node in self._nodes if str(node.get("language") or "").lower() == "python"]
        if self._workspace_root is None:
            self._python_enrichment_summary["workspace_unavailable"] += 1
            for node in python_nodes:
                self._skip_python_node(node, "workspace_root_unavailable")
            return
        for node in python_nodes:
            self._enrich_python_node(node)
        self._node_by_file = {
            _posix(node.get("file")): node for node in self._nodes if node.get("file")
        }

    def _skip_python_node(self, node: dict[str, Any], reason: str) -> None:
        self._python_enrichment_summary["files_skipped"] += 1
        node["python_semantic_enrichment"] = {"status": "skipped", "reason": reason}

    def _enrich_python_node(self, node: dict[str, Any]) -> None:
        assert self._workspace_root is not None
        relative_file = _posix(node.get("file"))
        if not relative_file:
            self._python_enrichment_summary["files_skipped"] += 1
            return
        source_path = (self._workspace_root / relative_file).resolve()
        try:
            source_path.relative_to(self._workspace_root)
        except ValueError:
            self._skip_python_node(node, "path_outside_workspace")
            return
        if not source_path.is_file():
            self._skip_python_node(node, "source_file_missing")
            return
        try:
            source_text = source_path.read_text(encoding="utf-8", errors="ignore")
            extracted = PythonSemanticExtractor().extract(source_text)
        except (OSError, SyntaxError) as exc:
            self._skip_python_node(node, f"{type(exc).__name__}: {exc}")
            return

        node["entities"] = self._merge_python_entities(node.get("entities", []) or [], extracted["entities"])
        node["imports"], dynamic_added = _merge_python_imports(node.get("imports", []) or [], extracted)
        uncertainty_by_line = extracted["import_uncertainty_by_line"]
        constants = sum(1 for entity in extracted["entities"] if entity.get("kind") == "constant")
        self._python_enrichment_summary["files_enriched"] += 1
        self._python_enrichment_summary["safe_constants"] += constants
        self._python_enrichment_summary["dynamic_imports"] += dynamic_added
        node["python_semantic_enrichment"] = {
            "status": "enriched",
            "source": "python_ast",
            "module_importable_entities": sum(1 for entity in extracted["entities"] if entity.get("importable")),
            "non_importable_owned_entities": sum(1 for entity in extracted["entities"] if not entity.get("importable")),
            "safe_constants": constants,
            "dynamic_imports_added": dynamic_added,
            "uncertain_import_lines": len(uncertainty_by_line),
        }

    def _merge_python_entities(
        self,
        original_entities: Sequence[dict[str, Any]],
        semantic_entities: Sequence[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        by_key: defaultdict[tuple[str, Any], list[dict[str, Any]]] = defaultdict(list)
        for entity in semantic_entities:
            line_range = entity.get("line_range") or {}
            by_key[(_canonical_symbol(entity.get("name")), line_range.get("start_line"))].append(entity)

        merged: list[dict[str, Any]] = []
        used_ids: set[int] = set()
        for original in original_entities:
            item = copy.deepcopy(original)
            line_range = item.get("line_range") or {}
            key = (_canonical_symbol(item.get("name") or item.get("entity_name")), line_range.get("start_line"))
            candidates = by_key.get(key, [])
            match = next((candidate for candidate in candidates if id(candidate) not in used_ids), None)
            if match is not None:
                item.update(copy.deepcopy(match))
                used_ids.add(id(match))
            else:
                item.update(
                    {
                        "qualified_name": item.get("qualified_name") or item.get("name"),
                        "owner": item.get("owner"),
                        "scope": item.get("scope") or "unconfirmed",
                        "importable": False,
                        "semantic_note": "not_confirmed_by_python_semantic_pass",
                    }
                )
            merged.append(item)
        for entity in semantic_entities:
            if id(entity) not in used_ids:
                merged.append(copy.deepcopy(entity))
        return self._dedupe_dicts(
            merged,
            fields=("qualified_name", "kind", "line_range"),
        )

    def _merge_nodes(self, left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
        merged = copy.deepcopy(left)
        merged["entities"] = self._dedupe_dicts(
            list(left.get("entities", []) or []) + list(right.get("entities", []) or []),
            fields=("name", "kind", "line_range"),
        )
        merged["imports"] = self._dedupe_dicts(
            list(left.get("imports", []) or []) + list(right.get("imports", []) or []),
            fields=("raw", "module", "import_style", "line", "symbols"),
        )
        merged["go_usages"] = self._dedupe_dicts(
            list(left.get("go_usages", []) or []) + list(right.get("go_usages", []) or []),
            fields=("kind", "qualifier", "name", "receiver", "receiver_type", "symbol", "context", "line"),
        )
        merged["go_shadow_names"] = sorted(
            set(left.get("go_shadow_names", []) or []) | set(right.get("go_shadow_names", []) or [])
        )
        merged["imported_by"] = sorted(
            {_posix(v) for v in (left.get("imported_by", []) or []) + (right.get("imported_by", []) or [])}
        )
        return merged

    def _base_output_document(self) -> dict[str, Any]:
        if len(self._documents) == 1:
            result = dict(self._documents[0])
            result["nodes"] = self._nodes
            return result

        edges: list[dict[str, Any]] = []
        package_edges: list[dict[str, Any]] = []
        unresolved: list[dict[str, Any]] = []
        unresolved_go: list[dict[str, Any]] = []
        source_metadata: list[dict[str, Any]] = []
        for path, document in zip(self.graph_paths, self._documents):
            edges.extend(copy.deepcopy(document.get("edges", []) or []))
            package_edges.extend(copy.deepcopy(document.get("package_edges", []) or []))
            unresolved.extend(copy.deepcopy(document.get("unresolved_imports", []) or []))
            unresolved_go.extend(copy.deepcopy(document.get("unresolved_go_usages", []) or []))
            source_metadata.append(
                {
                    "path": str(path),
                    "schema_version": document.get("schema_version"),
                    "repo_name": document.get("repo_name"),
                    "workspace_root": document.get("workspace_root"),
                    "generated_at": document.get("generated_at"),
                }
            )
        return {
            "schema_version": SCHEMA_VERSION,
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "source_graph_metadata": source_metadata,
            "nodes": copy.deepcopy(self._nodes),
            "edges": self._dedupe_dicts(
                edges,
                fields=("source", "target", "type", "raw", "line", "symbol", "owner"),
            ),
            "package_edges": self._dedupe_dicts(package_edges, fields=("source", "target", "type", "raw", "line")),
            "unresolved_imports": unresolved,
            "unresolved_go_usages": self._dedupe_dicts(
                unresolved_go,
                fields=(
                    "source", "line", "kind", "symbol", "receiver",
                    "receiver_type", "owner", "reason",
                ),
            ),
        }

    def _build_symbol_index(self) -> None:
        index: defaultdict[str, list[SymbolDefinition]] = defaultdict(list)
        seen: set[tuple[Any, ...]] = set()
        for node in self._nodes:
            source_file = _posix(node.get("file"))
            language = str(node.get("language") or "").lower()
            for entity in node.get("entities", []) or []:
                if not isinstance(entity, dict):
                    continue
                if language == "python":
                    if entity.get("scope") != "module" or entity.get("importable") is not True:
                        continue
                    if entity.get("kind") not in {
                        "class",
                        "function",
                        "async_function",
                        "route_handler",
                        "constant",
                    }:
                        continue
                if language == "go":
                    if entity.get("kind") == "package":
                        continue
                    if entity.get("scope") not in {None, "package"}:
                        continue
                name = _canonical_symbol(entity.get("name") or entity.get("entity_name"))
                if not name:
                    continue
                line_range = entity.get("line_range") or {}
                definition = SymbolDefinition(
                    name=name,
                    source_file=source_file,
                    kind=entity.get("kind") or entity.get("entity_type"),
                    start_line=line_range.get("start_line") or entity.get("start_line"),
                    end_line=line_range.get("end_line") or entity.get("end_line"),
                    exported=entity.get("exported"),
                    qualified_name=entity.get("qualified_name") or name,
                    owner=entity.get("owner"),
                    scope=entity.get("scope"),
                    importable=entity.get("importable"),
                )
                key = (
                    definition.name,
                    definition.source_file,
                    definition.kind,
                    definition.start_line,
                    definition.end_line,
                )
                if key not in seen:
                    seen.add(key)
                    index[name].append(definition)
        for definitions in index.values():
            definitions.sort(key=lambda d: (d.source_file, d.start_line or -1, d.kind or ""))
        self._symbol_index = index

    def _resolve_import(
        self,
        source_file: str,
        import_object: Mapping[str, Any],
    ) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any] | None]:
        result = copy.deepcopy(dict(import_object))
        raw = str(result.get("raw") or result.get("module") or "").strip()
        module = str(result.get("module") or result.get("raw") or "").strip()
        original_symbols = [c for c in map(_canonical_symbol, result.get("symbols") or []) if c]
        uncertainty_reasons = sorted(set(result.get("uncertainty_reasons") or []))
        is_dynamic = (
            result.get("import_style") == "dynamic_import"
            or result.get("resolution_eligible") is False
            or "dynamic_import" in uncertainty_reasons
        )
        is_wildcard = "*" in original_symbols or "wildcard_import" in uncertainty_reasons
        symbols = [symbol for symbol in original_symbols if symbol != "*"]
        existing_path = _posix(result.get("resolved_file"))
        existing_path_valid = bool(existing_path and existing_path in self._node_by_file)
        hard_path_reason = self._hard_path_reason(raw)

        if result.get("resolution_kind") == "package" and result.get("internal"):
            result.update(
                {
                    "resolved_path": None,
                    "resolved_paths": [],
                    "symbol_resolutions": [],
                    "is_unresolved": False,
                    "is_uncertain": False,
                    "uncertainty_reasons": [],
                    "reason": None,
                    "resolution_status": "resolved_package",
                    "lrm_resolution_strategy": result.get("resolution_strategy"),
                }
            )
            return result, [], None

        if is_dynamic or is_wildcard:
            reason = "dynamic_import" if is_dynamic else "wildcard_import"
            result.update(
                {
                    "resolved_path": None,
                    "resolved_paths": [],
                    "symbol_resolutions": [
                        self._unresolved_symbol(symbol, reason) for symbol in symbols
                    ],
                    "is_unresolved": True,
                    "is_uncertain": True,
                    "uncertainty_reasons": sorted({*uncertainty_reasons, reason}),
                    "reason": reason,
                    "resolution_status": "uncertain",
                    "lrm_resolution_strategy": None,
                }
            )
            return result, [], self._unresolved_record(source_file, result, reason)

        # The existing graph builder already resolves @/ and ~/ when tsconfig/src
        # rules produce a concrete file. Preserve that stronger evidence unless the
        # caller explicitly requests literal PRD hard-path behavior.
        if hard_path_reason and (self.strict_hard_path or not existing_path_valid):
            symbol_resolutions = [
                self._unresolved_symbol(symbol, "hard_path_skipped") for symbol in symbols
            ]
            result.update(
                {
                    "resolved_path": None,
                    "resolved_paths": [],
                    "symbol_resolutions": symbol_resolutions,
                    "is_unresolved": True,
                    "reason": "hard_path_skipped",
                    "resolution_status": "hard_path_skipped",
                    "lrm_resolution_strategy": None,
                }
            )
            return result, [], self._unresolved_record(source_file, result, hard_path_reason)

        module_only = not symbols and existing_path_valid
        symbol_resolutions = [
            self._resolve_symbol(symbol=symbol, module=module, existing_path=existing_path if existing_path_valid else None)
            for symbol in symbols
        ]
        resolved_paths, status, strategy, reason = _import_status(symbols, symbol_resolutions, existing_path if module_only else None)

        result.update(
            {
                "resolved_path": resolved_paths[0] if len(resolved_paths) == 1 else None,
                "resolved_paths": resolved_paths,
                "symbol_resolutions": symbol_resolutions,
                "is_unresolved": status in {"partial", "unresolved"},
                "reason": reason,
                "resolution_status": status,
                "lrm_resolution_strategy": strategy,
                "is_uncertain": bool(uncertainty_reasons),
                "uncertainty_reasons": uncertainty_reasons,
            }
        )

        edges = _import_edges(source_file, raw, result, symbol_resolutions, existing_path if module_only else None)
        unresolved = None
        if result["is_unresolved"]:
            unresolved = self._unresolved_record(source_file, result, reason or "unresolved")
        return result, edges, unresolved

    def _resolve_symbol(
        self,
        *,
        symbol: str,
        module: str,
        existing_path: str | None,
    ) -> dict[str, Any]:
        definitions = list(self._symbol_index.get(symbol, []))
        candidate_paths = sorted({definition.source_file for definition in definitions})

        if existing_path:
            exact_in_existing = [d for d in definitions if d.source_file == existing_path]
            if exact_in_existing:
                return {
                    "symbol": symbol,
                    "resolved_path": existing_path,
                    "confidence": "high",
                    "strategy": "existing_file_plus_exact_symbol",
                    "reason": None,
                    "candidates": [],
                }
            # A module can re-export a symbol defined elsewhere. Accept a unique
            # global definition, but record that it was not found in the imported
            # module itself.
            if len(candidate_paths) == 1:
                return {
                    "symbol": symbol,
                    "resolved_path": candidate_paths[0],
                    "confidence": "medium",
                    "strategy": "unique_symbol_via_resolved_module",
                    "reason": None,
                    "candidates": [],
                }

        if len(candidate_paths) == 1:
            candidate = candidate_paths[0]
            if self.allow_global_symbol_fallback or self._module_matches_file(module, candidate):
                return {
                    "symbol": symbol,
                    "resolved_path": candidate,
                    "confidence": "medium" if self.allow_global_symbol_fallback else "high",
                    "strategy": "unique_global_symbol" if self.allow_global_symbol_fallback else "module_scoped_unique_symbol",
                    "reason": None,
                    "candidates": [],
                }
            return self._unresolved_symbol(symbol, "module_scope_mismatch", candidate_paths)

        if len(candidate_paths) > 1:
            return self._unresolved_symbol(symbol, "ambiguous_symbol", candidate_paths)
        return self._unresolved_symbol(symbol, "symbol_not_found")

    def _unresolved_symbol(
        self,
        symbol: str,
        reason: str,
        candidates: Iterable[str] | None = None,
    ) -> dict[str, Any]:
        return {
            "symbol": symbol,
            "resolved_path": None,
            "confidence": "none",
            "strategy": None,
            "reason": reason,
            "candidates": sorted(set(candidates or [])),
        }

    def _hard_path_reason(self, raw: str) -> str | None:
        cleaned = raw.strip().strip("'\"`")
        if cleaned.startswith("@/"):
            return "alias_prefix_@/"
        if cleaned.startswith("~/"):
            return "alias_prefix_~/"
        parent_hops = 0
        remaining = cleaned
        while remaining.startswith("../"):
            parent_hops += 1
            remaining = remaining[3:]
        if parent_hops >= self.deep_relative_parent_hops:
            return f"deep_relative_path_{parent_hops}_parent_hops"
        return None

    def _module_matches_file(self, module: str, source_file: str) -> bool:
        cleaned = module.strip().strip("'\"`")
        cleaned = cleaned.lstrip(".")
        if cleaned.startswith("@/") or cleaned.startswith("~/"):
            cleaned = cleaned[2:]
        cleaned = cleaned.replace("\\", "/").replace(".", "/").strip("/")
        if not cleaned:
            return False

        module_parts = [part for part in cleaned.split("/") if part]
        file_path = PurePosixPath(_posix(source_file))
        without_suffix = str(file_path.with_suffix(""))
        file_parts = list(PurePosixPath(without_suffix).parts)
        if file_parts and file_parts[-1] == "__init__":
            file_parts = file_parts[:-1]
        if file_parts and file_parts[-1] == "index":
            file_parts = file_parts[:-1]
        if not file_parts:
            return False

        # A module can name either the file itself (models -> models.py) or a
        # package that contains the symbol file (models -> models/order.py).
        candidate_sequences = [file_parts]
        if len(file_parts) > 1:
            candidate_sequences.append(file_parts[:-1])
        for candidate_parts in candidate_sequences:
            max_compare = min(len(module_parts), len(candidate_parts))
            if any(
                module_parts[-size:] == candidate_parts[-size:]
                for size in range(max_compare, 0, -1)
                if size >= 1
            ):
                return True
        return False

    def _unresolved_record(
        self,
        source_file: str,
        import_object: Mapping[str, Any],
        detail: str,
    ) -> dict[str, Any]:
        return {
            "source_file": source_file,
            "raw": import_object.get("raw"),
            "module": import_object.get("module"),
            "symbols": import_object.get("symbols") or [],
            "line": import_object.get("line"),
            "resolution_status": import_object.get("resolution_status"),
            "reason": import_object.get("reason"),
            "detail": detail,
            "symbol_resolutions": import_object.get("symbol_resolutions") or [],
        }

    def _dedupe_dicts(
        self,
        values: Iterable[dict[str, Any]],
        *,
        fields: Sequence[str],
    ) -> list[dict[str, Any]]:
        seen: set[tuple[str, ...]] = set()
        result: list[dict[str, Any]] = []
        for value in values:
            if not isinstance(value, dict):
                continue
            key = tuple(_json_key(value.get(field)) if isinstance(value.get(field), (dict, list)) else str(value.get(field)) for field in fields)
            if key not in seen:
                seen.add(key)
                result.append(value)
        return result

    def _print_summary(self, output_path: Path, summary: Mapping[str, int]) -> None:
        print("\n[SHIPREADYV2 LINKER RESOLUTION COMPLETE]")
        print(f"Output: {output_path}")
        print(f"Files indexed: {summary['files_indexed']:,}")
        print(
            "Imports: "
            f"{summary['imports_resolved']:,} resolved, "
            f"{summary['imports_resolved_package']:,} package-level, "
            f"{summary['imports_partial']:,} partial, "
            f"{summary['imports_unresolved']:,} unresolved, "
            f"{summary['imports_hard_path_skipped']:,} hard-path skipped, "
            f"{summary['imports_uncertain']:,} uncertain"
        )
        print(
            "Python enrichment: "
            f"{summary['python_files_enriched']:,} files, "
            f"{summary['python_safe_constants_added']:,} safe constants, "
            f"{summary['python_dynamic_imports_added']:,} dynamic imports marked"
        )
        print(
            "Symbols: "
            f"{summary['symbols_resolved']:,}/{summary['symbols_total']:,} resolved; "
            f"{summary['ambiguous_symbol_names']:,} ambiguous names in index"
        )
        print(f"Symbol edges added: {summary['symbol_edges_added']:,}")
        print(
            f"Go symbol edges promoted: {summary['go_symbol_edges_promoted']:,}; "
            f"unresolved Go usages: {summary['go_usages_unresolved']:,}"
        )


def _import_status(symbols, symbol_resolutions, module_path):
    """-> (resolved_paths, status, strategy, reason) for one import.

    module_path: an import without symbols whose file the graph builder
    already proved; it resolves to that file as a whole."""
    if module_path:
        return [module_path], "resolved", "existing_file_resolution", None
    resolved_paths = sorted({item["resolved_path"] for item in symbol_resolutions if item.get("resolved_path")})
    resolved_count = len([item for item in symbol_resolutions if item.get("resolved_path")])
    if symbols and resolved_count == len(symbols):
        status = "resolved" if len(resolved_paths) <= 1 else "resolved_multi_target"
        reason = None
    elif resolved_count:
        status, reason = "partial", "partial_symbol_resolution"
    else:
        status = "unresolved"
        reasons = {item.get("reason") for item in symbol_resolutions if item.get("reason")}
        reason = "ambiguous_symbol" if "ambiguous_symbol" in reasons else "unknown_symbol_or_external_module"
    strategies = sorted({str(item.get("strategy")) for item in symbol_resolutions if item.get("strategy")})
    strategy = strategies[0] if len(strategies) == 1 else ("mixed_symbol_resolution" if strategies else None)
    return resolved_paths, status, strategy, reason


def _import_edges(source_file, raw, result, symbol_resolutions, module_path):
    """One imports_symbol edge per resolved symbol, or one imports_module edge.
    Edges of an uncertain import are marked uncertain and capped at medium confidence."""
    edges = [
        {
            "source": source_file,
            "target": item["resolved_path"],
            "type": "imports_symbol",
            "symbol": item["symbol"],
            "raw": raw,
            "line": result.get("line"),
            "confidence": item.get("confidence"),
            "resolution_strategy": item.get("strategy"),
        }
        for item in symbol_resolutions
        if item.get("resolved_path")
    ]
    if module_path:
        edges.append(
            {
                "source": source_file,
                "target": module_path,
                "type": "imports_module",
                "symbol": None,
                "raw": raw,
                "line": result.get("line"),
                "confidence": result.get("resolution_confidence") or "high",
                "resolution_strategy": "existing_file_resolution",
            }
        )
    uncertainty_reasons = result.get("uncertainty_reasons")
    if uncertainty_reasons:
        for edge in edges:
            edge["is_uncertain"] = True
            edge["uncertainty_reasons"] = uncertainty_reasons
            if edge.get("confidence") == "high":
                edge["confidence"] = "medium"
    return edges


def _merge_python_imports(imports, extracted) -> tuple[list[dict[str, Any]], int]:
    """Add the extractor's uncertainty reasons to each import line and append
    dynamic imports not already present. -> (imports, dynamic imports added)."""
    uncertainty_by_line = extracted["import_uncertainty_by_line"]
    enriched: list[dict[str, Any]] = []
    seen_dynamic = set()
    for import_object in imports:
        item = copy.deepcopy(import_object)
        line = int(item.get("line") or 0)
        reasons = set(item.get("uncertainty_reasons") or [])
        reasons.update(uncertainty_by_line.get(line, []))
        if reasons:
            item["is_uncertain"] = True
            item["uncertainty_reasons"] = sorted(reasons)
        enriched.append(item)
        if item.get("import_style") == "dynamic_import":
            seen_dynamic.add((item.get("line"), item.get("raw")))
    added = 0
    for dynamic_import in extracted["dynamic_imports"]:
        key = (dynamic_import.get("line"), dynamic_import.get("raw"))
        if key not in seen_dynamic:
            enriched.append(dynamic_import)
            seen_dynamic.add(key)
            added += 1
    return enriched, added
