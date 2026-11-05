"""Exercise the runnable examples and profiles shipped with this repository."""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
RAG_EXAMPLE = ROOT / "skills/unvibecode-rag-review/scripts/rag_review_example.py"
GUARDRAILS_DIR = (
    ROOT
    / "skills/unvibecode_gaurdrails_implemenataion_pack"
    / "Pre-configured_gaurdrails_programs"
)
GUARDRAILS_RUNNER = GUARDRAILS_DIR / "guardrails_runner.py"
PROFILE_NAMES = (
    "guardrails_agent.json",
    "guardrails_chatbot.json",
    "guardrails_multi_agent.json",
    "guardrails_rag.json",
)


def test_rag_example_regressions_pass():
    result = subprocess.run(
        [sys.executable, str(RAG_EXAMPLE)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert result.returncode == 0, result.stderr
    match = re.search(r"Ran (\d+) tests?", result.stderr)
    assert match and int(match.group(1)) > 0, result.stderr


@pytest.mark.parametrize("profile_name", PROFILE_NAMES)
def test_shipped_guardrails_profile_has_no_configuration_errors(profile_name):
    profile = GUARDRAILS_DIR / profile_name
    result = subprocess.run(
        [sys.executable, str(GUARDRAILS_RUNNER), "check", "--config", str(profile)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    report = json.loads(result.stdout)
    assert report["configuration_valid"] is True
    assert report["errors"] == 0
    assert report["warnings"] > 0
    assert report["runtime_verified"] is False


def test_traffic_archive_script_is_valid_python():
    script = ROOT / ".github/scripts/archive_github_traffic.py"
    compile(script.read_text(encoding="utf-8"), str(script), "exec")
