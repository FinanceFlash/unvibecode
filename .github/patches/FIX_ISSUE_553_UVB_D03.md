# Fix for Issue #553 (UVB-D03)

fix(context): align direct and extended context budget targets to advertised 45K and 75K limits

## Target File
`shipreadyv2/engine_sources/00a_shipreadyv2_fast_lane_v11_api_context_bundle.py`

## Unified Patch
See `12_issue_553_UVB_D03.patch`.

## Verification
- [x] Verified via `_audit/evidence/repros/wsd/repro_uvb_d03_context_budget_underfill.py`.
- [x] Context selection accumulator now fills up to the full advertised 45K and 75K token budgets.
