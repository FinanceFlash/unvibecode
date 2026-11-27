"""ImportResolver: an import string written in one file -> the repository file it means.

resolve(source_file, language, imp) returns imp plus resolved_file, internal,
resolution_strategy and resolution_confidence. It only ever answers with a
file from the scanned file set; everything else is reported as external or
unresolved, with a reason."""
from __future__ import annotations

import json
import posixpath
from urllib.parse import urldefrag, urlparse
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import Any

from .config import NODE_TS_EXTENSIONS
from .util import safe_read_text, to_posix_rel



def _join_relative(source_dir: Path, raw: str) -> str:
    """source_dir/raw as a repository path with '.' and '..' collapsed.

    pathlib drops '.' but keeps '..', so 'src/lazy/../utils' would never match
    the scanned file 'src/utils/index.ts'. A path that climbs above the
    repository root stays '../...' and simply does not resolve.
    """
    return posixpath.normpath(to_posix_rel(source_dir / raw))

# -----------------------------------------------------------------------------
# Resolver
# -----------------------------------------------------------------------------
class ImportResolver:
    def __init__(self, workspace_root: Path, rel_files: list[str]) -> None:
        self.workspace_root = workspace_root
        self.rel_files = sorted(to_posix_rel(f) for f in rel_files)
        self.file_set = set(self.rel_files)
        self.by_basename: dict[str, list[str]] = defaultdict(list)
        self.by_stem: dict[str, list[str]] = defaultdict(list)
        for rel in self.rel_files:
            p = Path(rel)
            self.by_basename[p.name].append(rel)
            self.by_stem[p.stem].append(rel)
        self.tsconfig_aliases = self._load_tsconfig_aliases()
        self.php_psr4 = self._load_php_psr4()
        self.go_module, self.go_replace = self._load_go_module()

    def resolve(self, source_file: str, language: str, imp: dict[str, Any]) -> dict[str, Any]:
        raw = str(imp.get("raw") or imp.get("module") or "").strip()
        result = dict(imp)
        result.update(
            {
                "resolved_file": None,
                "internal": False,
                "resolution_strategy": None,
                "resolution_confidence": "none",
            }
        )
        if not raw:
            return result

        if language == "python":
            resolved, strategy = self._resolve_python(source_file, imp)
        elif language in {"javascript", "jsx", "typescript", "tsx"}:
            resolved, strategy = self._resolve_node_ts(source_file, raw)
        elif language == "rust":
            resolved, strategy = self._resolve_rust(source_file, raw, str(imp.get("import_style") or ""))
        elif language == "go":
            resolved, strategy, package_extra = self._resolve_go(raw)
            if package_extra is not None:
                result.update(
                    {
                        "resolved_file": None,
                        "resolved_package": package_extra["package"],
                        "package_files": package_extra["files"],
                        "vendored": package_extra.get("vendored", False),
                        "internal": True,
                        "resolution_kind": "package",
                        "resolution_strategy": strategy,
                        "resolution_confidence": "high",
                    }
                )
                if str(imp.get("alias") or "") == "_":
                    result["side_effect_import"] = True
                return result
            first_segment = (raw.split("/")[0] if raw else "").strip()
            if raw.strip() == "C":
                result["external_kind"] = "cgo"
            elif first_segment and "." not in first_segment:
                result["external_kind"] = "stdlib"
            else:
                result["external_kind"] = "third_party"
        elif language == "php":
            resolved, strategy = self._resolve_php(raw)
        elif language == "ruby":
            resolved, strategy = self._resolve_ruby(source_file, raw, str(imp.get("import_style") or ""))
        elif language in {"html", "css"}:
            resolved, strategy = self._resolve_web_asset(source_file, raw)
        else:
            resolved, strategy = None, None

        if resolved:
            result.update(
                {
                    "resolved_file": resolved,
                    "internal": True,
                    "resolution_strategy": strategy,
                    "resolution_confidence": "high" if strategy not in {"basename_fallback", "stem_fallback"} else "medium",
                }
            )
        return result

    # ---- Python ----
    def _resolve_python(self, source_file: str, imp: dict[str, Any]) -> tuple[str | None, str | None]:
        module = str(imp.get("module") or "")
        raw = str(imp.get("raw") or "")
        symbols = list(imp.get("symbols") or [])
        level = int(imp.get("relative_level") or 0)
        source_dir = Path(source_file).parent

        candidate_modules: list[str] = []
        if level > 0:
            base = source_dir
            # level=1 means current package; level=2 means parent package
            for _ in range(max(0, level - 1)):
                base = base.parent
            if module:
                candidate_modules.append(to_posix_rel(base / module.replace(".", "/")))
            else:
                for sym in symbols:
                    candidate_modules.append(to_posix_rel(base / sym.replace(".", "/")))
        else:
            if module:
                candidate_modules.append(module.replace(".", "/"))
            if raw and not raw.startswith("."):
                candidate_modules.append(raw.replace(".", "/"))

        # Also support from package import thing where thing is a submodule.
        expanded: list[str] = []
        for base in candidate_modules:
            expanded.append(base)
            for sym in symbols:
                if sym != "*":
                    expanded.append(to_posix_rel(Path(base) / sym))

        for mod_path in expanded:
            candidates = [f"{mod_path}.py", f"{mod_path}/__init__.py"]
            for cand in candidates:
                cand = to_posix_rel(cand).lstrip("/")
                if cand in self.file_set:
                    return cand, "python_module_resolution"

        # Last resort: basename/stem fallback for internal local module names.
        if module:
            return self._resolve_by_basename(module.split(".")[-1])
        return None, None

    # ---- Node / TypeScript ----
    def _resolve_node_ts(self, source_file: str, raw: str) -> tuple[str | None, str | None]:
        source_dir = Path(source_file).parent
        candidates: list[str] = []

        if raw.startswith("."):
            base = _join_relative(source_dir, raw)
            candidates.extend(self._node_candidate_paths(base))
        elif raw.startswith("@/"):
            candidates.extend(self._node_candidate_paths("src/" + raw[2:]))
        elif raw.startswith("~/"):
            candidates.extend(self._node_candidate_paths("src/" + raw[2:]))
        elif raw.startswith("src/"):
            candidates.extend(self._node_candidate_paths(raw))
        else:
            # tsconfig path aliases, e.g. @app/* -> src/app/*
            for alias_prefix, target_prefix in self.tsconfig_aliases.items():
                if raw.startswith(alias_prefix):
                    suffix = raw[len(alias_prefix) :].lstrip("/")
                    candidates.extend(self._node_candidate_paths(to_posix_rel(Path(target_prefix) / suffix)))

        for cand in candidates:
            cand = to_posix_rel(cand).lstrip("/")
            if cand in self.file_set:
                return cand, "node_ts_module_resolution"
        return None, None

    def _node_candidate_paths(self, base: str) -> list[str]:
        base = to_posix_rel(base).lstrip("/")
        candidates = []
        suffix = Path(base).suffix
        if suffix:
            candidates.append(base)
        else:
            for ext in NODE_TS_EXTENSIONS:
                candidates.append(base + ext)
            for ext in NODE_TS_EXTENSIONS:
                candidates.append(to_posix_rel(Path(base) / ("index" + ext)))
        return candidates

    def _load_tsconfig_aliases(self) -> dict[str, str]:
        aliases: dict[str, str] = {}
        tsconfig = self.workspace_root / "tsconfig.json"
        if not tsconfig.exists():
            return aliases
        try:
            data = json.loads(safe_read_text(tsconfig))
            paths = data.get("compilerOptions", {}).get("paths", {})
            base_url = data.get("compilerOptions", {}).get("baseUrl", ".")
            for alias, targets in paths.items():
                if not targets:
                    continue
                alias_prefix = alias.replace("/*", "").rstrip("/")
                target_prefix = str(targets[0]).replace("/*", "").rstrip("/")
                aliases[alias_prefix] = to_posix_rel(Path(base_url) / target_prefix)
        except Exception:
            pass
        return aliases

    # ---- Rust ----
    def _resolve_rust(self, source_file: str, raw: str, style: str) -> tuple[str | None, str | None]:
        raw = raw.strip().rstrip(";")
        source_dir = Path(source_file).parent
        candidates: list[str] = []

        if style == "mod_path":
            candidates.append(_join_relative(source_dir, raw))
        elif style == "mod":
            candidates.extend(
                [
                    to_posix_rel(source_dir / f"{raw}.rs"),
                    to_posix_rel(source_dir / raw / "mod.rs"),
                    to_posix_rel(Path("src") / f"{raw}.rs"),
                    to_posix_rel(Path("src") / raw / "mod.rs"),
                ]
            )
        else:
            cleaned = raw
            for prefix in ["crate::", "self::", "super::"]:
                if cleaned.startswith(prefix):
                    cleaned = cleaned[len(prefix) :]
                    break
            parts = [p.strip("{} ") for p in cleaned.split("::") if p.strip("{} ")]
            # Try progressively shorter module paths because the last item may be a symbol.
            for n in range(len(parts), 0, -1):
                path = Path("src").joinpath(*parts[:n])
                candidates.extend([to_posix_rel(path.with_suffix(".rs")), to_posix_rel(path / "mod.rs")])

        for cand in candidates:
            cand = to_posix_rel(cand).lstrip("/")
            if cand in self.file_set:
                return cand, "rust_module_resolution"
        return None, None

    # ---- PHP ----
    def _resolve_php(self, raw: str) -> tuple[str | None, str | None]:
        # raw can include aliases or comma-separated use clauses. Keep first namespace-like token.
        token = raw.split(",")[0].strip()
        token = token.split(" as ")[0].split(" AS ")[0].strip().lstrip("\\")
        if not token:
            return None, None

        for namespace_prefix, folder in self.php_psr4.items():
            prefix = namespace_prefix.strip("\\")
            if token.startswith(prefix):
                suffix = token[len(prefix) :].lstrip("\\")
                candidate = to_posix_rel(Path(folder) / (suffix.replace("\\", "/") + ".php"))
                if candidate in self.file_set:
                    return candidate, "php_psr4_resolution"

        # Laravel/common default fallback: App\Foo\Bar -> app/Foo/Bar.php
        if token.startswith("App\\"):
            candidate = to_posix_rel(Path("app") / (token[len("App\\") :].replace("\\", "/") + ".php"))
            if candidate in self.file_set:
                return candidate, "php_app_namespace_resolution"

        return self._resolve_by_basename(token.split("\\")[-1])

    def _load_php_psr4(self) -> dict[str, str]:
        composer = self.workspace_root / "composer.json"
        psr4: dict[str, str] = {}
        if not composer.exists():
            return psr4
        try:
            data = json.loads(safe_read_text(composer))
            mappings = data.get("autoload", {}).get("psr-4", {})
            for namespace, folder in mappings.items():
                if isinstance(folder, list):
                    folder = folder[0] if folder else ""
                if folder:
                    psr4[namespace] = str(folder).rstrip("/")
        except Exception:
            pass
        return psr4

    def _load_go_module(self) -> tuple[str, dict[str, str]]:
        go_mod = self.workspace_root / "go.mod"
        module = ""
        replace: dict[str, str] = {}
        if not go_mod.exists():
            return module, replace
        try:
            text = safe_read_text(go_mod)
        except Exception:
            return module, replace
        in_replace_block = False
        for raw_line in text.splitlines():
            line = raw_line.split("//")[0].strip()
            if not line:
                continue
            if line.startswith("replace ("):
                in_replace_block = True
                continue
            if in_replace_block and line == ")":
                in_replace_block = False
                continue
            if line.startswith("module") and not module:
                parts = line.split()
                if len(parts) >= 2:
                    module = parts[1].strip().strip('"')
                continue
            target: str | None = None
            if in_replace_block:
                target = line
            elif line.startswith("replace "):
                target = line[len("replace ") :]
            if target and "=>" in target:
                old, _, new = target.partition("=>")
                old = old.strip().split()[0].strip()
                new = new.strip().split()[0].strip().strip('"')
                if new.startswith("./") or new.startswith("../"):
                    local = (self.workspace_root / new)
                    try:
                        replace[old] = to_posix_rel(local.resolve().relative_to(self.workspace_root.resolve()))
                    except Exception:
                        replace[old] = to_posix_rel(Path(new))
                elif new.startswith("/"):
                    replace[old] = new.strip("/")
        return module, replace

    def _resolve_go(
        self, raw: str
    ) -> tuple[str | None, str | None, dict[str, Any] | None]:
        path = raw.strip().strip("'\"`")
        if not path or path == "C":
            return None, None, None
        if path.startswith(".") or path.startswith("/"):
            return None, None, None

        candidate_dirs: list[tuple[str, str, bool]] = []
        if self.go_module and (path == self.go_module or path.startswith(self.go_module + "/")):
            rel = path[len(self.go_module) :].strip("/")
            candidate_dirs.append((rel, "go_module_resolution", False))
        for old in sorted(self.go_replace, key=len, reverse=True):
            if path == old or path.startswith(old + "/"):
                base = self.go_replace[old]
                rest = path[len(old) :].strip("/")
                rel = to_posix_rel(Path(base) / rest) if rest else to_posix_rel(Path(base))
                candidate_dirs.append((rel, "go_replace_resolution", False))
                break
        candidate_dirs.append(("vendor/" + path.strip("/"), "go_vendor_resolution", True))

        for rel, strategy, vendored in candidate_dirs:
            info = self._go_package_dir(rel)
            if info is not None:
                info["vendored"] = vendored
                return None, strategy, info
        return None, None, None

    def _go_package_dir(self, rel: str) -> dict[str, Any] | None:
        rel = to_posix_rel(rel).strip("/")
        if rel in {"", "."}:
            files = [f for f in self.rel_files if f.endswith(".go") and "/" not in f]
            package = "."
        else:
            files = [f for f in self.rel_files if f.endswith(".go") and PurePosixPath(f).parent.as_posix() == rel]
            package = rel
            if not files:
                return None
        if not files:
            return None
        return {"package": package, "files": sorted(files)}

    # ---- Ruby ----
    def _resolve_ruby(self, source_file: str, raw: str, style: str) -> tuple[str | None, str | None]:
        raw = raw.strip()
        source_dir = Path(source_file).parent
        candidates: list[str] = []
        if style == "require_relative":
            base = _join_relative(source_dir, raw)
            candidates.append(base if base.endswith(".rb") else base + ".rb")
        else:
            candidates.append(raw if raw.endswith(".rb") else raw + ".rb")
            candidates.append(to_posix_rel(Path("lib") / (raw if raw.endswith(".rb") else raw + ".rb")))
            candidates.append(to_posix_rel(Path("app") / (raw if raw.endswith(".rb") else raw + ".rb")))

        for cand in candidates:
            cand = to_posix_rel(cand).lstrip("/")
            if cand in self.file_set:
                return cand, "ruby_require_resolution"
        return None, None

    # ---- HTML / CSS local asset and page links ----
    def _resolve_web_asset(self, source_file: str, raw: str) -> tuple[str | None, str | None]:
        cleaned = self._clean_web_reference(raw)
        if not cleaned:
            return None, None

        parsed = urlparse(cleaned)
        if parsed.scheme in {"http", "https", "mailto", "tel", "data", "javascript"}:
            return None, None
        if cleaned.startswith("#"):
            return None, None

        source_dir = Path(source_file).parent
        candidates: list[str] = []
        if cleaned.startswith("/"):
            base = cleaned.lstrip("/")
            candidates.extend(self._web_candidate_paths(base))
            candidates.extend(self._web_candidate_paths(to_posix_rel(Path("public") / base)))
            candidates.extend(self._web_candidate_paths(to_posix_rel(Path("src") / base)))
        else:
            base = _join_relative(source_dir, cleaned)
            candidates.extend(self._web_candidate_paths(base))

        for cand in candidates:
            cand = to_posix_rel(cand).lstrip("/")
            if cand in self.file_set:
                return cand, "web_relative_asset_resolution"
        return None, None

    def _clean_web_reference(self, raw: str) -> str:
        raw = (raw or "").strip().strip("'\"")
        if not raw:
            return ""
        raw, _fragment = urldefrag(raw)
        if "?" in raw:
            raw = raw.split("?", 1)[0]
        return raw.strip()

    def _web_candidate_paths(self, base: str) -> list[str]:
        base = to_posix_rel(base).lstrip("/")
        if not base:
            return []
        candidates = [base]
        if not Path(base).suffix:
            for ext in [".html", ".htm", ".css", ".js", ".jsx", ".ts", ".tsx", ".json"]:
                candidates.append(base + ext)
            candidates.append(to_posix_rel(Path(base) / "index.html"))
            candidates.append(to_posix_rel(Path(base) / "index.htm"))
        return candidates

    # ---- Fallback ----
    def _resolve_by_basename(self, raw: str) -> tuple[str | None, str | None]:
        stem = Path(raw.replace("\\", "/")).stem or raw.split(".")[-1]
        matches = self.by_stem.get(stem) or []
        if len(matches) == 1:
            return matches[0], "stem_fallback"
        return None, None
