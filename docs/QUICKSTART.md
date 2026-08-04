# UnvibeCode Quick Start

UnvibeCode reviews a repository from the command line and saves customer-ready results locally.

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

Install UnvibeCode:

```bash
python3 -m pip install --upgrade unvibecode
```

Review a repository:

```bash
python3 -m unvibecode review --repository "/path/to/repository"
```

## What happens next

UnvibeCode displays live progress in the terminal. Completed HTML reports open automatically and all customer files are saved under:

```text
./shipready_results/analysis_<timestamp>/customer_results/
```

No activation key, customer OpenAI key, or `.env` file is required.

## Continue reading

- [Understand the generated outputs](OUTPUTS.md)
- [See how the review works](HOW_IT_WORKS.md)
- [Resolve installation or runtime problems](TROUBLESHOOTING.md)

