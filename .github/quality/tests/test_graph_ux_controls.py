"""Graph UI recovery guards; runtime interactions are also tested in Chromium."""

from graph_test_helpers import render_map


def test_graph_controls_and_compact_picker(tmp_path):
    doc = render_map(tmp_path)
    assert "Explore files and connections" in doc
    assert 'id="uvc-file-results" size="3"' in doc
    assert 'id="uvc-file-toggle"' in doc
    assert 'id="uvc-file-count"' not in doc
    help_start = doc.index('<div id="uvc-graph-help">')
    tools_start = doc.index('<div id="uvc-map-tools">')
    assert help_start < doc.index('id="uvc-map-instruction"', help_start) < tools_start
    for control in (
        "uvc-fit-all",
        "uvc-clear-selection",
        "shipready-context-size",
        "shipready-download-button",
        "shipready-context-legend",
    ):
        assert 'id="' + control + '"' in doc
    assert "syncPicker(id);preview(id)" in doc
    assert "syncPicker(file);preview(file)" in doc
    assert "Math.min(bounds.bottom,window.innerHeight)" in doc
