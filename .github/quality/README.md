# Repository Quality Checks

This folder keeps repository-maintenance files out of the project root while preserving automated checks for documentation and workflow packs.

It contains:

- `requirements.txt` for the quality-tool dependencies;
- `pyproject.toml` for Black and Pytest configuration;
- `.flake8` for lint configuration;
- `tests/test_repository_quality.py` for repository validation.

Run the complete local check from the repository root:

```bash
python -m pip install -r .github/quality/requirements.txt
python -m black --config .github/quality/pyproject.toml --check .github/quality/tests
python -m flake8 --config .github/quality/.flake8 .github/quality/tests
python -m pytest -c .github/quality/pyproject.toml .github/quality/tests
```

GitHub Actions runs the same commands for Python 3.11, 3.12, and 3.13.
