"""Files -> code chunks and the relationships between them.

BoundaryChunker cuts each file at entity boundaries (functions, classes):
small files stay whole, oversized entities are split into overlapping
segments. ChunkGraphBuilder turns the resolved graph's edges into
chunk -> chunk edges. Chunk ids come from _stable_id(content position), so
they are identical on every run."""
from __future__ import annotations

import hashlib
import math
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from collections.abc import Callable, Iterable, Mapping, Sequence

from .config import Config
from .util import _posix


FILE_PRELUDE_LIMIT = 300


def _stable_id(*parts: Any, length: int = 16) -> str:
    text = "|".join(str(part or "") for part in parts)
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()[:length]


class TokenCounter:
    """Use tiktoken when installed; otherwise use a deterministic code estimate."""

    def __init__(self, encoding_name: str = "cl100k_base") -> None:
        self.encoding_name = encoding_name
        self.backend = "approx_chars_div_4"
        self._encoding = None
        self._cache: dict[str, int] = {}
        try:
            import tiktoken  # type: ignore

            self._encoding = tiktoken.get_encoding(encoding_name)
            self.backend = f"tiktoken:{encoding_name}"
        except Exception:
            self._encoding = None

    def count(self, text: str) -> int:
        digest = hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()
        cached = self._cache.get(digest)
        if cached is not None:
            return cached
        if not text:
            count = 0
        elif self._encoding is not None:
            count = len(self._encoding.encode(text, disallowed_special=()))
        else:
            # Code contains more punctuation than prose. chars/4 is a useful,
            # conservative-enough fallback without introducing a dependency.
            count = max(1, math.ceil(len(text) / 4))
        self._cache[digest] = count
        return count

    def truncate(self, text: str, max_tokens: int) -> str:
        if max_tokens <= 0 or not text:
            return ""
        if self.count(text) <= max_tokens:
            return text
        if self._encoding is not None:
            tokens = self._encoding.encode(text, disallowed_special=())[:max_tokens]
            return self._encoding.decode(tokens)
        return text[: max_tokens * 4]


class FastContextTokenCounter:
    """Fast, deterministic and conservative token estimate for code downloads."""

    def __init__(self, encoding_name: str = "cl100k_base") -> None:
        self.encoding_name = encoding_name
        self.backend = "fast_conservative_code_estimate"

    def count(self, text: str) -> int:
        if not text:
            return 0
        return max(1, math.ceil(len(text) / 3.2))

    def truncate(self, text: str, max_tokens: int) -> str:
        if max_tokens <= 0 or not text:
            return ""
        return text[: int(max_tokens * 3.2)]


@dataclass
class CodeChunk:
    chunk_id: str
    file: str
    language: str
    start_line: int
    end_line: int
    kind: str
    entity: str | None
    qualified_name: str | None
    parent_entity_id: str | None
    tokens: int
    code: str
    file_prelude: str
    role_hints: list[str] = field(default_factory=list)

    def as_feed_dict(self) -> dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "file": self.file,
            "language": self.language,
            "line_range": {"start_line": self.start_line, "end_line": self.end_line},
            "kind": self.kind,
            "entity": self.entity,
            "qualified_name": self.qualified_name,
            "parent_entity_id": self.parent_entity_id,
            "estimated_tokens": self.tokens,
            "numbered_code": self.code,
            "role_hints": self.role_hints,
        }


@dataclass(frozen=True)
class ChunkEdge:
    source: str
    target: str
    weight: float
    relationship: str
    confidence: str
    symbol: str | None = None
    uncertain: bool = False


class BoundaryChunker:
    def __init__(
        self,
        repo_root: Path,
        graph: Mapping[str, Any],
        counter: TokenCounter,
        *,
        whole_file_limit: int = Config.whole_file_limit,
        max_entity_tokens: int = Config.max_entity_tokens,
        segment_tokens: int = Config.segment_tokens,
        overlap_tokens: int = Config.overlap_tokens,
        prelude_limit: int = FILE_PRELUDE_LIMIT,
        tiny_context_tokens: int = Config.tiny_context_tokens,
        on_progress: Callable[..., None] | None = None,
    ) -> None:
        self.on_progress = on_progress or (lambda *_: None)
        self.repo_root = repo_root.resolve()
        self.graph = graph
        self.counter = counter
        self.whole_file_limit = max(200, whole_file_limit)
        self.max_entity_tokens = max(300, max_entity_tokens)
        self.segment_tokens = max(200, segment_tokens)
        self.overlap_tokens = max(0, min(overlap_tokens, self.segment_tokens // 3))
        self.prelude_limit = max(0, prelude_limit)
        self.tiny_context_tokens = max(0, tiny_context_tokens)
        self.skipped_files: list[dict[str, Any]] = []

    def build(self) -> list[CodeChunk]:
        chunks: list[CodeChunk] = []
        nodes = self.graph.get("nodes", []) or []
        done = 0
        for node in nodes:
            if not isinstance(node, dict) or not node.get("file"):
                continue
            chunks.extend(self._chunk_file(node))
            done += 1
            self.on_progress("chunk", done, len(nodes))
        return sorted(chunks, key=lambda c: (c.file, c.start_line, c.end_line, c.chunk_id))

    def _chunk_file(self, node: Mapping[str, Any]) -> list[CodeChunk]:
        """Small file -> one whole_file chunk. Larger file -> one chunk per outermost
        entity plus the file context between them; oversized pieces are split."""
        relative_file = _posix(node.get("file")).lstrip("/")
        text = self._read_source(relative_file)
        if not text or not text.strip():
            return []
        lines = text.splitlines()
        language = str(node.get("language") or "unknown")
        role_hints = sorted({str(v) for v in node.get("role_hints", []) or []})
        prelude = self._build_prelude(lines, node.get("imports", []) or [])

        def chunk(start, end, kind, entity, qualified_name):
            return self._make_chunk(
                relative_file, language, lines, start, end,
                kind=kind, entity=entity, qualified_name=qualified_name,
                parent_entity_id=None, prelude=prelude, role_hints=role_hints,
            )

        if self.counter.count(text) <= self.whole_file_limit:
            return [chunk(1, len(lines), "whole_file", None, None)]

        chunks: list[CodeChunk] = []
        for start, end, kind, entity, qualified_name in self._pieces(node, lines, language):
            raw = "\n".join(lines[start - 1 : end])
            if not raw.strip():
                continue
            if self.counter.count(raw) <= self.max_entity_tokens:
                chunks.append(chunk(start, end, kind, entity, qualified_name))
                continue
            parent_id = f"entity_{_stable_id(relative_file, qualified_name or entity or kind, start, end)}"
            chunks.extend(
                self._split_large_range(
                    relative_file, language, lines, start, end, kind, entity, qualified_name, parent_id, prelude, role_hints
                )
            )
        return chunks

    def _read_source(self, relative_file: str) -> str | None:
        """The file's text, or None (recorded in skipped_files) if it cannot be read."""
        source_path = (self.repo_root / relative_file).resolve()
        try:
            source_path.relative_to(self.repo_root)
        except ValueError:
            self.skipped_files.append({"file": relative_file, "reason": "path_outside_repository"})
            return None
        if not source_path.is_file():
            self.skipped_files.append({"file": relative_file, "reason": "source_file_missing"})
            return None
        try:
            return source_path.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            self.skipped_files.append({"file": relative_file, "reason": f"read_error: {exc}"})
            return None

    def _pieces(self, node: Mapping[str, Any], lines: list[str], language: str):
        """(start, end, kind, entity, qualified_name) covering every line: outermost
        entities in order, with the lines between them as file_context."""
        pieces: list[tuple[int, int, str, str | None, str | None]] = []
        cursor = 1
        for start, end, kind, entity, qualified_name in self._outermost_entity_intervals(
            node.get("entities", []) or [], lines, language
        ):
            if cursor < start:
                pieces.append((cursor, start - 1, "file_context", None, None))
            pieces.append((start, end, kind or "entity", entity, qualified_name))
            cursor = max(cursor, end + 1)
        if cursor <= len(lines):
            pieces.append((cursor, len(lines), "file_context", None, None))
        if not pieces:
            pieces = [(1, len(lines), "file_context", None, None)]
        return self._merge_tiny_context_pieces(pieces, lines)

    def _outermost_entity_intervals(
        self,
        entities: Sequence[Mapping[str, Any]],
        lines: Sequence[str],
        language: str,
    ) -> list[tuple[int, int, str, str | None, str | None]]:
        candidates: list[tuple[int, int, str, str | None, str | None]] = []
        for entity in entities:
            if not isinstance(entity, Mapping):
                continue
            if entity.get("kind") == "constant":
                continue
            # Python enrichment explicitly identifies module-owned entities.
            # Nested methods/functions remain inside the outer class/function.
            scope = entity.get("scope")
            if scope in {"class", "function"} or entity.get("importable") is False:
                continue
            line_range = entity.get("line_range") or {}
            try:
                start = int(line_range.get("start_line") or entity.get("start_line") or 0)
                end = int(line_range.get("end_line") or entity.get("end_line") or start)
            except (TypeError, ValueError):
                continue
            line_count = len(lines)
            if start < 1 or end < start or start > line_count:
                continue
            start = self._expand_leading_metadata(lines, start, language)
            end = min(end, line_count)
            candidates.append(
                (
                    start,
                    end,
                    str(entity.get("kind") or "entity"),
                    str(entity.get("name") or entity.get("entity_name") or "") or None,
                    str(entity.get("qualified_name") or entity.get("name") or "") or None,
                )
            )
        candidates.sort(key=lambda item: (item[0], -item[1], item[2], item[3] or ""))

        selected: list[tuple[int, int, str, str | None, str | None]] = []
        for candidate in candidates:
            start, end = candidate[0], candidate[1]
            if any(existing[0] <= start and end <= existing[1] for existing in selected):
                continue
            if selected and start <= selected[-1][1]:
                # Overlapping but neither containing the other is parser noise.
                # Keep the earlier, larger interval to avoid duplicated code.
                continue
            selected.append(candidate)
        return selected

    def _expand_leading_metadata(self, lines: Sequence[str], start: int, language: str) -> int:
        """Include decorators/attributes immediately associated with an entity.

        Supports Python and JS/TS ``@decorator`` blocks plus Rust ``#[...]``
        attributes and ``///`` documentation. The scan is deliberately bounded
        and stops at a blank line, so unrelated preceding code is not absorbed.
        """

        if start <= 1:
            return start
        language = language.lower()
        marker_prefixes: tuple[str, ...]
        doc_prefixes: tuple[str, ...]
        if language in {"python", "javascript", "jsx", "typescript", "tsx"}:
            marker_prefixes = ("@",)
            doc_prefixes = ("//", "/**", "*", "*/") if language != "python" else ("#",)
        elif language == "rust":
            marker_prefixes = ("#[", "#![")
            doc_prefixes = ("///", "//!", "//")
        else:
            return start

        lower_bound = max(0, start - 41)
        block_start = start - 1
        for index in range(start - 2, lower_bound - 1, -1):
            if not lines[index].strip():
                break
            block_start = index
        marker_indices = [
            index
            for index in range(block_start, start - 1)
            if lines[index].strip().startswith(marker_prefixes)
        ]
        if not marker_indices:
            return start
        metadata_start = marker_indices[0]
        while metadata_start > block_start:
            previous = lines[metadata_start - 1].strip()
            if previous.startswith(doc_prefixes):
                metadata_start -= 1
            else:
                break
        return metadata_start + 1

    def _merge_tiny_context_pieces(
        self,
        pieces: Sequence[tuple[int, int, str, str | None, str | None]],
        lines: Sequence[str],
    ) -> list[tuple[int, int, str, str | None, str | None]]:
        if not self.tiny_context_tokens or len(pieces) < 2:
            return list(pieces)
        mutable = [list(piece) for piece in pieces]
        index = 0
        while index < len(mutable):
            start, end, kind, _entity, _qualified = mutable[index]
            if kind != "file_context":
                index += 1
                continue
            raw = "\n".join(lines[int(start) - 1 : int(end)])
            if self.counter.count(raw) > self.tiny_context_tokens:
                index += 1
                continue
            if index + 1 < len(mutable):
                # Leading comments, attributes and small setup fragments usually
                # explain the following entity.
                mutable[index + 1][0] = start
            elif index > 0:
                mutable[index - 1][1] = end
            else:
                index += 1
                continue
            mutable.pop(index)
        return [tuple(piece) for piece in mutable]  # type: ignore[return-value]

    def _split_large_range(
        self,
        relative_file: str,
        language: str,
        lines: Sequence[str],
        start: int,
        end: int,
        kind: str,
        entity: str | None,
        qualified_name: str | None,
        parent_id: str,
        prelude: str,
        role_hints: list[str],
    ) -> list[CodeChunk]:
        chunks: list[CodeChunk] = []
        current = start
        while current <= end:
            physical_line = lines[current - 1]
            numbered_line = f"{current:>6} | {physical_line}"
            if self.counter.count(numbered_line) > self.segment_tokens:
                for fragment_index, fragment in enumerate(
                    self._split_oversized_physical_line(current, physical_line),
                    start=1,
                ):
                    numbered = f"{current:>6} | {fragment}"
                    chunks.append(
                        CodeChunk(
                            chunk_id=(
                                f"chunk_{_stable_id(relative_file, current, qualified_name or entity or kind, 'line_fragment', fragment_index)}"
                            ),
                            file=relative_file,
                            language=language,
                            start_line=current,
                            end_line=current,
                            kind=f"{kind}_line_fragment_{fragment_index}",
                            entity=entity,
                            qualified_name=qualified_name,
                            parent_entity_id=parent_id,
                            tokens=self.counter.count(numbered),
                            code=numbered,
                            file_prelude=prelude,
                            role_hints=role_hints,
                        )
                    )
                current += 1
                continue
            segment_end = current
            segment_parts: list[str] = []
            while segment_end <= end:
                candidate_parts = [*segment_parts, lines[segment_end - 1]]
                if segment_parts and self.counter.count("\n".join(candidate_parts)) > self.segment_tokens:
                    break
                segment_parts = candidate_parts
                segment_end += 1
            actual_end = max(current, segment_end - 1)
            chunks.append(
                self._make_chunk(
                    relative_file,
                    language,
                    lines,
                    current,
                    actual_end,
                    kind=f"{kind}_segment",
                    entity=entity,
                    qualified_name=qualified_name,
                    parent_entity_id=parent_id,
                    prelude=prelude,
                    role_hints=role_hints,
                )
            )
            if actual_end >= end:
                break
            next_start = actual_end + 1
            if self.overlap_tokens:
                overlap_start = actual_end
                overlap_parts: list[str] = []
                while overlap_start >= current:
                    candidate = [lines[overlap_start - 1], *overlap_parts]
                    if overlap_parts and self.counter.count("\n".join(candidate)) > self.overlap_tokens:
                        break
                    overlap_parts = candidate
                    overlap_start -= 1
                next_start = max(current + 1, overlap_start + 1)
            current = next_start
        return chunks

    def _split_oversized_physical_line(self, line_number: int, line: str) -> list[str]:
        """Split a giant line at tokenizer-measured character boundaries."""

        fragments: list[str] = []
        cursor = 0
        while cursor < len(line):
            low, high, best = cursor + 1, len(line), cursor
            while low <= high:
                middle = (low + high) // 2
                candidate = f"{line_number:>6} | {line[cursor:middle]}"
                if self.counter.count(candidate) <= self.segment_tokens:
                    best = middle
                    low = middle + 1
                else:
                    high = middle - 1
            if best == cursor:
                best = cursor + 1
            fragments.append(line[cursor:best])
            cursor = best
        return fragments

    def _make_chunk(
        self,
        relative_file: str,
        language: str,
        lines: Sequence[str],
        start: int,
        end: int,
        *,
        kind: str,
        entity: str | None,
        qualified_name: str | None,
        parent_entity_id: str | None,
        prelude: str,
        role_hints: list[str],
    ) -> CodeChunk:
        selected = list(lines[start - 1 : end])
        numbered = "\n".join(f"{line_no:>6} | {line}" for line_no, line in enumerate(selected, start=start))
        tokens = self.counter.count(numbered)
        chunk_id = f"chunk_{_stable_id(relative_file, start, end, qualified_name or entity or kind)}"
        return CodeChunk(
            chunk_id=chunk_id,
            file=relative_file,
            language=language,
            start_line=start,
            end_line=end,
            kind=kind,
            entity=entity,
            qualified_name=qualified_name,
            parent_entity_id=parent_entity_id,
            tokens=tokens,
            code=numbered,
            file_prelude=prelude,
            role_hints=role_hints,
        )

    def _build_prelude(self, lines: Sequence[str], imports: Sequence[Mapping[str, Any]]) -> str:
        import_lines = sorted(
            {
                int(item.get("line"))
                for item in imports
                if isinstance(item, Mapping) and str(item.get("line") or "").isdigit()
            }
        )
        snippets = [lines[line - 1] for line in import_lines if 1 <= line <= len(lines)]
        return self.counter.truncate("\n".join(snippets), self.prelude_limit)


class ChunkGraphBuilder:
    def __init__(self, graph: Mapping[str, Any], chunks: Sequence[CodeChunk]) -> None:
        self.graph = graph
        self.chunks = list(chunks)
        self.chunk_by_id = {chunk.chunk_id: chunk for chunk in chunks}
        self.chunks_by_file: defaultdict[str, list[CodeChunk]] = defaultdict(list)
        for chunk in chunks:
            self.chunks_by_file[chunk.file].append(chunk)
        for values in self.chunks_by_file.values():
            values.sort(key=lambda c: (c.start_line, c.end_line, c.chunk_id))

    def build(self) -> list[ChunkEdge]:
        edges: list[ChunkEdge] = []
        edges.extend(self._same_file_edges())
        edges.extend(self._symbol_edges())
        edges.extend(self._file_import_edges())
        return self._dedupe_edges(edges)

    def _same_file_edges(self) -> list[ChunkEdge]:
        edges: list[ChunkEdge] = []
        for chunks in self.chunks_by_file.values():
            for left, right in zip(chunks, chunks[1:]):
                same_parent = bool(left.parent_entity_id and left.parent_entity_id == right.parent_entity_id)
                edges.append(
                    ChunkEdge(
                        source=left.chunk_id,
                        target=right.chunk_id,
                        weight=10.0 if same_parent else 3.0,
                        relationship="same_entity_segment" if same_parent else "same_file",
                        confidence="high",
                    )
                )
        return edges

    def _symbol_edges(self) -> list[ChunkEdge]:
        edges: list[ChunkEdge] = []
        symbol_index = self.graph.get("global_symbol_index", {}) or {}
        for edge in self.graph.get("symbol_edges", []) or []:
            if not isinstance(edge, Mapping):
                continue
            if edge.get("is_uncertain"):
                weight = 0.5
            else:
                weight = 5.0
            source_file = _posix(edge.get("source"))
            target_file = _posix(edge.get("target"))
            source_chunk = self._chunk_at_line(source_file, edge.get("line")) or self._representative(source_file)
            target_line = self._symbol_definition_line(
                symbol_index,
                edge.get("symbol"),
                target_file,
                edge.get("owner"),
            )
            target_chunk = self._chunk_at_line(target_file, target_line) or self._representative(target_file)
            if source_chunk and target_chunk and source_chunk.chunk_id != target_chunk.chunk_id:
                edges.append(
                    ChunkEdge(
                        source=source_chunk.chunk_id,
                        target=target_chunk.chunk_id,
                        weight=weight,
                        relationship=str(edge.get("type") or "imports_symbol"),
                        confidence=str(edge.get("confidence") or "none"),
                        symbol=str(edge.get("symbol")) if edge.get("symbol") else None,
                        uncertain=bool(edge.get("is_uncertain")),
                    )
                )
        return edges

    def _file_import_edges(self) -> list[ChunkEdge]:
        edges: list[ChunkEdge] = []
        for edge in self.graph.get("edges", []) or []:
            # Go call edges also sit in "edges"; _symbol_edges() already links them.
            if not isinstance(edge, Mapping) or edge.get("type") != "imports":
                continue
            source_file = _posix(edge.get("source"))
            target_file = _posix(edge.get("target"))
            source_chunk = self._chunk_at_line(source_file, edge.get("line")) or self._representative(source_file)
            target_chunk = self._representative(target_file)
            if source_chunk and target_chunk and source_chunk.chunk_id != target_chunk.chunk_id:
                edges.append(
                    ChunkEdge(
                        source=source_chunk.chunk_id,
                        target=target_chunk.chunk_id,
                        weight=2.0,
                        relationship="file_import",
                        confidence=str(edge.get("confidence") or "medium"),
                    )
                )
        return edges

    def _chunk_at_line(self, file_path: str, line: Any) -> CodeChunk | None:
        try:
            line_number = int(line or 0)
        except (TypeError, ValueError):
            return None
        matches = [
            chunk
            for chunk in self.chunks_by_file.get(file_path, [])
            if chunk.start_line <= line_number <= chunk.end_line
        ]
        if not matches:
            return None
        return min(matches, key=lambda c: (c.end_line - c.start_line, c.start_line, c.chunk_id))

    def _representative(self, file_path: str) -> CodeChunk | None:
        chunks = self.chunks_by_file.get(file_path, [])
        return chunks[0] if chunks else None

    @staticmethod
    def _symbol_definition_line(
        symbol_index: Mapping[str, Any],
        symbol: Any,
        target_file: str,
        owner: Any = None,
    ) -> int | None:
        definitions = symbol_index.get(str(symbol or ""), []) or []
        if owner:
            for definition in definitions:
                if _posix(definition.get("source_file")) != target_file:
                    continue
                if str(definition.get("owner") or "") != str(owner):
                    continue
                line_range = definition.get("line_range") or {}
                try:
                    return int(line_range.get("start_line") or 0) or None
                except (TypeError, ValueError):
                    return None
        for definition in definitions:
            if _posix(definition.get("source_file")) != target_file:
                continue
            line_range = definition.get("line_range") or {}
            try:
                return int(line_range.get("start_line") or 0) or None
            except (TypeError, ValueError):
                return None
        return None

    @staticmethod
    def _dedupe_edges(edges: Iterable[ChunkEdge]) -> list[ChunkEdge]:
        strongest: dict[tuple[str, str, str, str | None], ChunkEdge] = {}
        for edge in edges:
            key = (edge.source, edge.target, edge.relationship, edge.symbol)
            existing = strongest.get(key)
            if existing is None or edge.weight > existing.weight:
                strongest[key] = edge
        return sorted(strongest.values(), key=lambda e: (e.source, e.target, -e.weight, e.relationship))
