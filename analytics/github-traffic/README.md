# GitHub traffic history

This directory is populated automatically by
`.github/workflows/archive-github-traffic.yml`.

The design intentionally uses a few append/upsert CSV files instead of creating
a new JSON file every day. That keeps Git history, file count, and long-term
storage small while preserving the useful traffic history.

## Files

- `daily.csv`
  - One row per UTC date.
  - Views, unique visitors, clones, and unique cloners.
  - Each run re-reads GitHub's available rolling window and upserts those dates,
    so recent values can be corrected if GitHub updates them.

- `referrers.csv`
  - Up to 10 rows per snapshot date.
  - Stores the ranked referring sites returned by GitHub.
  - These are snapshots of GitHub's rolling traffic window, not per-day source attribution.

- `popular_paths.csv`
  - Up to 10 rows per snapshot date.
  - Stores the ranked repository paths/pages returned by GitHub.
  - These are snapshots of GitHub's rolling traffic window, not per-day page attribution.

Re-running the workflow on the same UTC date replaces that date's referrer and
page snapshots instead of duplicating them.

## Required repository secret

Create a repository secret named `TRAFFIC_TOKEN`.

Use a fine-grained personal access token restricted to this repository with the
minimum repository permission required to read traffic metrics. The workflow
uses the normal GitHub Actions token only to commit the resulting CSV files.

The secret itself is never written to the repository.

## Manual run

Open **Actions → Archive GitHub traffic → Run workflow**.

After the workflow succeeds, the CSV files will appear in this directory and
will continue to grow automatically.
