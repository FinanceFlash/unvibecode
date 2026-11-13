# Fix for Issue #781 (UVB-CLI01, self-assigned)

fix(cli): print and persist the hosted job id at submit time (#781)

## Target File
- `unvibecode/cli.py` (pip package `unvibecode` 0.4.0; the CLI source ships only in the PyPI wheel, so this patch is against the installed module)

## Unified Patch
See `15_issue_781_UVB_CLI01.patch`.

## Root cause
In `main()`, after `submit()` returns, the job id is validated but never printed or
stored. It only appears in the two graceful terminal handlers (`STOPPED`, ~65-minute
deadline). An ungraceful exit - SIGKILL, power loss, SSH drop - skips those
handlers, so the id is lost and `unvibecode resume` / the interim download endpoint
can never be used. The run's results become unreachable from the client.

## Change
Immediately after job-id validation, when the command is `review`:
1. Print `Job started: <id> - resume with: unvibecode resume <id>` (flushed, so it survives a kill).
2. Persist the id to `<output>/.unvibecode-job`, guarded by `try/except OSError`.

The print comes first, so the recovery path survives even when persistence fails.
If the output folder cannot be created or written (read-only parent, path exists as
a file), the guard catches the `OSError`, prints a warning naming the job id, and
the review continues polling - without the guard, a successful remote submission
would turn into a local `[STOPPED]` failure before the first status poll.

Marker semantics: the marker holds the most recently submitted job id for that
output folder (a second `review` overwrites it). A second review into a non-empty
output folder still stops at download under the pre-existing "report folder already
exists" collision rule - unchanged by this patch. The marker filename cannot
collide silently with report contents: `download()` raises when an extracted item
meets a pre-existing path not written by an earlier download step.

## Verification
`test_issue_781_job_recovery.py` - fully offline; fake API server on 127.0.0.1 via
the documented `UNVIBECODE_API_URL` override; the real CLI runs as a subprocess.
Four scenarios, run against pristine 0.4.0 and the patched module:

| test | pristine 0.4.0 | patched |
|---|---|---|
| kill_then_resume: SIGKILL mid-run, then `resume <saved id>` | FAIL - id neither printed nor persisted; nothing to resume with | PASS - exact resume line printed, marker saved, resume exits 0 and downloads the report |
| graceful_completion | PASS (rc 0, report downloaded) | PASS (rc 0, report downloaded, line printed, marker saved) |
| readonly_output: unwritable output dir after successful submit | n/a (nothing to persist) | PASS - CLI keeps polling, prints the resume line plus a warning, no crash |
| repeated_reviews: second review into same output folder | stops at download on the pre-existing collision rule | PASS - same collision behavior; marker holds the latest submitted job id |

- [x] Bug reproduced on unpatched 0.4.0 (SIGKILL: `id_printed=False, id_persisted=False`).
- [x] Recovery proven end to end on the patched CLI: the id saved before the kill resumes the run and downloads the report.
- [x] Persist failures cannot strand a submitted run (guarded write; printed recovery line retained).
- [x] The two install trees used for the matrix differ only in `cli.py` (`diff -rq`).
