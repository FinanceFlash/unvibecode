# Fix for Issue #552 (UVB-D02)

fix(context): record zero-byte files in skipped_files manifest to reconcile preflight counts

## Target File
`shipreadyv2/engine_sources/00a_shipreadyv2_fast_lane_v11_api_context_bundle.py`

## Unified Patch
See `11_issue_552_UVB_D02.patch`.

## Verification
- [x] Verified via `_audit/evidence/repros/wsd/repro_uvb_d02_zero_byte_files_desync.py`.
- [x] Manifest file counts (`source_files` + `skipped_files`) reconcile 100% with preflight token estimator.
