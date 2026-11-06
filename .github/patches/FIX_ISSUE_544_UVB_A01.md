# Fix for Issue #544 (UVB-A01)

fix(traversal): prevent infinite traversal recursion on NTFS directory junctions and symlinks

## Target File
`shipreadyv2/customer_runner.py`

## Unified Patch
See `03_issue_544_UVB_A01.patch`.

## Verification
- [x] Verified via `_audit/evidence/repros/wsa/repro_wsa_symlinks_and_junctions.py`.
- [x] Confirmed repository with junction loop is scanned exactly once with 1 node instead of 64 duplicate nodes.
- [x] Token estimation finishes deterministically without runaway token growth.
