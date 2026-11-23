# UnvibeCode Quick Start

The UnvibeCode Python package uploads eligible source files for hosted analysis and downloads the results to your computer. Hosted AI analysis uses our OpenAI API credentials. We will introduce bring-your-own-key support shortly, so you can use your own API credentials.

For a local-only Connected Code Map, fork the repository and use the graph source in `src/unvibecode_graph/`. No API key or source upload is needed for the local graph.

## Requirements

- Python 3.11 or newer
- Internet access for hosted business analysis
- Read access to the repository being reviewed

## Windows

Install UnvibeCode:

```powershell
python -m pip install --upgrade unvibecode
```

Review a repository:

```powershell
python -m unvibecode review --repository "D:\path\to\repository"
```

## macOS or Linux

Create a virtual environment and install UnvibeCode in it:

```bash
python3 -m venv ~/.venvs/unvibecode
source ~/.venvs/unvibecode/bin/activate
python3 -m pip install --upgrade unvibecode
```

Review a repository:

```bash
python3 -m unvibecode review --repository "/path/to/repository"
```

## What happens next

UnvibeCode displays live progress in the terminal. Completed HTML reports open automatically and all customer files are saved under:

```text
./unvibecode_results/
```

No activation key, customer OpenAI key, or `.env` file is required. Use `--output` to choose a different results folder.

We do not retain your uploaded source code or analysis results on our server after processing. Results are downloaded to your computer. OpenAI processes the AI requests under its own data policies.

Full workflow and risk analysis supports up to approximately two million estimated source tokens. Larger repositories receive graph and context outputs only, subject to [upload limits](LIMITATIONS.md).

## Continue reading

- [Understand the generated outputs](OUTPUTS.md)
- [See how the review works](HOW_IT_WORKS.md)
- [Resolve installation or runtime problems](TROUBLESHOOTING.md)

