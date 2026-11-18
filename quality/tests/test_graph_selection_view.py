"""Guard view behavior; Chromium replay verifies state restoration on real graphs."""

import re
from graph_test_helpers import render_map


def test_sidebar_selection_preserves_camera_and_clear_fits_all(tmp_path):
    doc = render_map(tmp_path)
    choose = re.search(r"function chooseFile\(\)\{(.*?)\}\n", doc).group(1)
    assert "preview(file)" in choose
    assert "network.focus" not in choose and "network.fit" not in choose
    clear = re.search(r"function clearSelection\(\)\{(.*?)\}\n", doc).group(1)
    assert "hidePanel()" in clear and "network.unselectAll()" in clear
    assert "network.fit({animation:false})" in clear
    assert 'id="uvc-search-control"' in doc
    assert "#uvc-file-toggle::after" in doc
    assert "height:32px" in doc
