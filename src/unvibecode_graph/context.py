"""ContextBuilder: resolved graph -> per-file connected-code downloads.

For every file it prepares three selections under Config's token limits:
radius 0 (the file itself), 1 (plus files one connection away) and 2
(plus files two connections away). Writes fast_lane_context_store.json, the same data as .js for
the browser, and the complete-repository ZIP. No LLM calls."""
from __future__ import annotations

import json
import time
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from collections.abc import Callable, Mapping, Sequence

from .config import Config
from .chunk import BoundaryChunker, ChunkEdge, ChunkGraphBuilder, CodeChunk, FastContextTokenCounter, TokenCounter


class ContextBuilder:
    """Prepare compact graph-radius selections without creating LLM batches."""

    def __init__(
        self,
        repo_root: Path,
        resolved_graph: Mapping[str, Any],
        cfg: Config = Config(),
        on_progress: Callable[..., None] | None = None,
    ) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.graph = dict(resolved_graph)
        self.cfg = cfg
        self.on_progress = on_progress or (lambda *_: None)
        if cfg.token_mode == "fast":
            self.counter = FastContextTokenCounter(cfg.encoding_name)
        elif cfg.token_mode == "exact":
            self.counter = TokenCounter(cfg.encoding_name)
        else:
            raise ValueError("Config.token_mode must be 'fast' or 'exact'.")
        self.chunks: list[CodeChunk] = []
        self.chunk_by_id: dict[str, CodeChunk] = {}
        self.chunks_by_file: defaultdict[str, list[CodeChunk]] = defaultdict(list)
        self.chunks_by_parent: defaultdict[str, list[CodeChunk]] = defaultdict(list)
        self.verified_edges: list[ChunkEdge] = []
        self.file_neighbors: defaultdict[str, set[str]] = defaultdict(set)
        self.cross_edges_by_file: defaultdict[str, list[ChunkEdge]] = defaultdict(list)
        self._file_hops_cache: dict[tuple[str, int], dict[str, int]] = {}
        self._core_order_cache: dict[str, list[str]] = {}

    def build(
        self,
        output_path: Path,
        *,
        json_output_path: Path | None = None,
        bundle_output_path: Path | None = None,
    ) -> dict[str, Any]:
        """Chunk, connect, select, then write the store (.js, .json) and the ZIP."""
        timer = time.monotonic()
        lap = lambda: round(time.monotonic() - timer, 3)  # noqa: E731
        skipped_files = self._chunk()
        chunk_seconds = lap()

        timer = time.monotonic()
        self._connect()
        connection_seconds = lap()

        timer = time.monotonic()
        file_records: dict[str, Any] = {}
        for done, (file_path, chunks) in enumerate(sorted(self.chunks_by_file.items()), 1):
            file_records[file_path] = {
                "file": file_path,
                "source_tokens": sum(chunk.tokens for chunk in chunks),
                "scopes": {str(radius): self._selection(file_path, radius) for radius in (0, 1, 2)},
            }
            self.on_progress("select", done, len(self.chunks_by_file))
        selection_seconds = lap()
        relationships = self._relationships()

        timer = time.monotonic()
        self._write_store(output_path, json_output_path, file_records, relationships)
        serialization_seconds = lap()

        bundle_seconds = 0.0
        if bundle_output_path is not None:
            timer = time.monotonic()
            self._write_repository_bundle(
                bundle_output_path,
                file_records=file_records,
                relationships=relationships,
                skipped_files=skipped_files,
            )
            bundle_seconds = lap()

        return {
            "context_store_js": str(output_path),
            "context_store_json": str(json_output_path) if json_output_path else None,
            "complete_repository_bundle": (
                str(bundle_output_path) if bundle_output_path else None
            ),
            "source_files": len(file_records),
            "atomic_code_sections": len(self.chunks),
            "verified_cross_file_connections": len(relationships),
            "store_bytes": output_path.stat().st_size,
            "tokenizer": self.counter.backend,
            "skipped_files": skipped_files,
            "preparation_seconds": {
                "code_sections": chunk_seconds,
                "connections": connection_seconds,
                "download_selections": selection_seconds,
                "browser_store": serialization_seconds,
                "zip_bundle": bundle_seconds,
            },
        }

    def _chunk(self) -> list[dict[str, Any]]:
        """Cut every file into chunks and index them by id, file and parent entity.
        Returns the files the chunker had to skip."""
        chunker = BoundaryChunker(
            self.repo_root,
            self.graph,
            self.counter,
            whole_file_limit=self.cfg.whole_file_limit,
            max_entity_tokens=self.cfg.max_entity_tokens,
            segment_tokens=self.cfg.segment_tokens,
            overlap_tokens=self.cfg.overlap_tokens,
            tiny_context_tokens=self.cfg.tiny_context_tokens,
            on_progress=self.on_progress,
        )
        self.chunks = chunker.build()
        self.on_progress("chunked", len(self.chunks), len(self.chunks))
        if not self.chunks:
            raise ValueError("No source code sections were available for context downloads.")
        self.chunk_by_id = {chunk.chunk_id: chunk for chunk in self.chunks}
        for chunk in self.chunks:
            self.chunks_by_file[chunk.file].append(chunk)
            if chunk.parent_entity_id:
                self.chunks_by_parent[chunk.parent_entity_id].append(chunk)
        for values in self.chunks_by_file.values():
            values.sort(key=self._chunk_sort_key)
        for values in self.chunks_by_parent.values():
            values.sort(key=self._chunk_sort_key)
        return chunker.skipped_files

    def _connect(self) -> None:
        """Keep certain (high/medium, not uncertain) chunk edges; index cross-file ones by file."""
        all_edges = ChunkGraphBuilder(self.graph, self.chunks).build()
        self.on_progress("connect", len(all_edges), len(all_edges))
        self.verified_edges = [
            edge
            for edge in all_edges
            if edge.source in self.chunk_by_id
            and edge.target in self.chunk_by_id
            and not edge.uncertain
            and str(edge.confidence).lower() in {"high", "medium"}
        ]
        for edge in self.verified_edges:
            source = self.chunk_by_id[edge.source]
            target = self.chunk_by_id[edge.target]
            if source.file == target.file:
                continue
            self.file_neighbors[source.file].add(target.file)
            self.file_neighbors[target.file].add(source.file)
            self.cross_edges_by_file[source.file].append(edge)
            self.cross_edges_by_file[target.file].append(edge)

    def _relationships(self) -> list[dict[str, Any]]:
        relationships = []
        for edge in self.verified_edges:
            source = self.chunk_by_id[edge.source]
            target = self.chunk_by_id[edge.target]
            if source.file == target.file:
                continue
            relationships.append(
                {
                    "source_chunk": edge.source,
                    "source_file": source.file,
                    "source_line": source.start_line,
                    "relationship": edge.relationship,
                    "symbol": edge.symbol,
                    "target_chunk": edge.target,
                    "target_file": target.file,
                    "target_line": target.start_line,
                    "confidence": edge.confidence,
                }
            )
        return relationships

    def _write_store(self, output_path: Path, json_output_path: Path | None, file_records, relationships) -> None:
        """Source code is stored once and reused by every graph click."""
        store = {
            "schema_version": "shipreadyv2.fast_lane_context_store.v1",
            "repository": self.graph.get("repo_name"),
            "tokenizer": self.counter.backend,
            "settings": {
                "focused_maximum_tokens": self.cfg.focused_max_tokens,
                "direct_target_tokens": self.cfg.direct_target_tokens,
                "direct_maximum_tokens": self.cfg.direct_max_tokens,
                "extended_target_tokens": self.cfg.extended_target_tokens,
                "extended_maximum_tokens": self.cfg.extended_max_tokens,
            },
            "files": file_records,
            "chunks": {chunk.chunk_id: chunk.as_feed_dict() for chunk in self.chunks},
            "verified_cross_file_connections": relationships,
        }
        serialized_store = json.dumps(store, ensure_ascii=True, separators=(",", ":"))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("window.SHIPREADY_CONTEXT_STORE=" + serialized_store + ";\n", encoding="utf-8", newline="\n")
        if json_output_path is not None:
            json_output_path.parent.mkdir(parents=True, exist_ok=True)
            json_output_path.write_text(serialized_store + "\n", encoding="utf-8", newline="\n")

    def _write_repository_bundle(
        self,
        output_path: Path,
        *,
        file_records: Mapping[str, Any],
        relationships: Sequence[Mapping[str, Any]],
        skipped_files: Sequence[Mapping[str, Any]],
    ) -> None:
        """Write one normalized, provider-neutral bundle for API automation."""

        manifest = {
            "schema_version": "shipreadyv2.repository_context_bundle.v1",
            "repository": self.graph.get("repo_name"),
            "tokenizer": self.counter.backend,
            "source_files": len(file_records),
            "atomic_code_sections": len(self.chunks),
            "verified_cross_file_connections": len(relationships),
            "skipped_files": list(skipped_files),
            "contents": {
                "chunks.jsonl": "One self-contained source-code section per line.",
                "connections.jsonl": "Verified connections between code sections.",
                "selections.jsonl": "Precomputed narrow, optimal and wider selections per file.",
                "README.md": "Usage guidance for batch or API analysis.",
            },
        }
        readme = """# ShipReady complete repository context

This ZIP is a normalized context store for later analysis or API automation.

- `chunks.jsonl` contains each source-code section exactly once.
- `connections.jsonl` contains verified cross-file links.
- `selections.jsonl` maps each source file to precomputed narrow, optimal and wider connected contexts.
- Join a selection's `chunk_ids` to `chunks.jsonl` before sending one context to an LLM.

Do not send this entire ZIP as one LLM request. Process one selected context at a time and cite the original file and line fields.
"""
        chunk_lines = "".join(
            json.dumps(chunk.as_feed_dict(), ensure_ascii=True, separators=(",", ":"))
            + "\n"
            for chunk in self.chunks
        )
        connection_lines = "".join(
            json.dumps(item, ensure_ascii=True, separators=(",", ":")) + "\n"
            for item in relationships
        )
        selection_lines = "".join(
            json.dumps(record, ensure_ascii=True, separators=(",", ":")) + "\n"
            for _file_path, record in sorted(file_records.items())
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(
            output_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6
        ) as archive:
            archive.writestr(
                "manifest.json",
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            )
            archive.writestr("chunks.jsonl", chunk_lines)
            archive.writestr("connections.jsonl", connection_lines)
            archive.writestr("selections.jsonl", selection_lines)
            diagnostics = list(self.graph.get("unresolved_linker_imports", []) or [])
            diagnostics += list(self.graph.get("unresolved_imports", []) or [])
            diagnostics += list(self.graph.get("unresolved_go_usages", []) or [])
            diagnostics += [edge for edge in self.graph.get("symbol_edges", []) or []
                            if edge.get("is_uncertain") or str(edge.get("confidence", "none")).lower() not in {"high", "medium"}]
            archive.writestr("unresolved_relationships.jsonl", "".join(
                json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in diagnostics))
            archive.writestr("README.md", readme)

    @staticmethod
    def _chunk_sort_key(chunk: CodeChunk) -> tuple[Any, ...]:
        return (chunk.start_line, chunk.end_line, chunk.chunk_id)

    def _file_hops(self, center: str, radius: int) -> dict[str, int]:
        cache_key = (center, radius)
        cached = self._file_hops_cache.get(cache_key)
        if cached is not None:
            return cached
        hops = {center: 0}
        frontier = [center]
        while frontier:
            current = frontier.pop(0)
            if hops[current] >= radius:
                continue
            for neighbor in sorted(self.file_neighbors.get(current, set())):
                if neighbor not in hops:
                    hops[neighbor] = hops[current] + 1
                    frontier.append(neighbor)
        self._file_hops_cache[cache_key] = hops
        return hops

    def _core_order(self, center: str) -> list[str]:
        cached = self._core_order_cache.get(center)
        if cached is not None:
            return cached
        weight: Counter[str] = Counter()
        for edge in self.cross_edges_by_file.get(center, []):
            source = self.chunk_by_id[edge.source]
            target = self.chunk_by_id[edge.target]
            if source.file == center and target.file != center:
                weight[edge.source] += edge.weight
            if target.file == center and source.file != center:
                weight[edge.target] += edge.weight
        ordered = [
            chunk.chunk_id
            for chunk in sorted(
                self.chunks_by_file[center],
                key=lambda chunk: (-weight[chunk.chunk_id], self._chunk_sort_key(chunk)),
            )
        ]
        self._core_order_cache[center] = ordered
        return ordered

    def _selection(self, center: str, radius: int) -> dict[str, Any]:
        cfg = self.cfg
        maximum = {0: cfg.focused_max_tokens, 1: cfg.direct_max_tokens, 2: cfg.extended_max_tokens}[radius]
        target = {
            0: cfg.focused_max_tokens - cfg.package_safety_tokens,
            1: cfg.direct_target_tokens,
            2: cfg.extended_target_tokens,
        }[radius]
        content_limit = max(500, maximum - cfg.package_safety_tokens)
        selected: list[str] = []
        selected_set: set[str] = set()
        content_tokens = 0

        def add(chunk_id: str) -> bool:
            nonlocal content_tokens
            if chunk_id in selected_set:
                return True
            chunk = self.chunk_by_id[chunk_id]
            if content_tokens + chunk.tokens > content_limit:
                return False
            selected.append(chunk_id)
            selected_set.add(chunk_id)
            content_tokens += chunk.tokens
            return True

        core_order = self._core_order(center)
        core_limit = min(content_limit, cfg.focused_max_tokens - cfg.package_safety_tokens)
        for chunk_id in core_order:
            if content_tokens + self.chunk_by_id[chunk_id].tokens <= core_limit:
                add(chunk_id)
        if not selected and core_order:
            add(core_order[0])

        hops = self._file_hops(center, radius)
        if radius:
            boundary: list[tuple[int, float, str, str]] = []
            relevant_edges = {
                (
                    edge.source,
                    edge.target,
                    edge.relationship,
                    edge.symbol,
                ): edge
                for file_path in hops
                for edge in self.cross_edges_by_file.get(file_path, [])
            }
            for edge in relevant_edges.values():
                source = self.chunk_by_id[edge.source]
                target_chunk = self.chunk_by_id[edge.target]
                if source.file == target_chunk.file:
                    continue
                source_hop = hops.get(source.file)
                target_hop = hops.get(target_chunk.file)
                if source_hop is None or target_hop is None:
                    continue
                if source_hop < target_hop:
                    boundary.append((target_hop, -edge.weight, target_chunk.file, edge.target))
                    if source.file == center:
                        boundary.append((0, -edge.weight, source.file, edge.source))
                elif target_hop < source_hop:
                    boundary.append((source_hop, -edge.weight, source.file, edge.source))
                    if target_chunk.file == center:
                        boundary.append((0, -edge.weight, target_chunk.file, edge.target))
            for _hop, _negative_weight, _file_path, chunk_id in sorted(set(boundary)):
                if not add(chunk_id):
                    continue
                parent_id = self.chunk_by_id[chunk_id].parent_entity_id
                if parent_id:
                    for sibling in self.chunks_by_parent.get(parent_id, []):
                        add(sibling.chunk_id)
            for file_path in sorted(hops, key=lambda item: (hops[item], item)):
                if content_tokens >= target:
                    break
                for chunk in self.chunks_by_file.get(file_path, []):
                    if content_tokens >= target:
                        break
                    add(chunk.chunk_id)

        included_files = sorted({self.chunk_by_id[item].file for item in selected})
        omitted_center_sections = [
            chunk_id for chunk_id in core_order if chunk_id not in selected_set
        ]
        return {
            "radius": radius,
            "chunk_ids": selected,
            "included_files": included_files,
            "connected_files_not_included": sorted(set(hops) - set(included_files)),
            "selected_file_sections_not_included": omitted_center_sections,
            "estimated_tokens": content_tokens + cfg.package_safety_tokens,
            "maximum_tokens": maximum,
        }
