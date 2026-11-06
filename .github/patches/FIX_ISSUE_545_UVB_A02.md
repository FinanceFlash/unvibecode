# Fix for Issue #545 (UVB-A02)

fix(traversal): support .gitignore parsing and pattern exclusion during repository scans

## Target File
`shipreadyv2/customer_runner.py`

## Unified Patch
See `04_issue_545_UVB_A02.patch`.

## Verification
- [x] Verified via `_audit/evidence/repros/wsa/repro_wsa_hidden_and_gitignore.py`.
- [x] Confirmed ignored files (`ignored_dir/secret_logic.py`, `config.secret.py`) are excluded from discovery and token estimates.
- [x] Zero sensitive/ignored files appear in generated context packages.
