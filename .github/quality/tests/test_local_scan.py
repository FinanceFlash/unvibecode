import json
from zipfile import ZipFile
from importlib.util import find_spec

from graph_test_helpers import Network

from unvibecode_graph.__main__ import main


def test_local_scan_writes_connected_map_and_context(tmp_path, monkeypatch):
    if find_spec("pyvis") is None:
        monkeypatch.setattr("unvibecode_graph.render._import_pyvis", lambda: Network)
    repo = tmp_path / "example"
    repo.mkdir()
    (repo / "main.py").write_text("from helper import greet\ngreet()\n")
    (repo / "helper.py").write_text("def greet():\n    return 'hello'\n")
    output = tmp_path / "results"
    assert main([str(repo), "--out", str(output)]) == 0
    run = output / "run"
    graph = json.loads((run / "shipreadyv2_resolved_graph.json").read_text())
    assert any(
        edge["source"] == "main.py" and edge["target"] == "helper.py"
        for edge in graph["edges"]
    )
    assert "main.py" in (run / "fast_lane_symbol_resolution_graph.html").read_text(
        encoding="utf-8"
    )
    with ZipFile(run / "shipready_complete_repository_context.zip") as bundle:
        assert bundle.namelist()
        assert bundle.testzip() is None
