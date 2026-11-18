"""HTML and CSS -> references, in the same shape as parse_py.

HTML: <script src>, <link href>, <img src>, <a href> and similar attributes.
CSS: @import and url(...). Uses tinycss2 when installed, a small scanner otherwise."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from typing import Any


# -----------------------------------------------------------------------------
# Optional CSS parser
# -----------------------------------------------------------------------------
try:
    import tinycss2  # type: ignore

    TINYCSS2_AVAILABLE = True
except Exception:
    tinycss2 = None  # type: ignore
    TINYCSS2_AVAILABLE = False


# -----------------------------------------------------------------------------
# HTML parser adapter
# -----------------------------------------------------------------------------
class _RefHTMLParser(HTMLParser):
    def __init__(self, rel_file: str) -> None:
        super().__init__(convert_charrefs=True)
        self.rel_file = rel_file
        self.imports: list[dict[str, Any]] = []
        self.entities: list[dict[str, Any]] = []
        self.role_hints: list[str] = ["html_page"]
        self._capture_tag: str | None = None
        self._capture_line: int | None = None
        self._capture_data: list[str] = []
        self._title_seen = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        line = int(self.getpos()[0])
        tag_l = tag.lower()
        attrs_dict = {str(k).lower(): (v or "") for k, v in attrs}

        if tag_l in {"title", "h1", "h2", "h3"}:
            self._capture_tag = tag_l
            self._capture_line = line
            self._capture_data = []

        if tag_l == "a" and attrs_dict.get("href"):
            self.imports.append(self._import(attrs_dict["href"], "html_anchor", line))
        elif tag_l == "script" and attrs_dict.get("src"):
            self.imports.append(self._import(attrs_dict["src"], "html_script_src", line))
            self.role_hints.append("has_script_asset")
        elif tag_l == "link" and attrs_dict.get("href"):
            rel = attrs_dict.get("rel", "").lower()
            style = "html_stylesheet_href" if "stylesheet" in rel else "html_link_href"
            self.imports.append(self._import(attrs_dict["href"], style, line))
            if "stylesheet" in rel:
                self.role_hints.append("has_css_asset")
        elif tag_l in {"img", "source", "video", "audio", "iframe"}:
            attr = "src" if attrs_dict.get("src") else "data-src"
            if attrs_dict.get(attr):
                self.imports.append(self._import(attrs_dict[attr], f"html_{tag_l}_{attr}", line))
        elif tag_l == "form":
            self.role_hints.append("has_form")
            action = attrs_dict.get("action", "")
            method = attrs_dict.get("method", "get").upper()
            self.entities.append(
                {
                    "name": action or "form_without_action",
                    "kind": "html_form",
                    "line_range": {"start_line": line, "end_line": line},
                    "method": method,
                    "exported": True,
                }
            )
            if action:
                self.imports.append(self._import(action, "html_form_action", line))
        elif tag_l == "meta":
            name = attrs_dict.get("name") or attrs_dict.get("property")
            content = attrs_dict.get("content")
            if name:
                self.entities.append(
                    {
                        "name": name,
                        "kind": "html_meta",
                        "line_range": {"start_line": line, "end_line": line},
                        "content_preview": (content or "")[:160],
                        "exported": True,
                    }
                )

    def handle_data(self, data: str) -> None:
        if self._capture_tag:
            clean = " ".join(data.split())
            if clean:
                self._capture_data.append(clean)

    def handle_endtag(self, tag: str) -> None:
        tag_l = tag.lower()
        if self._capture_tag and tag_l == self._capture_tag:
            text = " ".join(self._capture_data).strip()
            if text:
                kind = "html_title" if tag_l == "title" else f"html_heading_{tag_l}"
                self.entities.append(
                    {
                        "name": text[:180],
                        "kind": kind,
                        "line_range": {
                            "start_line": self._capture_line,
                            "end_line": int(self.getpos()[0]),
                        },
                        "exported": True,
                    }
                )
                if tag_l == "title":
                    self._title_seen = True
            self._capture_tag = None
            self._capture_line = None
            self._capture_data = []

    def _import(self, raw: str, style: str, line: int) -> dict[str, Any]:
        return {
            "raw": raw.strip(),
            "module": raw.strip(),
            "symbols": [],
            "import_style": style,
            "line": line,
        }


class HtmlAstAdapter:
    parser_name = "python_htmlparser"
    confidence = "high"

    def parse(self, rel_file: str, abs_file: Path, source_text: str) -> dict[str, Any]:
        parser = _RefHTMLParser(rel_file)
        parse_errors: list[str] = []
        try:
            parser.feed(source_text)
            parser.close()
        except Exception as exc:
            parse_errors.append(f"HTMLParseWarning: {exc}")

        # Always add the document as an entity so HTML-only folders are not empty.
        entities = [
            {
                "name": Path(rel_file).name,
                "kind": "html_document",
                "line_range": {"start_line": 1, "end_line": source_text.count("\n") + 1 if source_text else 1},
                "exported": True,
            }
        ] + parser.entities

        role_hints = parser.role_hints + self._path_role_hints(rel_file)
        return {
            "imports": self._dedupe_imports(parser.imports),
            "entities": self._dedupe_entities(entities),
            "role_hints": sorted(set(role_hints)),
            "parse_errors": parse_errors,
        }

    def _path_role_hints(self, rel_file: str) -> list[str]:
        p = rel_file.lower().replace("\\", "/")
        hints = []
        if "index." in p or p.endswith("/index.html"):
            hints.append("entry_or_index_page")
        if any(x in p for x in ["privacy", "terms", "refund", "contact"]):
            hints.append("policy_or_support_page")
        if any(x in p for x in ["insight", "blog", "article", "research"]):
            hints.append("content_or_insight_page")
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


# -----------------------------------------------------------------------------
# CSS parser adapter
# -----------------------------------------------------------------------------
class CssAstAdapter:
    def parse(self, rel_file: str, abs_file: Path, source_text: str) -> dict[str, Any]:
        if TINYCSS2_AVAILABLE:
            extracted = self._parse_with_tinycss2(rel_file, source_text)
            extracted["parser_used"] = "tinycss2"
            extracted["parser_confidence"] = "medium"
            return extracted

        extracted = self._parse_with_light_scanner(rel_file, source_text)
        extracted["parser_used"] = "css_light_scanner"
        extracted["parser_confidence"] = "low"
        extracted["parse_errors"].append("tinycss2 not installed; used conservative CSS light scanner. Install: pip install tinycss2")
        return extracted

    def _parse_with_tinycss2(self, rel_file: str, source_text: str) -> dict[str, Any]:
        imports: list[dict[str, Any]] = []
        entities: list[dict[str, Any]] = []
        parse_errors: list[str] = []
        try:
            rules = tinycss2.parse_stylesheet(source_text, skip_comments=True, skip_whitespace=True)  # type: ignore[union-attr]
            for rule in rules:
                line = int(getattr(rule, "source_line", 1) or 1)
                if getattr(rule, "type", "") == "at-rule":
                    keyword = str(getattr(rule, "at_keyword", ""))
                    prelude = getattr(rule, "prelude", []) or []
                    prelude_text = tinycss2.serialize(prelude).strip() if tinycss2 else ""  # type: ignore[union-attr]
                    entities.append(
                        {
                            "name": f"@{keyword} {prelude_text}"[:180],
                            "kind": "css_at_rule",
                            "line_range": {"start_line": line, "end_line": line},
                            "exported": True,
                        }
                    )
                    if keyword.lower() == "import":
                        target = self._first_css_url_or_string(prelude_text)
                        if target:
                            imports.append(self._import(target, "css_import", line))
                    for target in self._extract_urls_from_text(prelude_text):
                        imports.append(self._import(target, "css_url", line))
                elif getattr(rule, "type", "") == "qualified-rule":
                    selector = tinycss2.serialize(getattr(rule, "prelude", []) or []).strip() if tinycss2 else ""  # type: ignore[union-attr]
                    if selector:
                        entities.append(
                            {
                                "name": selector[:180],
                                "kind": "css_selector",
                                "line_range": {"start_line": line, "end_line": line},
                                "exported": True,
                            }
                        )
                    content_text = tinycss2.serialize(getattr(rule, "content", []) or []) if tinycss2 else ""  # type: ignore[union-attr]
                    for target in self._extract_urls_from_text(content_text):
                        imports.append(self._import(target, "css_url", line))
        except Exception as exc:
            parse_errors.append(f"TinyCSS2ParseWarning: {exc}")
            return self._parse_with_light_scanner(rel_file, source_text)

        return {
            "imports": self._dedupe_imports(imports),
            "entities": self._dedupe_entities(entities),
            "role_hints": sorted(set(["css_stylesheet"] + self._path_role_hints(rel_file))),
            "parse_errors": parse_errors,
        }

    def _parse_with_light_scanner(self, rel_file: str, source_text: str) -> dict[str, Any]:
        imports: list[dict[str, Any]] = []
        entities: list[dict[str, Any]] = [
            {
                "name": Path(rel_file).name,
                "kind": "css_stylesheet",
                "line_range": {"start_line": 1, "end_line": source_text.count("\n") + 1 if source_text else 1},
                "exported": True,
            }
        ]
        parse_errors: list[str] = []
        lines = source_text.splitlines()
        for idx, line_text in enumerate(lines, start=1):
            stripped = line_text.strip()
            if stripped.startswith("@import"):
                target = self._first_css_url_or_string(stripped)
                if target:
                    imports.append(self._import(target, "css_import", idx))
                entities.append(
                    {
                        "name": stripped[:180],
                        "kind": "css_at_rule",
                        "line_range": {"start_line": idx, "end_line": idx},
                        "exported": True,
                    }
                )
            for target in self._extract_urls_from_text(stripped):
                imports.append(self._import(target, "css_url", idx))
            if "{" in stripped and not stripped.startswith("@"):
                selector = stripped.split("{", 1)[0].strip()
                if selector:
                    entities.append(
                        {
                            "name": selector[:180],
                            "kind": "css_selector",
                            "line_range": {"start_line": idx, "end_line": idx},
                            "exported": True,
                        }
                    )
        return {
            "imports": self._dedupe_imports(imports),
            "entities": self._dedupe_entities(entities),
            "role_hints": sorted(set(["css_stylesheet"] + self._path_role_hints(rel_file))),
            "parse_errors": parse_errors,
        }

    def _first_css_url_or_string(self, text: str) -> str | None:
        urls = self._extract_urls_from_text(text)
        if urls:
            return urls[0]
        for quote in ["'", '"']:
            start = text.find(quote)
            if start >= 0:
                end = text.find(quote, start + 1)
                if end > start:
                    return text[start + 1 : end].strip()
        return None

    def _extract_urls_from_text(self, text: str) -> list[str]:
        out: list[str] = []
        idx = 0
        lowered = text.lower()
        while True:
            start = lowered.find("url(", idx)
            if start < 0:
                break
            content_start = start + 4
            end = text.find(")", content_start)
            if end < 0:
                break
            value = text[content_start:end].strip().strip("'\"")
            if value and value not in out:
                out.append(value)
            idx = end + 1
        return out

    def _import(self, raw: str, style: str, line: int) -> dict[str, Any]:
        return {
            "raw": raw.strip(),
            "module": raw.strip(),
            "symbols": [],
            "import_style": style,
            "line": line,
        }

    def _path_role_hints(self, rel_file: str) -> list[str]:
        p = rel_file.lower().replace("\\", "/")
        hints = []
        if any(x in p for x in ["global", "globals", "base", "reset"]):
            hints.append("global_css")
        if any(x in p for x in ["theme", "tailwind"]):
            hints.append("theme_or_design_css")
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
