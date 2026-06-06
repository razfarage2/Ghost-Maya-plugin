# Stage 08 - Packaging & Installation Report

**Verdict**: Pass

## What Changed
- Created the main entry point `src/pose_ghost/launcher.py` which instantiates and wires together the `CompositionRoot`, `MayaEventBridge`, `MayaUiCommandsAdapter`, and `PoseGhostPanel`.
- Created `PoseGhost.mod` to allow Maya to recognize and map the plugin source path smoothly.
- Created metadata definitions in `src/pose_ghost/version.py`.
- Wrote the `install.md` and `uninstall.md` documentation, including a shelf button script.
- Authored a `test_load.py` integration script to strictly validate that the launcher initializes and correctly unloads without leaking any OpenMaya callbacks.

## The Logic According to Codex
The system uses `PoseGhost.mod` to inject the `src` folder into the `PYTHONPATH`. From there, the `pose_ghost.launcher` handles instantiating the entire decoupled architecture. To respect the strict boundaries, the `MayaUiCommandsAdapter`—which translates pure UI commands into Maya node actions—was placed directly in the launcher composition file, ensuring neither `ui` nor `maya_adapters` have to break rules to communicate. 

## What Bugs Could Happen
- If a user manually places `PoseGhost.mod` in a directory without properly modifying its internal relative path string, Maya will silently fail to find `pose_ghost.launcher`.

## How to Test
1. Run `& "C:\Program Files\Autodesk\Maya2024\bin\mayapy.exe" "work\08_packaging_installation\test_load.py"`
2. Verify all output logs print `[CONFIRMED]`.

## How This Relates to the Spec / Approved Decision
This fulfills the V1 delivery goal: a zero-install footprint python plugin that relies solely on Maya's standard `.mod` functionality and an intuitive shelf script, leaving Maya's environment clean upon unload.

## What Could be a V2 Improvement
- A standard PyPI package wrapper or an automated `.mll` installer/zipper for studios.
- Automatic shelf button creation on plugin load (using Maya's `maya.cmds.shelfButton`).

## Exact Tests/Checks Run
- Maya Integration Test (`test_load.py`): Validated `launcher.show()` and `launcher.unload()` in a headless Maya environment. (Pass)
- Previous Integration Tests (`test_integration.py`): Re-validated core logic. (Pass)
- Unit Tests: Re-validated core, runtime, and UI. (Pass)
- Import Boundary Checks: Validated boundaries post-packaging. (Pass)

## Pass/Fail Counts
- Maya Packaging Checks: 3 Passed / 0 Failed

## Files Changed
- `PoseGhost.mod` (Created)
- `docs/install/install.md` (Created)
- `docs/install/uninstall.md` (Created)
- `install/shelf_pose_ghost.py` (Created)
- `src/pose_ghost/launcher.py` (Created)
- `src/pose_ghost/version.py` (Created)
- `work/08_packaging_installation/test_load.py` (Created)
- `work/08_packaging_installation/output/packaging_report.md` (Created)

## Fresh Maya/mayapy Load Result
The module loaded completely error-free in `mayapy` standalone. The system correctly recognized `batch=True` and skipped Qt initialization to prevent a crash, demonstrating stable environment awareness. 

## Callback Cleanup/Unload Result
`launcher.unload()` successfully ran `root.lifecycle.shutdown()`. The callback registry length dropped to 0, confirming 100% callback cleanup with no hanging background tasks.

## Boundary Check Results
`All boundary checks passed.` The `MayaUiCommandsAdapter` was placed in the launcher composition file, so the `ui` and `maya_adapters` packages strictly maintained their mutual independence.

## Known Manual Validation Gaps Carried Forward
- **Graph Editor Tangent Handles**: Due to limitations in automated Maya batch testing, manipulating tangent handles in the Graph Editor without moving the key value was not programmatically verified. If ghosts fail to automatically update after a tangent edit, use the "Force Rebuild" button in the UI. 

## V1 Build Sequence Complete
**Yes.** The V1 Build Sequence is complete. The scaffold, core, runtime, adapters, UI, integration, and packaging are finished and passing.

## Owner Manual Maya Smoke Recommended Next
**Yes.** The final product is ready for Раз to boot up interactive Maya, run the shelf button, and test the onion-skinning interactive experience by hand!
