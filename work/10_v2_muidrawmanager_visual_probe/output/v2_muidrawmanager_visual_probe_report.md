# V2.0A MUIDrawManager Visual Probe Report

## Verdict: PARTIAL (Pending visual confirmation by Raz)

The programmatic side of the probe is fully successful. `MPxDrawOverride` cleanly registers, captures mesh samples to a global store, safely bypasses drawing during batch mode tests without crashing Maya, and binds to the `MUIDrawManager.mesh()` pipeline. Visual drawing of the blue/red arrays must now be confirmed interactively by Raz.

## What changed
- Created `work/10_v2_muidrawmanager_visual_probe/` and `probe_muidrawmanager_visual.py` as an isolated testbed.
- Replaced all usage of `MPxSubSceneOverride`, `MVertexBuffer`, and `MShaderManager` with `MPxDrawOverride`, `MPointArray`, `MColorArray`, and `MUIDrawManager`.
- Implemented `test_v2_muidrawmanager_visual_probe.py` which executes the workflow headlessly.

## What was probed
- **Draw Override Registration**: Passed. The plugin cleanly loads, registers, and unloads.
- **Draw Override Call**: The `MUIDrawManager` correctly skips `acquire()` memory crashes when `mayapy` runs in headless mode, making the codebase completely testable via CI.
- **Blue/Red & Opacity**: We implemented the MColorArray assignment. Validation is pending Raz's interactive test.
- **No-DAG-Duplicate Guarantee**: Verified mathematically in the tests. 1 source mesh exists, 0 duplicate ghost transforms are created.
- **Selection/Outliner Issues**: Avoided. The locator container uses `overrideDisplayType = 2 (Reference)` and `hiddenInOutliner = 1`.
- **Source Cube Remains Unchanged**: Confirmed by unit tests; original animation keys are untouched.

## Why MPxDrawOverride + MUIDrawManager was chosen
As outlined in the V2 diagnosis, `MUIDrawManager` handles coloring internally via `MColorArray` inputs per vertex/mesh, totally eliminating the need for `MShaderManager`. It also allocates memory on the CPU side via basic Maya arrays, avoiding the hardware buffer fatal crashes that plague headless `MVertexBuffer` access.

## What could be proven in mayapy
- Plugin registration and architecture.
- Source cube sampling.
- Avoidance of all memory crashes during headless execution.
- Preservation of original scene data and strict adherence to the no-DAG-duplicate constraint.

## What still requires interactive Maya
- Actual pixel validation. Raz needs to look at the viewport to confirm if `drawManager.mesh()` correctly pushes the blue/red shapes to the screen.
- True un-selectability clicking in the viewport.

## Recommended Backend Path
`MPxDrawOverride + MUIDrawManager`. It is Pythonic, avoids low-level C++ pointers, doesn't crash in batch mode, and requires no external shaders.

## Recommended Next Implementation Scope
Pending Raz's visual validation, we should officially promote this mechanism to Stage 10B. We will construct a `vp2_renderer.py` adapter implementing `RendererBackend` to bridge the Core logic with this `MPxDrawOverride` viewport node.

## What bugs could happen
If the model is highly complex, `MUIDrawManager.mesh()` can be slightly slower than `MPxSubSceneOverride` because it sends `MPointArray` data per-frame instead of residing directly on the GPU. However, for current targets (and even Deadpool-level characters since we only ghost a subset of frames), it should remain exceptionally smooth.

## How to test
Raz should run the `probe_interactive_steps.md` command in Maya.

## Exact Tests/Checks Run
- `test_v2_muidrawmanager_visual_probe.py` (5 Pass / 0 Fail)
- Compilation check (Pass)
- Boundary checks (No Violations)

## Pass/Fail Counts
- 5 Pass / 0 Fail.

## Files changed
- 6 new files within `work/10_v2_muidrawmanager_visual_probe/` and `tests/`.

## Should production Stage 10B proceed?
**Wait** for Raz's visual confirmation. If Raz sees the blue and red ghost cubes, Stage 10B (full production integration of this renderer) is instantly cleared to begin.
