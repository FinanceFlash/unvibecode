"""Regression tests for guardrails_runner.py (run with pytest from this directory)."""

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
RUNNER = HERE / "guardrails_runner.py"


def run_check(config_path):
    return subprocess.run(
        [sys.executable, str(RUNNER), "check", "--config", str(config_path)],
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_deeply_nested_config_exits_2_with_json_report(tmp_path):
    deep = tmp_path / "deep.json"
    deep.write_text('{"a":' * 10000 + "1" + "}" * 10000, encoding="utf-8")

    result = run_check(deep)

    assert result.returncode == 2
    assert "Traceback" not in result.stderr
    report = json.loads(result.stdout)
    assert report["configuration_valid"] is False
    assert "error" in report


def test_shipped_profile_passes_check():
    result = run_check(HERE / "guardrails_chatbot.json")

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["configuration_valid"] is True
