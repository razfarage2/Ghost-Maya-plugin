# Pose Ghost V1 Hotfix 01: UI Target Scan Wiring Report

**Verdict**: Pass

## What Changed
- Fixed a method name mismatch in `src/pose_ghost/launcher.py`. 
- Changed `TargetScanner.scan_hierarchy(path)` to the correct API `TargetScanner.scan_target_root(path)`.
- Added a new regression test `tests/maya_integration/test_ui_scan_wiring.py` to validate that the UI command adapter correctly populates the target lists.

## Root Cause
During the UI commands adapter creation, the scanner method was typed as `scan_hierarchy`, but the actual method in `TargetScanner` was named `scan_target_root`. This typo caused a hard crash when the `Scan` button was pressed in the UI because the UI adapter could not find the method.

## The Logic According to Codex
The UI adapter uses duck typing to bridge the UI interface with the Maya adapters. The launcher implements this bridge explicitly. By fixing the method name, the bridge correctly passes the `root_path` string to the `TargetScanner`, returns a list of target node paths, and maps them to `TargetRowData` items for the `ObjectListModel`.

## What Bugs Could Happen
- If the `TargetScanner` implementation changes its method signature (e.g., adding a required argument), the UI adapter will crash again. Python's dynamic typing does not catch this at compile-time, so the regression integration test provides safety.

## How to Test
1. Run `& "C:\Program Files\Autodesk\Maya2026\bin\mayapy.exe" "tests\maya_integration\test_ui_scan_wiring.py"`
2. It should print `OK`.

## How This Relates to the Spec / Approved Decision
This enforces the clean architecture requirement where the UI layer (`ObjectListModel`) does not talk directly to Maya APIs. The `launcher` acts as the integration point, correctly wiring `scan_target_root` without polluting the UI with Maya imports.

## What Could be a V2 Improvement
- Add type-hint stubs (e.g., `.pyi` files) or use `Protocol` enforcement in a way that static analysis (like `mypy`) can catch missing/misnamed methods on `TargetScanner` before runtime.

## Exact Tests/Checks Run
- Maya Integration Test (`test_ui_scan_wiring.py`): Validated UI target list population. (Pass)
- Maya Integration Test (`test_renderer.py`): Re-validated renderer logic. (Pass)
- Maya Integration Test (`test_integration.py`): Re-validated core evaluation mechanics. (Pass)
- Maya Integration Test (`test_load.py`): Re-validated launcher headless init. (Pass)
- Python Unit Tests: Re-validated core, runtime, and UI. (48 Passed / 0 Failed)
- Import Boundary Checks: Validated boundaries post-fix. (Pass)
- Python Compile Checks: Re-compiled successfully. (Pass)

## Pass/Fail Counts
- Maya Packaging Checks: 4 Passed / 0 Failed

## Files Changed
- `src/pose_ghost/launcher.py` (Modified)
- `tests/maya_integration/test_ui_scan_wiring.py` (Created)
- `work/08_packaging_installation/output/pose_ghost_v1_hotfix01_ui_target_scan_wiring_report.md` (Created)

## Exact Scanner API Before and After
- **Before**: `TargetScanner.scan_hierarchy(path)` (Did not exist)
- **After**: `TargetScanner.scan_target_root(path)` (Correctly mapped to `TargetScanner.scan_target_root(root_path: str, exclude_pose_ghost_nodes: bool = True)`)

## Proof that UI Command Path Can Scan a Cube Group
The regression test creates a `polyCube` under a `group`. The `app.ui_adapter.scan_target_root(grp)` command successfully extracts `|testGrp|testCube` from the group hierarchy.

## Proof that Target List is No Longer Empty After Scan
The regression test asserts `len(app.ui_adapter.current_targets) > 0` and `len(app.ui_model._rows) > 0`. Both pass successfully, proving the UI receives the populated list and the controller receives the target strings for Force Rebuild.

## Proof that Existing Tests Still Pass
All Stage 05, Stage 07, and Stage 08 tests completed successfully with `[CONFIRMED]` output using `mayapy.exe`.

## Boundary Check Results
`All boundary checks passed.` The `launcher` correctly bridges the gap without making the UI import Maya directly.

## Interactive Maya Smoke Retry Recommended
**Yes.** Please boot up interactive Maya again, load the plugin, and press the `Scan` button! The target list should now populate cleanly and `Force Rebuild` should generate ghosts.
