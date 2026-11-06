# Fix for Issue #543 (UVB-D05)

fix(packaging): enable cross-platform import fallback for native extensions on Linux/macOS

## Target File
`shipreadyv2/cli.py`

## Unified Patch
See `02_issue_543_UVB_D05.patch`.

## Verification
- [x] Verified via `_audit/evidence/repros/wsd/repro_uvb_d05_cross_platform_wheel_lockin.py`.
- [x] Tested import behavior in simulated non-Windows POSIX environment: import succeeds without unhandled ModuleNotFoundError.
- [x] Fast Lane CLI command `py -m unvibecode --help` functions cleanly.
