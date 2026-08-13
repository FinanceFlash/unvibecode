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

If the terminal shows `403 Client Error` for `openaipublic.blob.core.windows.net`, or `Host not in allowlist` for `shipready-api.alphashots.ai`, your network is blocking specific hosts UnvibeCode needs rather than blocking all outbound traffic. Ask your network administrator to allow HTTPS access to:

- `openaipublic.blob.core.windows.net` (tokenizer data)
- `shipready-api.alphashots.ai` (business workflow and risk review)

Re-run the same command after access is allowed;
UnvibeCode does not need to be reinstalled.

## Only the Connected Code Map was produced

Repositories above approximately two million estimated source tokens intentionally receive the Connected Code Map and Complete Repository Context without the deeper Business Workflow and Risk Review.

## A review needs attention

The terminal prints the customer-facing reason and the technical-log location. Preserve the analysis folder when reporting a reproducible problem.

When opening an issue, remove source code, credentials, customer information, and other sensitive data from logs.

