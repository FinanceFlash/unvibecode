import re
from graph_test_helpers import render_map


def test_map_explicit_download_and_stable_layout(tmp_path):
    doc = render_map(tmp_path)
    click = re.search(r"network.on\('click',params=>(.*?)\);", doc, re.S).group(1)
    assert "downloadFor" not in click
    assert "pinnedFile=id" in doc
    assert "downloadButton.addEventListener('click'" in doc
    assert "if(!pinnedFile&&fileSet.has(id))preview(id)" in doc
    assert "physics:{enabled:false}" in doc
    assert "fixed:{x:true,y:true}" in doc
    assert "network.fit({animation:false})" in doc
    assert "uvc-fit-all" in doc and "uvc-clear-selection" in doc
    assert "uvc-file-picker" not in doc and "uvc-context-close" in doc
    assert "Source file" in doc
    assert doc.index("Source file") < doc.index("Download size")
    assert (
        "updateFileDetails(filePath)" in doc
        and "downloadButton.disabled=!selection" in doc
    )
    assert "Hover over a rectangular file node" in doc
    assert "⭐ Star UnvibeCode" in doc
