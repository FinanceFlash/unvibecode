import importlib.util
from pathlib import Path

import pytest

SCRIPT_PATH = (
    Path(__file__).resolve().parents[2] / "scripts" / "archive_github_traffic.py"
)

SPEC = importlib.util.spec_from_file_location("archive_github_traffic", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None

traffic = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(traffic)


def test_write_csv_preserves_existing_file_when_write_fails(tmp_path):
    target = tmp_path / "daily.csv"
    original_content = "ORIGINAL DATA\n"
    target.write_text(original_content, encoding="utf-8")

    def failing_rows():
        yield {"date": "2026-11-04"}
        raise RuntimeError("simulated mid-write failure")

    with pytest.raises(RuntimeError, match="simulated mid-write failure"):
        traffic.write_csv(target, ["date"], failing_rows())

    assert target.read_text(encoding="utf-8") == original_content
    assert not list(tmp_path.glob(".daily.csv.*.tmp"))
