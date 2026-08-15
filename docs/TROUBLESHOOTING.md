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

If some customer results were produced successfully, check the `customer_results` directory before reporting the failure. A partial review can still provide useful outputs even when the deeper Business Workflow and Risk Review needs attention.

For a reproducible hosted-analysis failure:

1. Record the UnvibeCode version with `python -m unvibecode --version`.
2. Record the repository size shown by the review command.
3. Note which customer results were produced successfully.
4. Open the referenced technical log and record the final error message.
5. Confirm that the repository path is correct and that the computer can reach the internet, then retry the review.
6. If the same failure occurs, preserve the analysis folder and include the sanitized error details when reporting the problem.

Do not upload generated reports containing source code, credentials, customer information, or other sensitive data.
