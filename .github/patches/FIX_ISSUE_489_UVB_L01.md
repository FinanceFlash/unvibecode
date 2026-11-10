# Fix for Issue #489 (UVB-L01)

fix(linker): require re-export provenance in LinkerResolutionModule (#489)

## Target Files
- `shipreadyv2/engine_sources/00a_shipreadyv2_fast_lane_v11_api_context_bundle.py`
- `shipreadyv2/engine_sources/01_shipreadyv2_merged_graph_pipeline_5chunks.py`

## Unified Patch
See `14_issue_489_UVB_L01.patch`.

## Verification
- [x] Verified via minimal reproduction: Python route import (`backend/main.py` -> `backend/routes.py`) is no longer hijacked by unrelated frontend TypeScript (`frontend/router.ts`).
- [x] Language family guard permits valid cross-extension re-exports within same ecosystem (e.g., `.ts` <-> `.tsx`, `.js` <-> `.jsx`, `.py` <-> `.pyw`).
- [x] Provenance verification verifies `imports` list on `existing_path` node before binding speculative `unique_symbol_via_resolved_module`.
- [x] Unverified candidate re-exports cleanly fall back to `_unresolved_symbol(symbol, "reexport_target_unverified", candidate_paths)`.
