"""run(): scan a repository and write its connected code graph.

    repository -> build (file graph) -> link (resolved symbol graph)
               -> context (per-file connected-code downloads + complete ZIP)
               -> render (interactive graph HTML + repository profile)

No network, LLM or taxonomy calls. Files written to a new run folder:

    shipreadyv2_resolved_graph.json          the resolved graph
    fast_lane_symbol_resolution_graph.html   the interactive map
    fast_lane_repository_profile.json        languages, roles, application shape
    fast_lane_context_store.json / .js       download selections (API / browser)
    shipready_complete_repository_context.zip
    fast_lane_timing.json
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from collections.abc import Callable

from .config import Config
from .build import GraphBuilder
from .link import DEFAULT_OUTPUT_NAME, Linker
from .context import ContextBuilder
from .render import write_artifacts


def _new_run_directory(output_root: Path) -> Path:
    """Create output_root/run, or run_2, run_3, ... if it already exists."""

    base_name = "run"
    candidate = output_root / base_name
    suffix = 2
    while candidate.exists():
        candidate = output_root / f"{base_name}_{suffix}"
        suffix += 1
    candidate.mkdir(parents=True, exist_ok=False)
    return candidate


@dataclass
class Result:
    run_dir: Path  # the new run folder holding every output file
    resolved_graph: Path  # run_dir / shipreadyv2_resolved_graph.json
    timing: dict[str, float]


def run(
    repo: str | Path,
    out_dir: str | Path,
    cfg: Config = Config(),
    *,
    on_progress: Callable[[str, int, int], None] | None = None,
    skip_dir: Callable[[Path], bool] | None = None,
) -> Result:
    """Build the connected code graph of `repo` in a new folder under `out_dir`.

    on_progress(stage, done, total) is called as work completes. Stages, in order:
      scan (0, files)          parse (k, files)        graph (files, files)
      link_start / link_done   context_start (0, files)
      chunk (k, files)         chunked (sections)      connect (relationships)
      select (k, files)        context_done            render_start / render_done
    skip_dir(path) -> True leaves a folder out of the scan, on top of IGNORE_DIRS.
    """

    progress = on_progress or (lambda *_: None)
    started = time.monotonic()
    workspace = Path(repo).expanduser().resolve()
    if not workspace.is_dir():
        raise FileNotFoundError(f"Repository folder does not exist or is not a directory: {workspace}")
    run_directory = _new_run_directory(Path(out_dir).expanduser().resolve())
    output_path = run_directory / DEFAULT_OUTPUT_NAME
    store_js = run_directory / "fast_lane_context_store.js"
    store_json = run_directory / "fast_lane_context_store.json"
    bundle_zip = run_directory / "shipready_complete_repository_context.zip"
    timing: dict[str, float] = {}

    def lap(key: str, since: float) -> None:
        timing[key] = round(time.monotonic() - since, 3)

    try:
        t = time.monotonic()
        stage_one_graph = GraphBuilder(str(workspace), skip_dir=skip_dir, on_progress=progress).build()
        lap("graph_build_seconds", t)

        t = time.monotonic()
        linker = Linker(
            graph_documents=[stage_one_graph],
            allow_global_symbol_fallback=cfg.allow_global_symbol_fallback,
            strict_hard_path=cfg.strict_hard_path,
            deep_relative_parent_hops=cfg.deep_relative_parent_hops,
            enrich_python=cfg.enrich_python,
        )
        progress("link_start", 0, 1)
        linker.resolve_to(output_path)
        progress("link_done", 1, 1)
        if linker.resolved_document is None:
            raise RuntimeError("Linker completed without exposing the resolved graph to the feed stage.")
        lap("linker_seconds", t)

        context_summary: dict[str, Any] = {}
        timing["context_download_preparation_seconds"] = 0.0
        if cfg.context_downloads:
            t = time.monotonic()
            context_builder = ContextBuilder(workspace, linker.resolved_document, cfg, on_progress=progress)
            progress("context_start", 0, len(context_builder.graph.get("nodes", []) or []))
            context_summary = context_builder.build(store_js, json_output_path=store_json, bundle_output_path=bundle_zip)
            progress("context_done", 1, 1)
            lap("context_download_preparation_seconds", t)

        t = time.monotonic()
        progress("render_start", 0, 1)
        artifacts = write_artifacts(
            stage_one_graph,
            linker.resolved_document,
            run_directory,
            auto_open=cfg.open_browser,
            context_store_filename=store_js.name if cfg.context_downloads else None,
            complete_context_bundle_filename=bundle_zip.name if cfg.context_downloads else None,
        )
        progress("render_done", 1, 1)
        lap("html_render_seconds", t)
        lap("fast_lane_total_seconds", started)

        (run_directory / "fast_lane_timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=2), encoding="utf-8")
        _print_done(workspace, run_directory, output_path, artifacts, context_summary, store_json, bundle_zip, timing)
        return Result(run_directory, output_path, timing)
    except Exception:
        # Do not leave partial/confusing artifacts after a failed execution.
        output_path.unlink(missing_ok=True)
        if run_directory.exists() and not any(run_directory.iterdir()):
            run_directory.rmdir()
        raise


def _print_done(workspace, run_directory, output_path, artifacts, context_summary, store_json, bundle_zip, timing) -> None:
    print("\n[SHIPREADYV2 FAST LANE COMPLETE]")
    print(f"Target folder: {workspace}")
    print(f"Run folder:    {run_directory}")
    print(f"Profile JSON:  {artifacts['profile_json']}")
    print(f"Resolved JSON: {output_path}")
    print(f"Symbol graph:  {artifacts['symbol_graph_html']}")
    if context_summary:
        print(
            "Click downloads: "
            f"{context_summary['source_files']:,} files, "
            f"{context_summary['atomic_code_sections']:,} code sections, "
            f"prepared in {timing['context_download_preparation_seconds']:.3f}s"
        )
        print(f"Context JSON:  {store_json}")
        print(f"Complete ZIP:  {bundle_zip}")
        print(f"Context timing: {context_summary['preparation_seconds']}")
    print(f"Timing:        {timing}")
