"""Graph -> the interactive pyvis map (fast_lane_symbol_resolution_graph.html)
and fast_lane_repository_profile.json (languages, roles, application shape).

write_artifacts() is the entry point; the HTML embeds its own help, search
and download buttons and reads the context store written by context.py."""
from __future__ import annotations

import hashlib
import json
import math
import re
import webbrowser
import html as html_lib
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any
from collections.abc import Mapping, Sequence

from .util import _posix
from .link import DEFAULT_OUTPUT_NAME


PALETTE = [
    "#93C5FD", "#86EFAC", "#FDE68A", "#FCA5A5", "#C4B5FD",
    "#67E8F9", "#FDBA74", "#F9A8D4", "#A7F3D0", "#CBD5E1",
]

LANGUAGE_BORDER = {
    "python": "#2563EB", "javascript": "#D97706", "jsx": "#D97706",
    "typescript": "#0891B2", "tsx": "#0891B2", "rust": "#B45309",
    "php": "#7C3AED", "ruby": "#DC2626", "html": "#EA580C",
    "css": "#0284C7",
}


def _top_directory(file_path: str) -> str:
    parts = PurePosixPath(_posix(file_path)).parts
    return parts[0] if len(parts) > 1 else "repository root"


def _folder_color(file_path: str) -> str:
    directory = _top_directory(file_path)
    index = int(hashlib.sha256(directory.encode("utf-8")).hexdigest()[:8], 16)
    return PALETTE[index % len(PALETTE)]


def _graph_nodes(graph: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for raw in graph.get("nodes", []) or []:
        if not isinstance(raw, Mapping):
            continue
        file_path = _posix(raw.get("file"))
        if file_path:
            output[file_path] = dict(raw)
    return output


def _file_title(file_path: str, node: Mapping[str, Any]) -> str:
    roles = ", ".join(str(value) for value in node.get("role_hints", []) if value)
    entities = [
        str(item.get("qualified_name") or item.get("name") or "")
        for item in node.get("entities", []) or [] if isinstance(item, Mapping)
    ]
    entity_preview = ", ".join(value for value in entities if value)[:420]
    escape = html_lib.escape
    return (
        f"<b>{escape(file_path)}</b><br>"
        f"Language: {escape(str(node.get('language') or 'unknown'))}<br>"
        f"Directory: {escape(_top_directory(file_path))}<br>"
        f"Lines: {escape(str(node.get('line_count') or 0))}<br>"
        f"Parser: {escape(str(node.get('parser_used') or 'unknown'))} "
        f"({escape(str(node.get('parser_confidence') or 'unknown'))})<br>"
        f"Roles: {escape(roles or 'none')}<br>"
        f"Entities: {escape(entity_preview or 'none')}<br>"
        f"Unresolved imports: {escape(str(node.get('unresolved_import_count') or 0))}"
    )


def _import_pyvis() -> Any:
    try:
        from pyvis.network import Network  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "PyVis is required for Fast Lane browser graphs. Install it with:\n"
            "    python -m pip install pyvis"
        ) from exc
    return Network


def _network(Network: Any, heading: str) -> Any:
    net = Network(
        height="93vh", width="100%", directed=True,
        bgcolor="#F8FAFC", font_color="#0F172A", heading="",
        select_menu=False, filter_menu=False, cdn_resources="in_line",
    )
    # PyVis can render its heading twice when select/filter templates are
    # enabled. Keep the template heading empty and inject one controlled title
    # during the UTF-8 write below.
    net.shipready_heading = heading
    net.set_options(
        """
        {
          "interaction": {
            "hover": true, "navigationButtons": true, "keyboard": true,
            "tooltipDelay": 100, "hideEdgesOnDrag": true
          },
          "nodes": {
            "shape": "box", "margin": 10,
            "font": {"face": "Segoe UI", "size": 14},
            "shadow": {"enabled": true, "size": 5, "x": 1, "y": 2}
          },
          "edges": {
            "arrows": {"to": {"enabled": true, "scaleFactor": 0.7}},
            "color": {"color": "#94A3B8", "highlight": "#0F766E"},
            "smooth": {"enabled": true, "type": "dynamic"},
            "font": {"face": "Segoe UI", "size": 10, "align": "middle"}
          },
          "physics": {
            "enabled": true, "solver": "forceAtlas2Based",
            "forceAtlas2Based": {
              "gravitationalConstant": -55, "centralGravity": 0.012,
              "springLength": 125, "springConstant": 0.06,
              "damping": 0.45, "avoidOverlap": 0.75
            },
            "stabilization": {"enabled": true, "iterations": 650, "fit": true}
          }
        }
        """
    )
    return net


# The map's controls (download panel, file search, layout freeze) live in
# map_ui.html next to this file; @@NAME@@ placeholders are filled in one pass.
_MAP_UI_PLACEHOLDER = re.compile(r"@@(STORE_NAME|PRESENTATION_JSON)@@")


def _map_ui_template() -> str:
    return Path(__file__).with_name("map_ui.html").read_text(encoding="utf-8")


def _write_html(
    net: Any,
    output_path: Path,
    *,
    context_store_filename: str | None = None,
    complete_context_bundle_filename: str | None = None,
) -> None:
    """Render PyVis HTML without using the Windows locale encoding.

    PyVis ``write_html`` opens the destination without an explicit encoding.
    On Windows that commonly selects cp1252 and fails when repository names,
    symbols, paths or source-derived tooltips contain Unicode. Generate the
    document in memory and persist it explicitly as UTF-8 instead.
    """

    rendered = net.generate_html(notebook=False)
    if not isinstance(rendered, str) or not rendered.strip():
        raise RuntimeError(f"PyVis generated empty HTML for: {output_path}")
    heading = html_lib.escape(
        str(getattr(net, "shipready_heading", "ShipReady Fast Lane"))
    )
    if context_store_filename:
        complete_bundle = ""
        if complete_context_bundle_filename:
            bundle_name = html_lib.escape(
                complete_context_bundle_filename, quote=True
            )
            complete_bundle = (
                '<div style="margin-top:7px;padding-top:6px;border-top:1px solid '
                'rgba(219,234,254,.24);font-size:10px">'
                f'<a href="{bundle_name}" download style="color:#fff;font-weight:700;'
                'text-decoration:underline;text-underline-offset:2px">'
                'Download complete repository context</a>'
                '<span style="margin-left:6px;color:#bfdbfe">'
                'Produces the normalized ZIP bundle for later analysis or API automation.'
                '</span></div>'
            )
        title_block = (
            '<div id="shipready-title" style="position:fixed;top:10px;left:50%;'
            'transform:translateX(-50%);z-index:1000;width:min(900px,calc(100vw - 40px));'
            'min-width:0;background:rgba(15,23,42,.94);color:white;padding:9px 18px;'
            'border-radius:12px;box-shadow:0 6px 18px rgba(15,23,42,.18);'
            'font-family:Segoe UI,Arial,sans-serif;text-align:center">'
            '<div style="font-size:16px;font-weight:700">'
            'Download contextually connected code for your LLM</div>'
            '<div style="margin-top:3px;color:#dbeafe;font-size:11px;font-weight:400">'
            'Hover over a file to preview connections. '
            'Select a file, choose a context size, then download.</div>'
            + complete_bundle
            + '</div>'
        )
    else:
        title_block = (
            '<div id="shipready-title" style="position:fixed;top:10px;left:50%;'
            'transform:translateX(-50%);z-index:1000;background:rgba(15,23,42,.92);'
            'color:white;padding:9px 18px;border-radius:12px;font:600 16px Segoe UI,'
            'Arial,sans-serif;box-shadow:0 6px 18px rgba(15,23,42,.18);white-space:nowrap">'
            f'{heading}</div>'
        )
    rendered = rendered.replace("<body>", "<body>\n" + title_block, 1)
    if context_store_filename:
        presentation_json = json.dumps(getattr(net, "shipready_presentation", {}), ensure_ascii=True).replace("<", "\\u003c")
        store_name = html_lib.escape(context_store_filename, quote=True)
        download_controls = _MAP_UI_PLACEHOLDER.sub(
            lambda m: {"STORE_NAME": store_name, "PRESENTATION_JSON": presentation_json}[m.group(1)],
            _map_ui_template(),
        )
        rendered = rendered.replace("</body>", download_controls + "\n</body>", 1)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8", newline="\n")


def _add_file_node(
    net: Any,
    file_path: str,
    node: Mapping[str, Any],
    degree: int,
) -> None:
    language = str(node.get("language") or "unknown").lower()
    net.add_node(
        file_path,
        label=PurePosixPath(file_path).name,
        title=_file_title(file_path, node),
        shape="box",
        directory=_top_directory(file_path),
        color={
            "background": _folder_color(file_path),
            "border": LANGUAGE_BORDER.get(language, "#475569"),
            "highlight": {"background": "#FFFFFF", "border": "#0F766E"},
        },
        borderWidth=2,
        borderWidthSelected=4,
        size=max(16, min(42, 15 + degree * 1.7)),
        value=max(1, degree),
    )


def _is_uncertain(edge: Mapping[str, Any]) -> bool:
    """Presentation only: do not promote absent/conflicting resolution evidence."""
    if edge.get("is_uncertain") or edge.get("uncertain"):
        return True
    status = str(edge.get("resolution_status") or edge.get("status") or "").lower()
    if status in {"unresolved", "ambiguous", "partial", "uncertain", "unknown"}:
        return True
    return str(edge.get("confidence") or "").lower() != "high"


def _render_symbol_graph(
    Network: Any,
    graph: Mapping[str, Any],
    output_path: Path,
    *,
    context_store_filename: str | None = None,
    complete_context_bundle_filename: str | None = None,
) -> dict[str, Any]:
    inventory = _graph_nodes(graph)
    # Preserve original records, including duplicates and self-links. Group only
    # their visual representation; analysis and context exports are untouched.
    def eligible(values):
        return [dict(e) for e in values if isinstance(e, Mapping)
                and e.get("source") in inventory and e.get("target") in inventory]
    symbols = eligible(graph.get("symbol_edges", []) or [])
    imports = eligible(graph.get("edges", []) or [])
    degree: Counter[str] = Counter()
    for e in symbols + imports:
        degree[e["source"]] += 1
        degree[e["target"]] += 1
    net = _network(Network, "Connected Code Map")
    for file in sorted(inventory):
        _add_file_node(net, file, inventory[file], degree[file])
        # Exact path is available for search; no confidence text is exposed.
        net.nodes[-1].pop("title", None)
        net.nodes[-1]["file_path"] = file
    groups = {}
    covered_imports = set()
    added_symbols = set()
    for e in symbols:
        source, target = e["source"], e["target"]
        symbol = str(e.get("symbol") or "module import")
        uncertain = _is_uncertain(e)
        # Split symbol nodes by certainty so a shared diamond cannot turn an
        # uncertain source-to-target route into a solid route.
        sid = "uvc-symbol:" + hashlib.sha256(
            json.dumps([target, symbol, uncertain], ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        if sid not in added_symbols:
            net.add_node(sid, label=symbol, shape="diamond", directory="resolved symbols",
                         symbol_target=target, symbol_name=symbol,
                         color={"background": "#FDE68A", "border": "#B45309"},
                         borderWidth=2, size=13, value=1)
            added_symbols.add(sid)
        # Only suppress a file arrow for the same recorded import location and
        # certainty. A different import between the same files remains visible.
        if e.get("line") is not None:
            covered_imports.add((source, target, str(e["line"]), uncertain))
        for start, end in [(source, sid), (sid, target)]:
            groups.setdefault((start, end, uncertain), []).append(e)
    suppressed = []
    for e in imports:
        key = (e["source"], e["target"], str(e.get("line")), _is_uncertain(e))
        if e.get("line") is not None and key in covered_imports:
            suppressed.append(e)
            continue
        groups.setdefault((e["source"], e["target"], _is_uncertain(e)), []).append(e)
    for i, ((source, target, uncertain), records) in enumerate(sorted(groups.items())):
        net.add_edge(source, target, id=f"uvc-edge-{i}", dashes=uncertain,
                     width=1.2 if uncertain else 1.7, relationship_records=records)
    # Large graphs receive a deterministic initial layout instead of an
    # expensive force simulation. All nodes and links are still present.
    if len(net.nodes) > 400:
        files = sorted(inventory, key=lambda f: (str(PurePosixPath(f).parent), f))
        columns = max(1, math.ceil(math.sqrt(len(files))))
        positions = {file: ((i % columns) * 360, (i // columns) * 240)
                     for i, file in enumerate(files)}
        symbol_index = 0
        for node in net.nodes:
            if node["id"] in positions:
                x, y = positions[node["id"]]
            else:
                x, y = positions[node["symbol_target"]]
                symbol_index += 1
                angle = symbol_index * 2.399963229728653
                x += 90 * math.cos(angle)
                y += 80 * math.sin(angle)
            node.update(x=x, y=y, physics=False)
        net.options = {
            "physics": {"enabled": False}, "layout": {"improvedLayout": False},
            "interaction": {"hover": True, "navigationButtons": True, "keyboard": True,
                            "hideEdgesOnDrag": True, "dragNodes": False},
            "edges": {"arrows": {"to": {"enabled": True, "scaleFactor": .7}},
                      "smooth": {"enabled": False}, "color": {"color": "#94A3B8"}},
            "nodes": {"font": {"face": "Segoe UI", "size": 14}, "margin": 10}
        }
    net.shipready_presentation = {"file_ids": sorted(inventory),
        "symbol_relationships": len(symbols), "file_relationships": len(imports),
        "file_imports_represented_by_symbols": suppressed,
        "static_layout": len(net.nodes) > 400}
    _write_html(net, output_path,
        context_store_filename=context_store_filename,
        complete_context_bundle_filename=complete_context_bundle_filename)
    return {"complete_symbol_edges": len(symbols), "rendered_symbol_edges": len(symbols),
            "rendered_file_nodes": len(inventory), "rendered_symbol_nodes": len(added_symbols),
            "complete_file_edges": len(imports), "visual_edges": len(groups),
            "file_edge_fallback_used": not bool(symbols)}



def _application_profile(graph: Mapping[str, Any]) -> dict[str, Any]:
    nodes = [node for node in graph.get("nodes", []) or [] if isinstance(node, Mapping)]
    languages: Counter[str] = Counter(str(node.get("language") or "unknown") for node in nodes)
    roles: Counter[str] = Counter(
        str(role) for node in nodes for role in (node.get("role_hints", []) or []) if role
    )
    paths = [_posix(node.get("file")).lower() for node in nodes]
    entity_kinds: Counter[str] = Counter(
        str(entity.get("kind") or "unknown")
        for node in nodes for entity in (node.get("entities", []) or [])
        if isinstance(entity, Mapping)
    )

    shapes: list[dict[str, Any]] = []

    def add_shape(shape: str, signals: Sequence[str], strong: bool = False) -> None:
        evidence = [signal for signal in signals if signal]
        if evidence:
            shapes.append({
                "shape": shape,
                "confidence": "HIGH" if strong or len(evidence) >= 2 else "MEDIUM",
                "evidence": list(evidence)[:8],
            })

    api_count = roles["api_route"] + roles["api_route_file"] + roles["api_or_controller_file"]
    add_shape("API_SERVICE", [f"{api_count} API/controller signals"] if api_count else [], api_count >= 2)
    frontend_count = sum(
        roles[name] for name in (
            "next_page_component", "ui_component_file", "html_page", "entry_or_index_page"
        )
    )
    add_shape("WEB_FRONTEND", [f"{frontend_count} page/UI signals"] if frontend_count else [], frontend_count >= 2)
    worker_files = [path for path in paths if any(word in path for word in ("worker", "consumer", "queue", "task"))]
    add_shape("BACKGROUND_WORKER_OR_CONSUMER", worker_files[:5], len(worker_files) >= 2)
    scheduled_files = [path for path in paths if any(word in path for word in ("cron", "schedule", "scheduler", "periodic"))]
    add_shape("SCHEDULED_SERVICE", scheduled_files[:5], len(scheduled_files) >= 2)
    cli_files = [path for path in paths if path.endswith("__main__.py") or any(word in path for word in ("/cli", "command", "commands/"))]
    main_entry_files = [
        _posix(node.get("file"))
        for node in nodes
        if any(
            str(entity.get("name") or entity.get("qualified_name") or "").split(".")[-1] == "main"
            for entity in (node.get("entities", []) or [])
            if isinstance(entity, Mapping)
        )
    ]
    cli_files.extend(path for path in main_entry_files if path not in cli_files)
    add_shape("CLI_APPLICATION", cli_files[:5], len(cli_files) >= 2)
    pipeline_files = [path for path in paths if any(word in path for word in ("pipeline", "etl", "ingest", "transform"))]
    add_shape("DATA_PIPELINE", pipeline_files[:5], len(pipeline_files) >= 2)
    if not shapes and entity_kinds:
        add_shape(
            "IMPORTABLE_LIBRARY_OR_UTILITY",
            [f"{sum(entity_kinds.values())} parsed entities with no strong runtime entrypoint signal"],
        )

    total_files = max(1, len(nodes))
    return {
        "schema_version": "shipreadyv2.fast_lane_profile.v1",
        "repository_name": graph.get("repo_name"),
        "workspace_root": graph.get("workspace_root"),
        "files_scanned": len(nodes),
        "language_counts": dict(sorted(languages.items())),
        "language_percentages": {
            language: round(count * 100.0 / total_files, 2)
            for language, count in sorted(languages.items())
        },
        "application_shapes": shapes,
        "top_role_hints": dict(roles.most_common(20)),
        "entity_kind_counts": dict(entity_kinds.most_common()),
        "interpretation_boundary": (
            "Fast deterministic profile. Application shapes are evidence-backed hints, "
            "not final business classifications."
        ),
    }


def write_artifacts(
    stage_one_graph: Mapping[str, Any],
    resolved_graph: Mapping[str, Any],
    run_directory: Path,
    *,
    auto_open: bool,
    context_store_filename: str | None = None,
    complete_context_bundle_filename: str | None = None,
) -> dict[str, Any]:
    Network = _import_pyvis()
    profile_json = run_directory / "fast_lane_repository_profile.json"
    symbol_html = run_directory / "fast_lane_symbol_resolution_graph.html"

    profile = _application_profile(stage_one_graph)
    profile_json.write_text(
        json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    symbol_summary = _render_symbol_graph(
        Network,
        resolved_graph,
        symbol_html,
        context_store_filename=context_store_filename,
        complete_context_bundle_filename=complete_context_bundle_filename,
    )

    if auto_open:
        opened = webbrowser.open_new_tab(symbol_html.resolve().as_uri())
        print(
            f"Browser request {'sent' if opened else 'not acknowledged'}: "
            f"{symbol_html.name}"
        )

    return {
        "profile_json": str(profile_json),
        "resolved_graph_json": str(run_directory / DEFAULT_OUTPUT_NAME),
        "symbol_graph_html": str(symbol_html),
        "symbol_graph_summary": symbol_summary,
    }
