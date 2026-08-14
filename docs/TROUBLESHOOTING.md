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

## A review stops with a `cl100k_base.tiktoken` error

The Business Workflow and Risk Review budgets its inputs with the `cl100k_base` token encoding. The first run downloads that encoding file from `openaipublic.blob.core.windows.net`. No OpenAI API key is required, but the host has to be reachable.

When a firewall or proxy blocks the host, the review stops and the terminal reports a reason similar to:

```text
403 Client Error: Forbidden for url: https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken
```

An unreachable proxy reports a `ProxyError` for the same URL. In both cases the Connected Code Map and Complete Repository Context are still produced.

Allow HTTPS access to `openaipublic.blob.core.windows.net` and run the review again.

For a machine that cannot reach the host, prepare the encoding cache once on a connected machine and copy the directory across. Set the cache directory, run any review to populate it, then copy the directory to the restricted machine and set the same variable there.

Windows:

```powershell
$env:TIKTOKEN_CACHE_DIR = "C:\unvibecode-tiktoken-cache"
python -m unvibecode review --repository "D:\flask"
```

macOS or Linux:

```bash
export TIKTOKEN_CACHE_DIR="$HOME/unvibecode-tiktoken-cache"
python3 -m unvibecode review --repository "/path/to/repository"
```

## Only the Connected Code Map was produced

Repositories above approximately two million estimated source tokens intentionally receive the Connected Code Map and Complete Repository Context without the deeper Business Workflow and Risk Review.

A smaller repository that produces only the Connected Code Map has failed rather than been skipped. Read the printed reason and `technical_logs/business_workflow_review.log` inside the analysis folder. A blocked `cl100k_base.tiktoken` download is one known cause.

## A review needs attention

The terminal prints the customer-facing reason and the technical-log location. Preserve the analysis folder when reporting a reproducible problem.

When opening an issue, remove source code, credentials, customer information, and other sensitive data from logs.

