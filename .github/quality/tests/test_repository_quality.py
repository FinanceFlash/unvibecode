from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

import pytest

ROOT = Path(__file__).resolve().parents[3]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def tracked_markdown():
    paths = subprocess.check_output(
        ["git", "ls-files", "-z", "--", "*.md"], cwd=ROOT
    ).decode("utf-8")
    return [ROOT / name for name in paths.split("\0") if name]


def test_github_automation_files_are_in_discoverable_locations():
    assert (ROOT / ".github/workflows/test.yml").is_file()
    assert (ROOT / ".github/pull_request_template.md").is_file()
    assert (ROOT / ".github/CONTRIBUTING.md").is_file()
    assert (ROOT / ".github/quality/requirements.txt").is_file()
    assert (ROOT / ".github/quality/pyproject.toml").is_file()
    assert (ROOT / ".github/quality/tests/test_repository_quality.py").is_file()
    assert not (ROOT / "test.yml").exists()
    assert not (ROOT / "pull_request_template.md").exists()
    assert not (ROOT / "CONTRIBUTING.md").exists()
    assert not (ROOT / "requirements-dev.txt").exists()
    assert not (ROOT / "pyproject.toml").exists()
    assert not (ROOT / "tests/test_repository_quality.py").exists()


@pytest.mark.parametrize("markdown_file", tracked_markdown())
def test_markdown_has_no_common_encoding_corruption(markdown_file):
    content = markdown_file.read_text(encoding="utf-8")
    corrupt_markers = ("â”", "Ã", "�")
    assert not any(marker in content for marker in corrupt_markers)


@pytest.mark.parametrize("markdown_file", tracked_markdown())
def test_local_markdown_links_resolve(markdown_file):
    content = markdown_file.read_text(encoding="utf-8")
    missing = []

    for raw_target in MARKDOWN_LINK.findall(content):
        target = unquote(raw_target.strip()).split("#", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if not (markdown_file.parent / target).resolve().exists():
            missing.append(raw_target)

    assert not missing, missing
