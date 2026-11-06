# Fix for Issue #550 (UVB-C02)

fix(compiler): prevent state transition misattribution in multi-resource workflow groups

## Target File
`shipreadyv2/engine_sources/04_shipreadyv2_business_path_compiler.py`

## Unified Patch
See `09_issue_550_UVB_C02.patch`.

## Verification
- [x] Verified via `_audit/evidence/repros/wsc/repro_wsc_transition_resource_misattribution.py`.
- [x] Transitions correctly reflect their specific resource owners.
