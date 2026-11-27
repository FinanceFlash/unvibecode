"""Tree-sitter adapter: JS/TS/TSX/JSX, Rust, Go, PHP and Ruby -> imports,
entities and role hints, in the same shape as parse_py. Go files also get
"usages" (identifier and selector uses) that build.py resolves across packages.

A missing grammar or package degrades to parser_used="tree_sitter_missing"
with no imports, never an exception."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import TREE_SITTER_LANGUAGE_CANDIDATES
from .parse_go import GoUsageCollector, go_is_exported, go_is_package_level, go_named_type, go_receiver_type
from .util import child_by_field_name, clean_string_literal, line_range_from_ts_node, named_children, node_text, walk_ts


# -----------------------------------------------------------------------------
# Optional Tree-sitter loaders.
# This supports two common Python package styles:
#   1) tree_sitter_language_pack
#   2) tree_sitter_languages
# -----------------------------------------------------------------------------
TREE_SITTER_BACKEND = None

try:
    from tree_sitter_language_pack import get_parser as _tslp_get_parser  # type: ignore

    TREE_SITTER_BACKEND = "tree_sitter_language_pack"
except Exception:
    _tslp_get_parser = None  # type: ignore

try:
    from tree_sitter_languages import get_parser as _tslangs_get_parser  # type: ignore

    if TREE_SITTER_BACKEND is None:
        TREE_SITTER_BACKEND = "tree_sitter_languages"
except Exception:
    _tslangs_get_parser = None  # type: ignore


# -----------------------------------------------------------------------------
# Tree-sitter adapter
# -----------------------------------------------------------------------------
class TreeSitterAstAdapter:
    def __init__(self) -> None:
        self._parser_cache: dict[str, tuple[Any, str]] = {}  # key -> (parser, parser_used label)

    def parse(self, language: str, rel_file: str, abs_file: Path, source_text: str) -> dict[str, Any]:
        parser, parser_used, errors = self._get_parser(language)
        if parser is None:
            return {
                "imports": [],
                "entities": [],
                "role_hints": self._path_role_hints(rel_file),
                "parse_errors": errors,
                "parser_used": "tree_sitter_missing",
                "parser_confidence": "none",
            }

        source_bytes = source_text.encode("utf-8", errors="ignore")
        try:
            tree = parser.parse(source_bytes)
            root = tree.root_node
        except Exception as exc:
            return {
                "imports": [],
                "entities": [],
                "role_hints": self._path_role_hints(rel_file),
                "parse_errors": [f"TreeSitterParseError: {exc}"],
                "parser_used": parser_used,
                "parser_confidence": "low",
            }

        if language in {"javascript", "jsx", "typescript", "tsx"}:
            extracted = self._extract_js_ts(language, root, source_bytes, rel_file)
        elif language == "rust":
            extracted = self._extract_rust(root, source_bytes, rel_file)
        elif language == "go":
            extracted = self._extract_go(root, source_bytes, rel_file)
        elif language == "php":
            extracted = self._extract_php(root, source_bytes, rel_file)
        elif language == "ruby":
            extracted = self._extract_ruby(root, source_bytes, rel_file)
        else:
            extracted = {
                "imports": [],
                "entities": [],
                "role_hints": self._path_role_hints(rel_file),
                "parse_errors": [f"Unsupported tree-sitter language: {language}"],
            }

        extracted["parser_used"] = parser_used
        extracted["parser_confidence"] = "high" if parser is not None else "none"
        return extracted

    def _get_parser(self, language: str) -> tuple[Any | None, str, list[str]]:
        errors: list[str] = []
        candidates = TREE_SITTER_LANGUAGE_CANDIDATES.get(language, [language])

        for candidate in candidates:
            cache_key = f"{TREE_SITTER_BACKEND}:{candidate}"
            if cache_key in self._parser_cache:
                parser, label = self._parser_cache[cache_key]
                return parser, label, []

            if _tslp_get_parser is not None:
                try:
                    parser = _tslp_get_parser(candidate)
                    label = f"tree_sitter_language_pack:{candidate}"
                    self._parser_cache[cache_key] = (parser, label)
                    return parser, label, []
                except Exception as exc:
                    errors.append(f"tree_sitter_language_pack failed for {candidate}: {exc}")

            if _tslangs_get_parser is not None:
                try:
                    parser = _tslangs_get_parser(candidate)
                    label = f"tree_sitter_languages:{candidate}"
                    self._parser_cache[cache_key] = (parser, label)
                    return parser, label, []
                except Exception as exc:
                    errors.append(f"tree_sitter_languages failed for {candidate}: {exc}")

        if not errors:
            errors.append(
                "Tree-sitter parser package not installed. Install: pip install tree-sitter tree-sitter-language-pack"
            )
        return None, "tree_sitter_missing", errors

    # ---- JS / TS / TSX / JSX ----
    def _extract_js_ts(self, language: str, root: Any, source_bytes: bytes, rel_file: str) -> dict[str, Any]:
        imports: list[dict[str, Any]] = []
        entities: list[dict[str, Any]] = []
        role_hints: list[str] = self._path_role_hints(rel_file)

        for node in walk_ts(root):
            t = node.type

            if t in {"import_statement", "import_declaration"}:
                raw_values = self._string_literals_inside(node, source_bytes)
                if raw_values:
                    imports.append(
                        {
                            "raw": raw_values[-1],
                            "module": raw_values[-1],
                            "symbols": self._js_import_symbols(node, source_bytes),
                            "import_style": "import_statement",
                            "line": line_range_from_ts_node(node)["start_line"],
                        }
                    )

            elif t == "call_expression":
                func = child_by_field_name(node, "function")
                func_text = node_text(func, source_bytes).strip() if func is not None else ""
                if func_text in {"require", "import"}:
                    raw_values = self._string_literals_inside(node, source_bytes)
                    if raw_values:
                        imports.append(
                            {
                                "raw": raw_values[0],
                                "module": raw_values[0],
                                "symbols": [],
                                "import_style": func_text,
                                "line": line_range_from_ts_node(node)["start_line"],
                            }
                        )

            elif t in {"function_declaration", "generator_function_declaration"}:
                name = self._name_from_node(node, source_bytes)
                if name:
                    entities.append(self._entity(name, "function", node, source_bytes, exported=self._is_exported(node)))

            elif t == "class_declaration":
                name = self._name_from_node(node, source_bytes)
                if name:
                    entities.append(self._entity(name, "class", node, source_bytes, exported=self._is_exported(node)))

            elif t in {"method_definition", "method_signature"}:
                name = self._name_from_node(node, source_bytes)
                if name:
                    entities.append(self._entity(name, "method", node, source_bytes, exported=False))

            elif t == "lexical_declaration":
                entities.extend(self._extract_js_lexical_entities(node, source_bytes))

            elif t == "export_statement":
                # Export statements often wrap declarations. The wrapped declaration is also extracted elsewhere.
                pass

        # Framework/path role hints
        p = rel_file.lower().replace("\\", "/")
        if any(seg in p for seg in ["pages/api", "app/api", "/api/"]):
            role_hints.append("api_route_file")
        if p.endswith(("page.tsx", "page.jsx", "page.js", "page.ts")):
            role_hints.append("next_page_component")
        if p.endswith(("route.ts", "route.js")) or "/routes/" in p:
            role_hints.append("api_route_file")
        if any(x in p for x in ["component", "components", ".tsx", ".jsx"]):
            role_hints.append("ui_component_file")
        if any(x in p for x in ["hook", "hooks", "use"]):
            role_hints.append("react_hook_or_state_file")

        return {
            "imports": self._dedupe_imports(imports),
            "entities": self._dedupe_entities(entities),
            "role_hints": sorted(set(role_hints)),
            "parse_errors": [],
        }

    def _extract_js_lexical_entities(self, node: Any, source_bytes: bytes) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for child in walk_ts(node):
            if child.type != "variable_declarator":
                continue
            name_node = child_by_field_name(child, "name")
            value_node = child_by_field_name(child, "value")
            if name_node is None or value_node is None:
                continue
            value_type = value_node.type
            if value_type in {"arrow_function", "function", "function_expression"}:
                name = node_text(name_node, source_bytes).strip()
                if name:
                    kind = "component" if self._looks_like_react_component(name) else "function"
                    if name.startswith("use") and len(name) > 3 and name[3].isupper():
                        kind = "hook"
                    out.append(self._entity(name, kind, child, source_bytes, exported=self._is_exported(node)))
        return out

    def _js_import_symbols(self, node: Any, source_bytes: bytes) -> list[str]:
        symbols: list[str] = []
        for child in walk_ts(node):
            # This is AST-driven: we look at identifier nodes under the import statement.
            # We exclude the final string module specifier separately.
            if child.type in {"identifier", "property_identifier", "shorthand_property_identifier"}:
                txt = node_text(child, source_bytes).strip()
                if txt and txt not in symbols:
                    symbols.append(txt)
        return symbols[:50]

    def _string_literals_inside(self, node: Any, source_bytes: bytes) -> list[str]:
        vals: list[str] = []
        for child in walk_ts(node):
            if child.type in {"string", "string_fragment", "template_string"}:
                txt = clean_string_literal(node_text(child, source_bytes))
                if txt and txt not in vals:
                    vals.append(txt)
        return vals

    def _name_from_node(self, node: Any, source_bytes: bytes) -> str | None:
        for field in ["name", "property"]:
            n = child_by_field_name(node, field)
            if n is not None:
                txt = node_text(n, source_bytes).strip()
                if txt:
                    return txt
        for child in named_children(node):
            if child.type in {"identifier", "property_identifier", "type_identifier"}:
                return node_text(child, source_bytes).strip()
        return None

    def _looks_like_react_component(self, name: str) -> bool:
        return bool(name and name[0].isupper())

    def _is_exported(self, node: Any) -> bool:
        parent = getattr(node, "parent", None)
        while parent is not None:
            if getattr(parent, "type", None) == "export_statement":
                return True
            parent = getattr(parent, "parent", None)
        return False

    # ---- Rust ----
    def _extract_rust(self, root: Any, source_bytes: bytes, rel_file: str) -> dict[str, Any]:
        imports: list[dict[str, Any]] = []
        entities: list[dict[str, Any]] = []
        role_hints: list[str] = self._path_role_hints(rel_file)

        for node in walk_ts(root):
            t = node.type
            if t == "use_declaration":
                raw = node_text(node, source_bytes).strip().removeprefix("use").rstrip(";").strip()
                imports.append(
                    {
                        "raw": raw,
                        "module": raw,
                        "symbols": [],
                        "import_style": "use",
                        "line": line_range_from_ts_node(node)["start_line"],
                    }
                )
            elif t in {"mod_item", "mod_declaration"}:
                name = self._name_from_node(node, source_bytes)
                if name and child_by_field_name(node, "body") is None:
                    path = self._rust_path_attribute(node, source_bytes)
                    imports.append(
                        {
                            "raw": path or name,
                            "module": path or name,
                            "symbols": [],
                            "import_style": "mod_path" if path else "mod",
                            "line": line_range_from_ts_node(node)["start_line"],
                        }
                    )
            elif t == "function_item":
                name = self._name_from_node(node, source_bytes)
                if name:
                    entities.append(self._entity(name, "function", node, source_bytes, exported=self._rust_is_pub(node, source_bytes)))
            elif t == "struct_item":
                name = self._name_from_node(node, source_bytes)
                if name:
                    entities.append(self._entity(name, "struct", node, source_bytes, exported=self._rust_is_pub(node, source_bytes)))
            elif t == "enum_item":
                name = self._name_from_node(node, source_bytes)
                if name:
                    entities.append(self._entity(name, "enum", node, source_bytes, exported=self._rust_is_pub(node, source_bytes)))
            elif t == "trait_item":
                name = self._name_from_node(node, source_bytes)
                if name:
                    entities.append(self._entity(name, "trait", node, source_bytes, exported=self._rust_is_pub(node, source_bytes)))
            elif t == "impl_item":
                first_line = node_text(node, source_bytes).strip().splitlines()[0][:160]
                entities.append(self._entity(first_line, "impl", node, source_bytes, exported=False))

        return {
            "imports": self._dedupe_imports(imports),
            "entities": self._dedupe_entities(entities),
            "role_hints": sorted(set(role_hints)),
            "parse_errors": [],
        }

    @staticmethod
    def _rust_path_attribute(node: Any, source_bytes: bytes) -> str | None:
        sibling = node.prev_named_sibling
        while sibling is not None and sibling.type == "attribute_item":
            attribute = next(iter(named_children(sibling)), None)
            parts = named_children(attribute) if attribute is not None else []
            value = child_by_field_name(attribute, "value") if attribute is not None else None
            if parts and value is not None and node_text(parts[0], source_bytes) == "path":
                return clean_string_literal(node_text(value, source_bytes))
            sibling = sibling.prev_named_sibling
        return None

    def _rust_is_pub(self, node: Any, source_bytes: bytes) -> bool:
        txt = node_text(node, source_bytes).lstrip()
        return txt.startswith("pub ") or txt.startswith("pub(")

    # ---- PHP ----
    def _extract_php(self, root: Any, source_bytes: bytes, rel_file: str) -> dict[str, Any]:
        imports: list[dict[str, Any]] = []
        entities: list[dict[str, Any]] = []
        role_hints: list[str] = self._path_role_hints(rel_file)

        for node in walk_ts(root):
            t = node.type
            if t in {"namespace_use_declaration", "namespace_use_clause"}:
                raw = node_text(node, source_bytes).replace("use", "", 1).rstrip(";").strip()
                if raw:
                    imports.append(
                        {
                            "raw": raw,
                            "module": raw,
                            "symbols": [],
                            "import_style": "use",
                            "line": line_range_from_ts_node(node)["start_line"],
                        }
                    )
            elif t in {"namespace_definition"}:
                # Namespace is kept as file metadata entity because it affects resolution.
                raw = node_text(node, source_bytes).split("{")[0].rstrip(";").strip()
                entities.append(self._entity(raw, "namespace", node, source_bytes, exported=True))
            elif t in {"class_declaration", "interface_declaration", "trait_declaration"}:
                name = self._name_from_node(node, source_bytes)
                if name:
                    kind = t.replace("_declaration", "")
                    entities.append(self._entity(name, kind, node, source_bytes, exported=True))
            elif t in {"function_definition", "method_declaration"}:
                name = self._name_from_node(node, source_bytes)
                if name:
                    kind = "method" if t == "method_declaration" else "function"
                    entities.append(self._entity(name, kind, node, source_bytes, exported=True))

        return {
            "imports": self._dedupe_imports(imports),
            "entities": self._dedupe_entities(entities),
            "role_hints": sorted(set(role_hints)),
            "parse_errors": [],
        }

    # ---- Ruby ----
    def _extract_ruby(self, root: Any, source_bytes: bytes, rel_file: str) -> dict[str, Any]:
        imports: list[dict[str, Any]] = []
        entities: list[dict[str, Any]] = []
        role_hints: list[str] = self._path_role_hints(rel_file)

        for node in walk_ts(root):
            t = node.type
            if t == "call":
                txt = node_text(node, source_bytes).strip()
                if txt.startswith("require ") or txt.startswith("require_relative "):
                    parts = txt.split(None, 1)
                    if len(parts) == 2:
                        raw = clean_string_literal(parts[1].strip())
                        imports.append(
                            {
                                "raw": raw,
                                "module": raw,
                                "symbols": [],
                                "import_style": parts[0],
                                "line": line_range_from_ts_node(node)["start_line"],
                            }
                        )
            elif t == "class":
                name = self._name_from_node(node, source_bytes) or self._ruby_class_module_name(node, source_bytes)
                if name:
                    entities.append(self._entity(name, "class", node, source_bytes, exported=True))
            elif t == "module":
                name = self._name_from_node(node, source_bytes) or self._ruby_class_module_name(node, source_bytes)
                if name:
                    entities.append(self._entity(name, "module", node, source_bytes, exported=True))
            elif t in {"method", "singleton_method"}:
                name = self._name_from_node(node, source_bytes)
                if name:
                    entities.append(self._entity(name, "method", node, source_bytes, exported=True))

        return {
            "imports": self._dedupe_imports(imports),
            "entities": self._dedupe_entities(entities),
            "role_hints": sorted(set(role_hints)),
            "parse_errors": [],
        }

    def _ruby_class_module_name(self, node: Any, source_bytes: bytes) -> str | None:
        for child in named_children(node):
            if child.type in {"constant", "scope_resolution"}:
                return node_text(child, source_bytes).strip()
        return None

    def _extract_go(self, root: Any, source_bytes: bytes, rel_file: str) -> dict[str, Any]:
        imports: list[dict[str, Any]] = []
        entities: list[dict[str, Any]] = []
        role_hints: list[str] = self._path_role_hints(rel_file)
        parse_errors: list[str] = []
        lowered = rel_file.lower().replace("\\", "/")
        if lowered.startswith("cmd/"):
            role_hints.append("cli_entrypoint")
        if rel_file.endswith("_test.go"):
            role_hints.append("test_file")

        for node in walk_ts(root):
            t = node.type
            if t == "ERROR":
                parse_errors.append("tree-sitter partial parse (ERROR node present)")
            elif t == "import_spec":
                imports += self._go_import(node, source_bytes)
            elif t == "package_clause":
                entities += self._go_package(node, source_bytes)
            elif t in {"function_declaration", "method_declaration"}:
                entities += self._go_function(node, source_bytes)
            elif t in {"type_spec", "type_alias"}:
                entities += self._go_type(node, source_bytes)
            elif t in {"var_spec", "const_spec"}:
                entities += self._go_values(node, source_bytes, "var" if t == "var_spec" else "const")

        usages = GoUsageCollector(source_bytes).collect(root)

        return {
            "imports": self._dedupe_imports(imports),
            "entities": self._dedupe_entities(entities),
            "role_hints": sorted(set(role_hints)),
            "parse_errors": sorted(set(parse_errors)),
            "usages": usages,
            "shadow_names": [],
        }

    # --- Go declarations: each returns the records for one syntax node ------

    @staticmethod
    def _go_first(node: Any, child_type: str, source_bytes: bytes) -> str | None:
        """Text of the first named child of `child_type`, or None."""
        for child in named_children(node):
            if child.type == child_type:
                return node_text(child, source_bytes).strip()
        return None

    def _go_import(self, node: Any, source_bytes: bytes) -> list[dict[str, Any]]:
        path = None
        alias: str | None = None
        for child in named_children(node):
            if child.type in {"interpreted_string_literal", "raw_string_literal"}:
                path = clean_string_literal(node_text(child, source_bytes))
            elif child.type == "package_identifier":
                alias = node_text(child, source_bytes).strip()
            elif child.type == "dot":
                alias = "."
            elif child.type == "blank_identifier":
                alias = "_"
        if alias is None:  # some grammars do not expose dot/blank as named children
            raw_spec = node_text(node, source_bytes).strip()
            if raw_spec.startswith(". ") or raw_spec.startswith(".'") or raw_spec.startswith('."'):
                alias = "."
            elif raw_spec.startswith("_ ") or raw_spec.startswith("_'") or raw_spec.startswith('_\"'):
                alias = "_"
        if not path:
            return []
        style = {".": "import_dot", "_": "import_blank"}.get(alias or "", "import_alias" if alias else "import")
        return [
            {
                "raw": path,
                "module": path,
                "symbols": [],
                "import_style": style,
                "alias": alias,
                "line": line_range_from_ts_node(node)["start_line"],
            }
        ]

    def _go_package(self, node: Any, source_bytes: bytes) -> list[dict[str, Any]]:
        name = self._go_first(node, "package_identifier", source_bytes)
        if not name:
            return []
        entity = self._entity(name, "package", node, source_bytes, exported=False)
        entity["scope"] = "package"
        return [entity]

    def _go_function(self, node: Any, source_bytes: bytes) -> list[dict[str, Any]]:
        is_method = node.type == "method_declaration"
        name = self._go_first(node, "field_identifier" if is_method else "identifier", source_bytes)
        if not name:
            return []
        receiver = go_receiver_type(node, source_bytes) if is_method else None
        entity = self._entity(
            name, "method" if is_method else "function", node, source_bytes, exported=go_is_exported(name)
        )
        entity["scope"] = "package"
        if receiver:
            entity["owner"] = receiver
            entity["qualified_name"] = f"{receiver}.{name}"
        returns = go_named_type(child_by_field_name(node, "result"), source_bytes)
        if returns:
            entity["returns"] = returns
        return [entity]

    def _go_type(self, node: Any, source_bytes: bytes) -> list[dict[str, Any]]:
        name = self._go_first(node, "type_identifier", source_bytes)
        if not name:
            return []
        kind = "type"
        for child in named_children(node):  # the last struct/interface child wins, as before
            if child.type == "struct_type":
                kind = "struct"
            elif child.type == "interface_type":
                kind = "interface"
        entity = self._entity(name, kind, node, source_bytes, exported=go_is_exported(name))
        entity["scope"] = "package" if go_is_package_level(node) else "local"
        return [entity]

    def _go_values(self, node: Any, source_bytes: bytes, kind: str) -> list[dict[str, Any]]:
        entities = []
        for child in named_children(node):
            if child.type != "identifier":
                continue
            name = node_text(child, source_bytes).strip()
            if not name or name == "_":
                continue
            entity = self._entity(name, kind, node, source_bytes, exported=go_is_exported(name))
            entity["scope"] = "package" if go_is_package_level(node) else "local"
            entities.append(entity)
        return entities

    # ---- shared helpers ----
    def _entity(self, name: str, kind: str, node: Any, source_bytes: bytes, exported: bool) -> dict[str, Any]:
        return {
            "name": name,
            "kind": kind,
            "line_range": line_range_from_ts_node(node),
            "exported": bool(exported),
        }

    def _path_role_hints(self, rel_file: str) -> list[str]:
        p = rel_file.lower().replace("\\", "/")
        hints = []
        if any(part in p for part in ["route", "routes", "controller", "controllers", "api/"]):
            hints.append("api_or_controller_file")
        if any(part in p for part in ["model", "models", "schema", "entity", "entities"]):
            hints.append("data_model_file")
        if any(part in p for part in ["service", "services"]):
            hints.append("service_file")
        if any(part in p for part in ["auth", "login", "jwt", "session"]):
            hints.append("auth_related_file")
        if any(part in p for part in ["payment", "billing", "invoice", "order", "checkout"]):
            hints.append("transaction_related_file")
        if any(part in p for part in ["db", "database", "repo", "repository", "dao"]):
            hints.append("persistence_related_file")
        return hints

    def _dedupe_imports(self, imports: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen = set()
        out = []
        for item in imports:
            key = (item.get("raw"), item.get("import_style"), item.get("line"))
            if key not in seen:
                seen.add(key)
                out.append(item)
        return out

    def _dedupe_entities(self, entities: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen = set()
        out = []
        for item in entities:
            lr = item.get("line_range", {})
            key = (item.get("name"), item.get("kind"), lr.get("start_line"), lr.get("end_line"))
            if key not in seen:
                seen.add(key)
                out.append(item)
        return out
