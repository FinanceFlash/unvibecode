#!/usr/bin/env python3
"""Archive GitHub repository traffic with compact, long-term CSV storage.

GitHub only exposes a rolling traffic window. This script is intended to run
once per day from GitHub Actions so the repository keeps its own history.

Stored datasets:
- daily.csv: daily views / unique visitors / clones / unique cloners
- referrers.csv: daily snapshots of the rolling top referrers
- popular_paths.csv: daily snapshots of the rolling top repository paths

The script is idempotent for a given UTC date: re-running it replaces that
date's referrer/path snapshot instead of adding duplicates.
"""

from __future__ import annotations

import csv
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen


REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "FinanceFlash/unvibecode")
TOKEN = os.environ.get("TRAFFIC_TOKEN", "").strip()
DATA_DIR = Path(os.environ.get("TRAFFIC_DATA_DIR", "analytics/github-traffic"))
API_ROOT = f"https://api.github.com/repos/{REPOSITORY}"

DAILY_FIELDS = ["date", "views", "unique_visitors", "clones", "unique_cloners"]
REFERRER_FIELDS = ["snapshot_date", "rank", "referrer", "count", "uniques"]
PATH_FIELDS = ["snapshot_date", "rank", "path", "count", "uniques"]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def api_get(endpoint: str) -> Any:
    request = Request(
        f"{API_ROOT}/{endpoint}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {TOKEN}",
            "User-Agent": "unvibecode-traffic-archiver",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        fail(f"GitHub API request failed ({exc.code}) for {endpoint}: {body}")
    except Exception as exc:
        fail(f"GitHub API request failed for {endpoint}: {exc}")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def update_daily(views: dict[str, Any], clones: dict[str, Any]) -> None:
    path = DATA_DIR / "daily.csv"
    rows_by_date: dict[str, dict[str, Any]] = {}

    for row in read_csv(path):
        date = row.get("date", "")
        if date:
            rows_by_date[date] = {field: row.get(field, "") for field in DAILY_FIELDS}

    def ensure_row(date: str) -> dict[str, Any]:
        if date not in rows_by_date:
            rows_by_date[date] = {
                "date": date,
                "views": "",
                "unique_visitors": "",
                "clones": "",
                "unique_cloners": "",
            }
        return rows_by_date[date]

    for item in views.get("views", []):
        date = str(item["timestamp"])[:10]
        row = ensure_row(date)
        row["views"] = item["count"]
        row["unique_visitors"] = item["uniques"]

    for item in clones.get("clones", []):
        date = str(item["timestamp"])[:10]
        row = ensure_row(date)
        row["clones"] = item["count"]
        row["unique_cloners"] = item["uniques"]

    ordered = [rows_by_date[key] for key in sorted(rows_by_date)]
    write_csv(path, DAILY_FIELDS, ordered)


def replace_snapshot(
    filename: str,
    fieldnames: list[str],
    snapshot_date: str,
    items: list[dict[str, Any]],
    value_key: str,
) -> None:
    """Replace one UTC day's snapshot, keeping all previous days."""
    path = DATA_DIR / filename
    historical = [
        row
        for row in read_csv(path)
        if row.get("snapshot_date") != snapshot_date
    ]

    current: list[dict[str, Any]] = []
    for rank, item in enumerate(items, start=1):
        current.append(
            {
                "snapshot_date": snapshot_date,
                "rank": rank,
                value_key: item[value_key],
                "count": item["count"],
                "uniques": item["uniques"],
            }
        )

    combined = historical + current
    combined.sort(
        key=lambda row: (
            row.get("snapshot_date", ""),
            int(row.get("rank", 0) or 0),
        )
    )
    write_csv(path, fieldnames, combined)


def main() -> None:
    if not TOKEN:
        fail(
            "TRAFFIC_TOKEN is not set. Add a repository secret named "
            "TRAFFIC_TOKEN with read access to repository traffic."
        )

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    views = api_get("traffic/views?per=day")
    clones = api_get("traffic/clones?per=day")
    referrers = api_get("traffic/popular/referrers")
    popular_paths = api_get("traffic/popular/paths")

    update_daily(views, clones)

    snapshot_date = datetime.now(timezone.utc).date().isoformat()
    replace_snapshot(
        "referrers.csv",
        REFERRER_FIELDS,
        snapshot_date,
        referrers,
        "referrer",
    )
    replace_snapshot(
        "popular_paths.csv",
        PATH_FIELDS,
        snapshot_date,
        popular_paths,
        "path",
    )

    print(f"Archived GitHub traffic for {REPOSITORY} on {snapshot_date}.")
    print(f"Data directory: {DATA_DIR}")


if __name__ == "__main__":
    main()
