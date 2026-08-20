# Troubleshooting UnvibeCode

## `No module named unvibecode`

UnvibeCode was probably installed into a different Python environment from the one used to run it.

Windows:

```powershell
python -m pip install --upgrade --force-reinstall unvibecode
python -m unvibecode --help
```

macOS or Linux:

```bash
python3 -m pip install --upgrade --force-reinstall unvibecode
python3 -m unvibecode --help
```

## `python` or `python3` is not recognized

Install Python 3.11 or newer and ensure the selected Python command is available in the terminal. Use the same Python command for installation and execution.

## Repository path not found

Confirm that the path exists and quote paths containing spaces.

Windows:

```powershell
python -m unvibecode review --repository "D:\Projects\My Repository"
```

macOS or Linux:

```bash
python3 -m unvibecode review --repository "/Users/example/My Repository"
```

## Hosted analysis cannot connect

Confirm that the computer has internet access and that organizational firewall rules allow HTTPS access to the hosted UnvibeCode service.

## Only the Connected Code Map was produced

Repositories above approximately two million estimated source tokens intentionally receive the Connected Code Map and Complete Repository Context without the deeper Business Workflow and Risk Review.

## A review needs attention

The terminal prints the customer-facing reason and the technical-log location. Preserve the analysis folder when reporting a reproducible problem.

When opening an issue, remove source code, credentials, customer information, and other sensitive data from logs.

## Business Workflow & Risk Review fails with `ResultValidationError: unknown connected_node_ids`

The terminal may report something like:

```text
Business Workflow & Risk Review needs attention.
Reason: Step 03 produced no usable results: completion=FAILED, successful=0, failed=1;
last request error=ResultValidationError: path_2_..._: unknown connected_node_ids ['chunk_xxxxxxxxxxxxxxx']
```

This does not necessarily mean the referenced code is missing from your repository. In an
observed case, the flagged chunk ID differed from a real chunk ID already present in the same
run's `shipreadyv2_semantic_packs.jsonl` by a single trailing character (for example
`chunk_8b348a2b7f8896c` vs. the actual `chunk_8b348a2b7f8896c2`). The same chunk was cited
correctly elsewhere in the same generated result, so the underlying code was not missing or
unresolved -- one field in the structured output did not match.

Before assuming a repository or connectivity problem, check whether this is the cause:

1. Open `<run_folder>/shipreadyv2_pass1_full_artifacts/<request_id>/attempt_1/error.json` to get
   the exact unknown chunk ID.
2. Search `shipreadyv2_semantic_packs.jsonl` (or `shipreadyv2_llm_feed.jsonl`) in the same run
   folder for that ID.
   - If it is genuinely absent everywhere, this may point to a different underlying issue --
     preserve the run folder and see "A review needs attention" above for what to include when
     reporting it.
   - If a near-identical ID exists (differing by one or a few trailing characters), compare it
     against `attempt_1/raw_response.json` or `attempt_1/normalized_result.json` in the same
     folder -- the same ID is often used correctly elsewhere in that file, confirming the
     underlying code was understood correctly and only one field diverged.

Re-running the review will generate a fresh request and may not reproduce the same mismatch.
