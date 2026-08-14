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

## "403 Client Error: Forbidden" fetching `cl100k_base.tiktoken`

**Symptom**

The `Business Workflow & Risk Review` stage stalls or reports "needs attention"
with an error similar to:

```
403 Client Error: Forbidden for url: https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken
```

The `Connected Code Map for LLMs` stage still completes normally, since it
runs entirely locally.

**Cause**

UnvibeCode uses the `tiktoken` library to estimate token counts before
sending context to the hosted review service. On first use, `tiktoken`
downloads its encoding file from
`openaipublic.blob.core.windows.net`. Corporate proxies, VPNs, and locked-down
CI/sandbox networks commonly block this domain even when the main UnvibeCode
API host is reachable, which surfaces as a 403 instead of a clearer
network-configuration message.

**Fix**

1. Confirm your network allowlist includes `openaipublic.blob.core.windows.net`
   in addition to UnvibeCode's own API host, then re-run the review.
2. If you can't allowlist that domain, pre-download the encoding file once
   from a machine that has access, then point `tiktoken` at a local cache
   directory:

   ```bash
   export TIKTOKEN_CACHE_DIR=/path/to/cache
   ```

   Copy the cached file from the working machine's cache directory (same env
   var) into that path before running `unvibecode review` on the restricted
   network.
3. Re-run `python -m unvibecode review --repository "/path/to/repository"`.
   The Connected Code Map and Complete Repository Context outputs from the
   earlier run are unaffected and do not need to be regenerated.

If the error persists after allowlisting or caching, open a GitHub issue with
your OS, Python version, and the full `technical_logs/business_workflow_review.log`
output (with any repository-specific paths redacted).
