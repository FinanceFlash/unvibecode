# Fix for Issue #542 (UVB-B01)

fix(parsers/go): resolve collection return types (slice, map, chan) in Go Tree-sitter adapter

## Target File
`shipreadyv2/engine_sources/00a_shipreadyv2_fast_lane_v11_api_context_bundle.py`

## Unified Patch
See `01_issue_542_UVB_B01.patch`.

## Verification
- [x] Verified via standalone reproduction script `_audit/evidence/repros/wsb/test_go_slice_return.py`: `ListItems()` returning `[]*Item` now correctly extracts `Item` return type, resolves receiver method `item.Process()`, and creates dependency edge `service/runner.go` -> `api/catalog.go`.
- [x] Tested against `gin-gonic/gin` v1.10.0: collection returns (`RoutesInfo`, `HandlersChain`) now correctly populate Connected Code Map without dropped edges.
- [x] Existing test suite passes with 0 regressions.
