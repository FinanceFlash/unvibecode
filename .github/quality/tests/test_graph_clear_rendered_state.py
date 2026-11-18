"""Regression: restoring DataSet colour strings alone leaves renderer overrides."""

from graph_test_helpers import render_map


def test_clear_restores_full_renderer_colors_and_opening_camera(tmp_path):
    doc = render_map(tmp_path)
    assert (
        "JSON.parse(JSON.stringify(network.body.edges[item.id].options.color))" in doc
    )
    assert (
        "position:initialView.position,scale:initialView.scale,animation:false" in doc
    )
    assert (
        "initialView={position:network.getViewPosition(),scale:network.getScale()}"
        in doc
    )
