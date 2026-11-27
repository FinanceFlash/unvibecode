"""Go: cross-file symbol edges, which need more than import resolution.

A Go import names a package (a folder), not a file, so build.py first builds
a catalog of every package's declarations and then resolves each file's
"usages" (from parse_ts) against it:

    selector         pkg.Name          -> the file in pkg that declares Name
    same_package_call Name()           -> another file of the same package
    method_call      x.Method()        -> the file declaring Method on x's type

An edge is added only when exactly one file qualifies. Ambiguous or
unprovable uses become unresolved_go_usages records with a reason;
external packages and the file's own declarations produce nothing.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from .util import _posix


def build_go_catalog(nodes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Package folder -> its package names, files and declarations by kind."""
    catalog: dict[str, dict[str, Any]] = {}
    for node in nodes:
        if node.get("language") != "go":
            continue
        file_path = str(node.get("file"))
        package_dir = str(Path(file_path).parent).replace("\\", "/")
        entry = catalog.setdefault(
            package_dir,
            {
                "names": set(),
                "production_names": set(),
                "files": {},
                "symbols": defaultdict(list),
                "functions": defaultdict(list),
                "methods": defaultdict(list),
                "types": defaultdict(list),
            },
        )
        package_name = None
        for entity in node.get("entities", []) or []:
            if not isinstance(entity, dict):
                continue
            if entity.get("kind") == "package":
                name = str(entity.get("name") or "")
                if name:
                    package_name = name
                    entry["names"].add(name)
        entry["files"][file_path] = package_name
        if package_name and not file_path.endswith("_test.go"):
            entry["production_names"].add(package_name)
        for entity in node.get("entities", []) or []:
            if not isinstance(entity, dict):
                continue
            if entity.get("scope") not in {None, "package"}:
                continue
            name = str(entity.get("name") or "")
            kind = str(entity.get("kind") or "")
            if not name or kind == "package":
                continue
            line_range = entity.get("line_range") or {}
            record = {
                "file": file_path,
                "line": line_range.get("start_line"),
                "exported": bool(entity.get("exported")),
                "kind": kind,
            }
            if kind == "function":
                record["returns"] = entity.get("returns")
                record["returns_collection"] = bool(entity.get("returns_collection"))
                entry["functions"][name].append(record)
            elif kind == "method":
                owner = str(entity.get("owner") or "")
                if owner:
                    record["owner"] = owner
                    entry["methods"][(owner, name)].append(record)
            elif kind in {"type", "struct", "interface"}:
                record["fields"] = entity.get("fields") or {}
                entry["types"][name].append(record)
            if entity.get("exported") and kind != "method" and not file_path.endswith("_test.go"):
                entry["symbols"][name].append(record)
    for entry in catalog.values():
        if not entry["production_names"]:
            entry["production_names"] = set(entry["names"])
    return catalog


def resolve_go_usages(
    node: dict[str, Any], catalog: dict[str, dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """One Go file's usages -> (edges, unresolved usages). Edges are not yet deduplicated."""
    if not node.get("go_usages"):
        return [], []
    return GoUsageResolver(node, catalog).resolve()


def hint_label(hint: dict[str, Any] | None) -> str | None:
    """A receiver type hint as text: 'pkg.Type', 'Type', 'pkg.New()' or 'New()'."""
    if not hint:
        return None
    name = str(hint.get("name") or "")
    qualifier = hint.get("qualifier")
    if hint.get("kind") == "call":
        return f"{qualifier}.{name}()" if qualifier else f"{name}()"
    return f"{qualifier}.{name}" if qualifier else name


class GoUsageResolver:
    """Resolves the usages of one Go file against the package catalog."""

    def __init__(self, node: dict[str, Any], catalog: dict[str, dict[str, Any]]) -> None:
        self.node = node
        self.catalog = catalog
        self.source_file = _posix(node.get("file"))
        self.source_dir = str(Path(self.source_file).parent).replace("\\", "/")
        self.source_entry = catalog.get(self.source_dir) or {}
        self.source_package = (self.source_entry.get("files") or {}).get(self.source_file)
        self.source_is_test = self.source_file.endswith("_test.go")
        self.edges: list[dict[str, Any]] = []
        self.unresolved: list[dict[str, Any]] = []

        # Which package each qualifier in this file refers to. A qualifier that
        # two different imports could mean maps to None (never resolved).
        self.qualifier_to_package: dict[str, str | None] = {}
        self.qualifier_to_names: dict[str, set] = {}
        for imp in node.get("imports", []) or []:
            if not imp.get("internal") or imp.get("resolution_kind") != "package":
                continue
            package_dir = imp.get("resolved_package")
            if package_dir is None or package_dir not in catalog:
                continue
            package_names = set(catalog[package_dir].get("production_names") or [])
            if not package_names:
                package_names = set(catalog[package_dir].get("names") or [])
            alias = imp.get("alias")
            qualifiers = [str(alias)] if alias and alias not in {".", "_"} else sorted(package_names)
            for qualifier in qualifiers:
                if qualifier in self.qualifier_to_package and self.qualifier_to_package[qualifier] != package_dir:
                    self.qualifier_to_package[qualifier] = None
                    self.qualifier_to_names.pop(qualifier, None)
                else:
                    self.qualifier_to_package[qualifier] = package_dir
                    self.qualifier_to_names[qualifier] = package_names

    def resolve(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        handlers = {
            "selector": self._selector,
            "qualified_type": self._selector,
            "same_package_call": self._same_package_call,
            "method_call": self._method_call,
        }
        for usage in self.node.get("go_usages") or []:
            handler = handlers.get(str(usage.get("kind") or "selector"))
            if handler is not None:
                handler(usage)
        return self.edges, self.unresolved

    # --- one handler per usage kind --------------------------------------

    def _selector(self, usage: dict[str, Any]) -> None:
        kind = str(usage.get("kind") or "selector")
        line = usage.get("line")
        qualifier = str(usage.get("qualifier") or "")
        symbol = str(usage.get("symbol") or "")
        if not qualifier or not symbol:
            return
        record, problem = self._package_symbol(qualifier, symbol, kind, line)
        if problem is not None:
            self.unresolved.append(problem)
            return
        if record is None:
            return
        symbol_kind = str(record.get("kind") or "")
        context = str(usage.get("context") or "")
        is_call = (context == "call" and symbol_kind in {"function", "var", "const"}) or (
            kind == "qualified_type" and symbol_kind == "function"
        )
        if kind == "qualified_type":
            import_style, strategy = "go_qualified_type_usage", "go_package_symbol_type"
        else:
            import_style = "go_selector_usage"
            strategy = "go_package_symbol_call" if is_call else "go_package_symbol_usage"
        self._edge(
            str(record.get("file")),
            "calls_symbol" if is_call else "imports_symbol",
            symbol,
            line,
            strategy,
            self._import_raw(str(self.qualifier_to_package.get(qualifier) or "")),
            import_style,
        )

    def _same_package_call(self, usage: dict[str, Any]) -> None:
        line = usage.get("line")
        name = str(usage.get("name") or "")
        if not name:
            return
        record, problem = self._same_package_function(name, line)
        if problem is not None:
            self.unresolved.append(problem)
            return
        if record is None:
            return
        self._edge(str(record.get("file")), "calls_symbol", name, line, "go_same_package_call", None, "same_package_call")

    def _method_call(self, usage: dict[str, Any]) -> None:
        line = usage.get("line")
        receiver = str(usage.get("receiver") or "")
        symbol = str(usage.get("symbol") or "")
        hint = usage.get("receiver_type")
        if not symbol:
            return
        resolved, reason, candidates = self._receiver_type(hint)
        if resolved is None:
            # Report only when the type is ours but unprovable; external types are silent.
            if reason and not str(reason).startswith("external"):
                same_name = self._methods_named(symbol)
                if same_name or candidates:
                    self.unresolved.append(
                        {
                            "source": self.source_file,
                            "line": line,
                            "kind": "method_call",
                            "symbol": symbol,
                            "receiver": receiver,
                            "receiver_type": hint_label(hint),
                            "reason": reason,
                            "candidates": (candidates or same_name)[:20],
                        }
                    )
            return
        owner_package_dir, owner, cross_package, qualifier = resolved
        record, problem = self._method(owner_package_dir, owner, symbol, cross_package, qualifier, line)
        if problem is not None:
            problem["receiver"] = receiver
            problem["receiver_type"] = hint_label(hint)
            self.unresolved.append(problem)
            return
        if record is None:
            return
        self._edge(
            str(record.get("file")),
            "method_call",
            symbol,
            line,
            "go_method_resolution",
            None,
            "method_call",
            owner=owner,
            receiver_type=hint_label(hint),
        )

    # --- lookups ----------------------------------------------------------

    def _package_matches(self, package_dir: str, target_file: str, cross_package: bool, qualifier: str | None = None) -> bool:
        """target_file belongs to the package this use can see (production files only across packages)."""
        entry = self.catalog.get(package_dir) or {}
        target_package = (entry.get("files") or {}).get(target_file)
        if target_package is None:
            return False
        if cross_package:
            allowed = self.qualifier_to_names.get(str(qualifier or ""))
            if not allowed:
                allowed = set(entry.get("production_names") or [])
            if target_file.endswith("_test.go"):
                return False
            return target_package in allowed
        return target_package == self.source_package

    def _import_raw(self, package_dir: str) -> str | None:
        for imp in self.node.get("imports", []) or []:
            if imp.get("resolved_package") == package_dir:
                return imp.get("raw")
        return None

    def _package_symbol(self, qualifier: str, symbol: str, usage_kind: str, line: int | None):
        """pkg.Name -> (the one declaring record, None) or (None, ambiguity problem) or (None, None)."""
        package_dir = self.qualifier_to_package.get(qualifier)
        if package_dir is None:
            return None, None
        entry = self.catalog.get(package_dir) or {}
        unique: dict[str, dict[str, Any]] = {}
        for record in entry.get("symbols", {}).get(symbol, []):
            target_file = str(record.get("file") or "")
            if not target_file or target_file == self.source_file:
                continue
            if not self._package_matches(package_dir, target_file, True, qualifier):
                continue
            unique[target_file] = record
        if len(unique) == 1:
            return next(iter(unique.values())), None
        if len(unique) > 1:
            return None, {
                "source": self.source_file,
                "line": line,
                "kind": usage_kind,
                "symbol": symbol,
                "qualifier": qualifier,
                "reason": "ambiguous_package_symbol",
                "candidates": [
                    {"file": key, "line": value.get("line"), "kind": value.get("kind")}
                    for key, value in sorted(unique.items())[:20]
                ],
            }
        return None, None

    def _same_package_function(self, name: str, line: int | None):
        """Name() -> the one other file of this package declaring it. Declared here too -> no edge."""
        if not self.source_entry or not self.source_package:
            return None, None
        unique: dict[str, dict[str, Any]] = {}
        for record in self.source_entry.get("functions", {}).get(name, []):
            target_file = str(record.get("file") or "")
            if not target_file:
                continue
            if (self.source_entry.get("files") or {}).get(target_file) != self.source_package:
                continue
            if not self.source_is_test and target_file.endswith("_test.go"):
                continue
            if target_file == self.source_file:
                return None, None
            unique[target_file] = record
        if len(unique) == 1:
            return next(iter(unique.values())), None
        if len(unique) > 1:
            return None, {
                "source": self.source_file,
                "line": line,
                "kind": "same_package_call",
                "symbol": name,
                "reason": "ambiguous_same_package_call",
                "candidates": [{"file": key, "line": value.get("line")} for key, value in sorted(unique.items())[:20]],
            }
        return None, None

    def _receiver_type(self, hint: dict[str, Any] | None):
        """Receiver type hint -> ((package_dir, type, cross_package, qualifier), None, [])
        or (None, reason, candidates). A 'call' hint (x := pkg.New()) uses the
        constructor's single declared return type."""
        if not hint:
            return None, "unknown_receiver_type", []
        if hint.get("kind") == "field":
            return self._field_type(hint)
        hint_kind = str(hint.get("kind") or "")
        qualifier = hint.get("qualifier")
        name = str(hint.get("name") or "")
        if not name:
            return None, "unknown_receiver_type", []
        if qualifier:
            package_dir = self.qualifier_to_package.get(str(qualifier))
            if package_dir is None:
                return None, "external_receiver_type", []
            cross_package = True
        else:
            package_dir = self.source_dir
            cross_package = False
        entry = self.catalog.get(package_dir)
        if not entry:
            return None, "external_receiver_type", []
        if hint_kind != "call":
            return (package_dir, name, cross_package, qualifier), None, []

        filtered = []
        for record in list(entry.get("functions", {}).get(name, [])):
            target_file = str(record.get("file") or "")
            if not target_file:
                continue
            if cross_package and not record.get("exported"):
                continue
            if (cross_package or not self.source_is_test) and target_file.endswith("_test.go"):
                continue
            if not self._package_matches(package_dir, target_file, cross_package, qualifier):
                continue
            filtered.append(record)
        element = bool(hint.get("element"))
        returns = {
            str(record.get("returns"))
            for record in filtered
            if record.get("returns") and record.get("returns_collection") == element
        }
        if len(returns) != 1:
            return None, "unknown_constructor_return", filtered[:20]
        return_type = next(iter(returns))
        if "." not in return_type:
            return (package_dir, return_type, cross_package, qualifier), None, []
        return_qualifier, return_name = return_type.split(".", 1)
        if not return_qualifier or not return_name:
            return None, "unknown_constructor_return", filtered[:20]
        if return_qualifier in (entry.get("names") or set()) or return_qualifier == qualifier:
            return (package_dir, return_name, cross_package, qualifier), None, []
        mapped = self.qualifier_to_package.get(return_qualifier)
        if mapped is None:
            return None, "external_return_type", []
        return (mapped, return_name, True, return_qualifier), None, []

    def _field_type(self, hint: dict[str, Any]):
        base, reason, candidates = self._receiver_type(hint.get("base"))
        if base is None:
            return None, reason, candidates
        package_dir, owner, cross_package, qualifier = base
        name = str(hint.get("name") or "")
        fields = {
            (str(field.get("type")), bool(field.get("collection")))
            for record in (self.catalog.get(package_dir) or {}).get("types", {}).get(owner, [])
            for field in [(record.get("fields") or {}).get(name)]
            if field
        }
        if len(fields) != 1:
            return None, "unknown_field_type", []
        field_type, collection = next(iter(fields))
        if collection != bool(hint.get("element")):
            return None, "unknown_field_type", []
        if "." in field_type:
            return None, "cross_package_field_type", []
        return (package_dir, field_type, cross_package, qualifier), None, []

    def _method(self, owner_package_dir: str, owner: str, name: str, cross_package: bool, qualifier: str | None, line: int | None):
        """Type.Method -> the one file declaring it. Interfaces and methods in this file -> no edge."""
        entry = self.catalog.get(owner_package_dir)
        if not entry:
            return None, None
        type_records = [
            record
            for record in entry.get("types", {}).get(owner, [])
            if self._package_matches(owner_package_dir, str(record.get("file") or ""), cross_package, qualifier)
        ]
        if any(str(record.get("kind")) == "interface" for record in type_records):
            return None, None
        all_records = [
            record
            for record in entry.get("methods", {}).get((owner, name), [])
            if self._package_matches(owner_package_dir, str(record.get("file") or ""), cross_package, qualifier)
        ]
        if any(str(record.get("file") or "") == self.source_file for record in all_records):
            return None, None
        unique: dict[str, dict[str, Any]] = {}
        for record in all_records:
            target_file = str(record.get("file") or "")
            if not target_file:
                continue
            if cross_package and not record.get("exported"):
                continue
            if not self.source_is_test and target_file.endswith("_test.go"):
                continue
            unique[str(record.get("file"))] = record
        if len(unique) == 1:
            return next(iter(unique.values())), None
        if len(unique) > 1:
            return None, {
                "source": self.source_file,
                "line": line,
                "kind": "method_call",
                "symbol": name,
                "owner": owner,
                "reason": "ambiguous_method",
                "candidates": [
                    {"file": key, "line": value.get("line"), "owner": owner} for key, value in sorted(unique.items())[:20]
                ],
            }
        if type_records or all_records:
            return None, {
                "source": self.source_file,
                "line": line,
                "kind": "method_call",
                "symbol": name,
                "owner": owner,
                "reason": "no_method_for_type",
                "candidates": [
                    {"file": record.get("file"), "line": record.get("line"), "owner": owner} for record in type_records[:20]
                ],
            }
        return None, None

    def _methods_named(self, symbol: str) -> list[dict[str, Any]]:
        """Every method called `symbol` in this package, as unresolved-usage candidates."""
        found = []
        for (owner, method_name), records in (self.source_entry.get("methods") or {}).items():
            if method_name != symbol:
                continue
            for record in records:
                target_file = str(record.get("file") or "")
                if not self.source_is_test and target_file.endswith("_test.go"):
                    continue
                found.append({"file": target_file, "line": record.get("line"), "owner": owner})
        return found

    def _edge(
        self,
        target: str,
        edge_type: str,
        symbol: str,
        line: int | None,
        strategy: str,
        raw: str | None,
        import_style: str,
        owner: str | None = None,
        receiver_type: str | None = None,
    ) -> None:
        edge = {
            "source": self.source_file,
            "target": target,
            "type": edge_type,
            "symbol": symbol,
            "raw": raw,
            "import_style": import_style,
            "line": line,
            "confidence": "high",
            "resolution_strategy": strategy,
        }
        if owner:
            edge["owner"] = owner
        if receiver_type:
            edge["receiver_type"] = receiver_type
        self.edges.append(edge)
