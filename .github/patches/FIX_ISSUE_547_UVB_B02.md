# Fix for Issue #547 (UVB-B02)

fix(parsers/go): resolve same-package sibling struct definitions and emit internal edges

## Target File
`shipreadyv2/engine_sources/00a_shipreadyv2_fast_lane_v11_api_context_bundle.py`

## Unified Patch
See `06_issue_547_UVB_B02.patch`.

## Verification
- [x] Verified via `_audit/evidence/repros/wsb/test_go_same_package.py`.
- [x] Sibling Go file struct references now resolve and generate expected dependency edges in `connected-code.html`.
