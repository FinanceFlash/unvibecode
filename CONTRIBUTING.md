# Contributing to UnvibeCode

Thank you for helping improve UnvibeCode.

## Before proposing a change

- Search existing issues and pull requests.
- Keep each change focused on one problem.
- Do not include proprietary repositories, credentials, customer data, or generated customer results.
- Preserve customer-facing terminology and avoid exposing internal analysis stages in the CLI.

## Local development

Create and activate a Python 3.11-or-newer virtual environment, then install the project from the repository root:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pytest
```

Run tests:

```bash
python -m pytest
```

## Pull requests

A pull request should include:

- A clear explanation of the problem
- The implemented change
- Tests for changed behaviour
- Updated documentation when customer behaviour changes
- Confirmation that no secrets or generated customer data were committed

Analysis changes should preserve deterministic paths, customer-result filenames, large-repository behaviour, and existing CLI progress unless the pull request explicitly proposes a reviewed product change.

By contributing, you agree that your contribution is licensed under the repository's Apache License 2.0.

