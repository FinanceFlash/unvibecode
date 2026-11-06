# Fix for Issue #549 (UVB-C01)

fix(compiler): prioritize canonical lifecycle stage over source line in workflow display sorting

## Target File
`shipreadyv2/engine_sources/04_shipreadyv2_business_path_compiler.py`

## Unified Patch
See `08_issue_549_UVB_C01.patch`.

## Verification
- [x] Verified via `_audit/evidence/repros/wsc/repro_wsc_lifecycle_ordering.py`.
- [x] Ingestion handlers now deterministically sort before execution and delivery handlers in `business_workflow_context.html`.
