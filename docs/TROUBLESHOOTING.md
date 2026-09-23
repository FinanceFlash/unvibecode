# Troubleshooting UnvibeCode

Start with the [README setup instructions](../README.md#try-unvibecode). Use the same Python command and environment to install and run UnvibeCode.

## Check installation on Windows

Run these commands in PowerShell, replacing the repository path:

```powershell
py --version
py -m pip install --upgrade unvibecode
py -m unvibecode --help
py -m unvibecode review --repository "D:\path\to\repository"
```

Python 3.11 or newer is required. If you use a virtual environment, activate it and use that environment's Python consistently for installation and execution.

## Check installation on macOS or Linux

Run these commands in your terminal, replacing the repository path:

```bash
python3 --version
python3 -m pip install --upgrade unvibecode
python3 -m unvibecode --help
python3 -m unvibecode review --repository "/path/to/repository"
```

## “No module named unvibecode”

The package may be installed in a different Python environment. Run the installation and help commands above using the same interpreter.

Check which package that interpreter sees:

- Windows: `py -m pip show unvibecode`
- macOS or Linux: `python3 -m pip show unvibecode`

If you are using a virtual environment, use its Python for both commands. Do not switch interpreters between installing and running.

## “py”, “python” or “python3” is not recognized

Install Python 3.11 or newer and reopen your terminal. Check that the command you intend to use is available. On Windows, if `py` is unavailable but `python --version` identifies the intended Python installation, use `python` consistently in place of `py`.

## Repository path not found

Point `--repository` at an existing local repository folder, not a GitHub URL or ZIP file. Clone or extract the repository first. Quote the full path, especially when it contains spaces, and check that your account can read it.

## Hosted analysis cannot connect

Workflow and risk analysis require internet access. Check your connection and whether your network permits HTTPS access to the hosted UnvibeCode service. Follow the terminal's error message; if an organizational restriction is involved, contact your network administrator.

No activation key or customer OpenAI API key is required. See [Data processing and privacy](DATA_PROCESSING.md).

## Only Connected Code and LLM Context are available

Repositories above approximately two million estimated source tokens receive these two outputs without the deeper Business Workflow and Risk Review. See [repository limits](LIMITATIONS.md).

For other cases, check the terminal and report status for a skipped, failed or incomplete stage. Missing workflow or risk output is not a no-findings result.

## The report does not open automatically

Open the generated results folder and double-click `00_unvibecode_results.html`. The [quick start](QUICKSTART.md) documents the results location as `shipready_results/analysis_<timestamp>/customer_results/`.

Use the latest completed review folder. Keep the entry file and its companion reports together.

## A report tab is blank or says “file not found”

The entry page loads separate HTML files. Moving only the entry page breaks those links.

Keep the complete results folder together, including:

- `01_connected_code_map_for_llm.html`
- `02_business_workflow_map.html`
- `03_business_risk_findings.html`
- `complete_repository_context_for_llm.zip`
- Any companion folders such as `_support/`

If a referenced file was never generated, check the review status rather than substituting a report from a different run.

## The map opens but context download does not work

Select a file in Connected Code, choose Narrow, Optimal or Wider, then use the download control. Check whether your browser blocked the download.

If the selection or download controls do not respond, check that the companion files are present. In the smolagents sample, context selection uses `_support/fast_lane_context_store.js`. Keep it with the matching map and ZIP from the same report set.

## My assistant cannot read the HTML or ZIP

Provide the relevant report file, not only the entry page that loads it. For a smaller code question, download focused context from Connected Code.

If your assistant cannot accept the ZIP, extract it, read the included README and provide the relevant files in a supported format. Use Narrow context or fewer files if the input exceeds the assistant's limit.

## The sample still shows an older report

Open the [current smolagents report](https://financeflash.github.io/unvibecode/gitdocs/smolagents/smolagents-main-unvibecode-analysis.html#business-workflows). It contains **30 workflows across 15 areas**.

Refresh the page or try a private browser window. If you maintain a published copy, confirm that its deployment contains the complete matching report set; changing the heading alone does not replace the workflows displayed inside it.

## What to include when requesting help

Provide your operating system, Python version, UnvibeCode version from `pip show`, repository language/framework, exact command, sanitized error message and the stage or tab that failed. Preserve the results folder and any technical-log location printed by the terminal.

Remove credentials, proprietary code and customer information before sharing logs or reports publicly.

- [GitHub issues](https://github.com/FinanceFlash/unvibecode/issues): reproducible problems and feature requests.
- [divya.singaravelu@iiml.org](mailto:divya.singaravelu@iiml.org): product questions, public-repository review requests and collaboration.
