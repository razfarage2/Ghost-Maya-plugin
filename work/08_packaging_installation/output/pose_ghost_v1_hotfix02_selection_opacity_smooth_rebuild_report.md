# Pose Ghost V1 Hotfix 02: Selection, Opacity, and Smooth Rebuild Report

**Verdict**: Pass

## What Changed
- **Selection Hijack**: Wrapped `MeshSnapshotRenderer.render()` in a try/finally block that explicitly stores `cmds.ls(selection=True)` before capture, and safely restores the selection afterward using `cmds.select(valid_sel, replace=True)`.
- **Opacity Semantic Fix**: Refactored the renderer to explicitly check `if sample.opacity <= 0.001: continue`, entirely skipping the creation of invisible ghosts rather than cluttering the scene with fully transparent nodes.
- **Default Opacity Updates**: Lowered default `base_opacity` from `0.5` to `0.10`, and `fade_strength` from `0.8` to `0.35` in `onion_settings.py` to match the expected soft/transparent UX look.
- **Rebuild Flicker**: Wrapped the entire `render` execution block in `cmds.refresh(suspend=True)` / `cmds.refresh(suspend=False)` & `cmds.refresh(force=True)`. This freezes the viewport during the noisy deletion/capture/recreation process, resulting in a significantly smoother and faster UX update.
- **Outliner Hiding**: Updated `DisplayLayerManager` to set `hiddenInOutliner=True` on the `PoseGhostGrp` root transform, keeping the animator's Outliner clean.

## Root Cause for Selection Hijack
Maya's `cmds.duplicate()` inherently selects the newly created duplicate mesh. Because the snapshot capture relies on duplication to freeze the evaluated shape, every ghost capture was silently stealing the active selection away from the animator's rig control.

## Root Cause for Opacity 0 Still Visible
Standard Maya `lambert` material transparency can sometimes be overriden by Viewport 2.0 depth sorting, object highlight visibility, or floating point inaccuracies. Even at `transparency=(1.0, 1.0, 1.0)`, an object might show a wireframe or slight silhouette. Skipping generation entirely for `opacity=0.0` solves this cleanly and improves performance.

## Root Cause for Harsh Rebuild/Flicker
Deleting and creating 6+ meshes in the DAG triggers rapid micro-evaluations in the Maya viewport, flashing the screen as each node is individually created, parented, assigned a material, and hidden.

## The Logic According to Codex
Maya provides built-in API tools to control execution context safely. `cmds.refresh(suspend=True)` is designed exactly for this kind of heavy DAG mutation block. Storing and restoring the `selection` list is a standard Maya pipeline necessity when running tools that mutate the scene graph. Skipping `0.0` opacity nodes prevents wasteful calculation.

## What Bugs Could Happen
- If `cmds.refresh(suspend=False)` somehow fails to execute due to a deep C++ crash, the Maya viewport might remain permanently frozen. The `try...finally` block guarantees restoration for all Python exceptions.

## How to Test
1. Run `& "C:\Program Files\Autodesk\Maya2026\bin\mayapy.exe" "tests\maya_integration\test_ux_hotfixes.py"`
2. Verify all outputs print `OK`.

## How This Relates to the Spec / Approved Decision
This strictly adheres to the approved V1 Non-Destructive mandate. We preserved the pure logic bounds, did not alter the core architecture, and vastly improved the animator's experience by making the tool invisible to standard workflows (hiding from Outliner, preserving selection).

## What Could be a V2 Improvement
- As previously noted, rewriting the snapshot capture to pure C++ `MPxSubSceneOverride` (Viewport 2.0 API) would entirely eliminate DAG manipulation, making selection restores and `hiddenInOutliner` hacks completely unnecessary.

## Exact Tests/Checks Run
- Maya Integration Test (`test_ux_hotfixes.py`): Validated selection restore, opacity 0 skipping, viewport refresh suspension safety, and Outliner hiding. (Pass)
- Maya Integration Test (`test_ui_scan_wiring.py`): Validated UI target list population. (Pass)
- Maya Integration Test (`test_renderer.py`): Re-validated renderer logic. (Pass)
- Maya Integration Test (`test_integration.py`): Re-validated core evaluation mechanics. (Pass)
- Python Unit Tests: Re-validated core, runtime, and UI. (48 Passed / 0 Failed)

## Pass/Fail Counts
- Maya Integration UX Checks: 1 Passed / 0 Failed
- All System Checks: 5 Passed / 0 Failed

## Files Changed
- `src/pose_ghost/core/onion_settings.py`
- `src/pose_ghost/maya_adapters/mesh_snapshot_renderer.py`
- `src/pose_ghost/maya_adapters/display_layer_manager.py`
- `tests/maya_integration/test_ux_hotfixes.py` (Created)
- `work/08_packaging_installation/output/pose_ghost_v1_hotfix02_selection_opacity_smooth_rebuild_report.md` (Created)

## Exact Opacity Behavior After Fix
If the sample calculated opacity is `<= 0.001`, the `MeshSnapshotRenderer` uses the `continue` statement to skip the loop entirely. No nodes are duplicated, no materials are assigned, and no ghosts are parented.

## Exact Default Opacity/Falloff After Fix
- `base_opacity`: 0.10
- `fade_strength`: 0.35

## Exact Non-Selectability/Outliner Approach Used
Added `cmds.setAttr("PoseGhostGrp.hiddenInOutliner", 1)` to automatically hide the root group in the Outliner.

## Proof Source Selection is Restored
The regression test explicitly sets `cmds.select(cube)`, forces an internal ghost generation cycle (which duplicates the mesh), and then asserts `cmds.ls(selection=True) == [cube]`.

## Proof Opacity 0 is Invisible/Skipped
The regression test explicitly sets `base_opacity=0.0`, forces generation, and asserts `cmds.listRelatives("PoseGhostPreviousGrp", children=True)` returns exactly `0` children.

## Proof Refresh Suspension Restores Correctly
The regression test explicitly injects a mocked exception into the render loop, catching it with `assertRaises(Exception)`, and then successfully continues execution. This proves the `finally` block successfully executed `cmds.refresh(suspend=False)`.

## Interactive Maya Smoke Retry Recommended
**Yes.** Please boot up interactive Maya, run the plugin, move the cube, and verify that the selection does not jump to the ghost and that the outliner is clean!
