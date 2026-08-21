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

## `UnicodeEncodeError` on Windows

Windows terminals use CP1252 encoding by default. UnvibeCode displays progress bars and status characters that CP1252 cannot represent, causing Python to crash immediately:

```
UnicodeEncodeError: 'charmap' codec can't encode characters in position 81-100:
character maps to <undefined>
```

**Workaround:** Set the terminal encoding to UTF-8 before running UnvibeCode.

PowerShell:

```powershell
$env:PYTHONIOENCODING="utf-8"
python -m unvibecode review --repository "D:\path\to\repository"
```

Command Prompt:

```cmd
set PYTHONIOENCODING=utf-8
python -m unvibecode review --repository "D:\path\to\repository"
```

To make this permanent, add `PYTHONIOENCODING` as a system environment variable set to `utf-8`.

This limitation is tracked in [issue #53](https://github.com/FinanceFlash/unvibecode/issues/53).

## Analysis produces zero results on Windows despite progress reaching 60–70%

Windows has a default path-length limit of 260 characters. UnvibeCode creates deeply nested output folders during analysis. When the repository path is long, the total file path can exceed this limit, causing intermediate files to silently fail to be created. The analysis appears to run but produces zero business-risk findings.

The hidden error in the log files is:

```
FileNotFoundError: [Errno 2] No such file or directory:
'C:\Users\...\attempt_1\raw_response.json.tmp'
```

**Workaround:** Move the repository (or run UnvibeCode from) a short base path. For example:

```powershell
$env:PYTHONIOENCODING="utf-8"
cd C:\Users\YourName\uv
python -m unvibecode review --repository "C:\Users\YourName\uv\my-repo"
```

Alternatively, enable long paths system-wide in Windows 10/11:

```powershell
# Run PowerShell as Administrator
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

After enabling long paths, restart the terminal and re-run the review.

This limitation is tracked in [issue #53](https://github.com/FinanceFlash/unvibecode/issues/53).
