from pathlib import Path
import re
from urllib.parse import unquote

import pytest

ROOT = Path(__file__).resolve().parents[3]
PACKS_ROOT = ROOT / "prebuilt-workflow-paths"

REQUIRED_PACK_FILES = {
    "README.md",
    "PRODUCT_AND_BUSINESS_GUIDE.md",
    "ENGINEERING_GUIDE.md",
    "CORE_20_SCENARIOS.md",
    "TESTING_GUIDE.md",
    "PATHS_AND_EDGE_CASES.md",
    "PERMISSION_AND_ABUSE_GUIDE.md",
    "RETRY_AND_RECOVERY_GUIDE.md",
    "WRITE_PRODUCT_SPEC_SKILL.md",
    "REVIEW_BUSINESS_RISK_SKILL.md",
    "UNDERSTAND_CODE_SKILL.md",
    "IMPLEMENT_WORKFLOW_SKILL.md",
    "TEST_WORKFLOW_SKILL.md",
}

SKILL_FILES = {name for name in REQUIRED_PACK_FILES if name.endswith("_SKILL.md")}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
CORE_SCENARIO_ROW = re.compile(r"^\|\s*(\d+)\s*\|", re.MULTILINE)
CORE_SCENARIO_WITH_OUTCOME = re.compile(
    r"^\|\s*(\d+)\s*\|[^|]+\|\s*\S[^|]*\|\s*$", re.MULTILINE
)


def workflow_packs():
    return sorted(path for path in PACKS_ROOT.iterdir() if path.is_dir())


@pytest.mark.parametrize("pack", workflow_packs(), ids=lambda path: path.name)
def test_workflow_pack_has_required_files(pack):
    present = {path.name for path in pack.iterdir() if path.is_file()}
    assert REQUIRED_PACK_FILES <= present, sorted(REQUIRED_PACK_FILES - present)


@pytest.mark.parametrize("pack", workflow_packs(), ids=lambda path: path.name)
def test_workflow_pack_defines_a_mece_boundary(pack):
    readme = (pack / "README.md").read_text(encoding="utf-8")
    assert "Starts when" in readme
    assert "Ends when" in readme
    assert "## Included" in readme
    assert "## Excluded" in readme


@pytest.mark.parametrize("pack", workflow_packs(), ids=lambda path: path.name)
def test_workflow_pack_has_exactly_twenty_core_scenarios(pack):
    content = (pack / "CORE_20_SCENARIOS.md").read_text(encoding="utf-8")
    scenario_numbers = [int(value) for value in CORE_SCENARIO_ROW.findall(content)]
    assert scenario_numbers == list(range(1, 21))


@pytest.mark.parametrize("pack", workflow_packs(), ids=lambda path: path.name)
def test_every_core_scenario_states_an_outcome_to_prevent(pack):
    content = (pack / "CORE_20_SCENARIOS.md").read_text(encoding="utf-8")
    scenarios_with_outcomes = [
        int(value) for value in CORE_SCENARIO_WITH_OUTCOME.findall(content)
    ]
    assert scenarios_with_outcomes == list(range(1, 21))


@pytest.mark.parametrize("pack", workflow_packs(), ids=lambda path: path.name)
def test_workflow_skills_have_frontmatter(pack):
    for filename in SKILL_FILES:
        content = (pack / filename).read_text(encoding="utf-8")
        assert content.startswith("---\n"), filename
        frontmatter = content.split("---", 2)[1]
        assert re.search(r"^name:\s*\S+", frontmatter, re.MULTILINE), filename
        assert re.search(r"^description:\s*\S+", frontmatter, re.MULTILINE), filename


def test_pack_index_links_every_workflow_pack():
    index = (PACKS_ROOT / "README.md").read_text(encoding="utf-8")
    for pack in workflow_packs():
        assert f"]({pack.name}/)" in index, pack.name


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


@pytest.mark.parametrize("markdown_file", sorted(ROOT.rglob("*.md")))
def test_markdown_has_no_common_encoding_corruption(markdown_file):
    content = markdown_file.read_text(encoding="utf-8")
    corrupt_markers = ("â”", "Ã", "�")
    assert not any(marker in content for marker in corrupt_markers)


@pytest.mark.parametrize("markdown_file", sorted(ROOT.rglob("*.md")))
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
