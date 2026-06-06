# Stage 05 - Mesh Snapshot Renderer Report

**Verdict**: Pass

## What Changed
- Created the Maya adapters layer in `src/pose_ghost/maya_adapters` to handle all scene mutation and mesh snapshot logic.
- Implemented `EvaluatedSnapshotCapture` to duplicate meshes at requested frames while preserving world-space positions.
- Implemented `MeshSnapshotRenderer` to coordinate generating and sorting ghosts into Previous/Next groups.
- Implemented `MaterialManager` to create and assign blue/red transparent lambert materials.
- Implemented `TargetScanner` to locate visible, non-intermediate mesh shapes while excluding Pose Ghost nodes.
- Implemented `SceneProfileStore`, `ObjectBypassStore`, and `ProxySourceResolver` as specified.
- Wrote a robust `test_renderer.py` Maya integration script to prove source safety and exact world-space preservation.

## The Logic According to Codex
The `maya_adapters` package translates the agnostic, pure-Python logic of the `core` into actual Maya commands. It receives a `SamplePlan` defining what frames need ghosts, captures them using `cmds.duplicate` with time shifting and dependency graph evaluation, creates the necessary groups and materials, and parents the snapshots cleanly. This enforces the separation of concerns: core knows *what* to draw, adapters know *how* to draw it.

## What Bugs Could Happen
- Extremely complex rigs with aggressive evaluation locks or viewport-only deformers might resist the batch `currentTime` evaluation, resulting in ghosts that don't match the viewport exactly.
- Re-parenting complex geometry with constrained components might yield artifacts if `returnRootsOnly` doesn't completely sever internal rig dependencies not caught by the `listConnections` pass.

## How to Test
1. Start an interactive Maya or run via batch.
2. In batch: `& "C:\Program Files\Autodesk\Maya2024\bin\mayapy.exe" "work\05_mesh_snapshot_renderer\test_renderer.py"`
3. Confirm all 6 test sections output `"status": "confirmed"`.

## How This Relates to the Spec / Approved Decision
This fulfills the V1 multi-sample relative-frame onion skinning spec by generating actual mesh copies. It adheres strictly to the rule of preserving the original rig without mutation. The use of display layers, non-renderable flags, and dedicated groups matches the target Maya scene organization requested.

## What Could be a V2 Improvement
- A V2 renderer could use `maya.api.OpenMaya.MFnMesh` to extract the evaluated vertex data directly and push it into a transient shape node or Viewport 2.0 override (MUserRenderOperation) without ever touching `cmds.duplicate`. This would be faster and leave no DAG footprint.
- Decimation logic (e.g., using a proxy mesh or Maya's polyReduce) to speed up high-res geometry snapshots.

## Exact Tests/Checks Run
- Maya Integration Test (`test_renderer.py`): 6 sub-tests validating scanner, capture independence, full render logic, bypass, proxy, and profile store. (Pass)
- Boundary Check: Ran Python script to scan all `src/pose_ghost/runtime` and `src/pose_ghost/core` files for banned framework and adapter imports. (Pass)
- Compile Checks: Syntax validation across the `maya_adapters` package. (Pass)

## Pass/Fail Counts
- Maya Integration Tests: 6 Passed / 0 Failed
- Import Boundary Checks: 1 Passed / 0 Failed

## Files Changed
- `src/pose_ghost/maya_adapters/__init__.py` (Created)
- `src/pose_ghost/maya_adapters/display_layer_manager.py` (Created)
- `src/pose_ghost/maya_adapters/evaluated_snapshot_capture.py` (Created)
- `src/pose_ghost/maya_adapters/material_manager.py` (Created)
- `src/pose_ghost/maya_adapters/mesh_snapshot_renderer.py` (Created)
- `src/pose_ghost/maya_adapters/mesh_target_adapter.py` (Created)
- `src/pose_ghost/maya_adapters/object_bypass_store.py` (Created)
- `src/pose_ghost/maya_adapters/proxy_source_resolver.py` (Created)
- `src/pose_ghost/maya_adapters/scene_profile_store.py` (Created)
- `src/pose_ghost/maya_adapters/target_scanner.py` (Created)
- `work/05_mesh_snapshot_renderer/test_renderer.py` (Created)
- `work/05_mesh_snapshot_renderer/output/renderer_report.md` (Created)

## Exact Snapshot Capture Approach Chosen
The capture approach sets `cmds.currentTime(frame, update=True)`, explicitly forces DG evaluation by querying `worldMatrix[0]`, duplicates the mesh using `cmds.duplicate(returnRootsOnly=True)`, explicitly unlocks and severs all transform incoming connections to isolate the ghost from the source rig, parents it to the world, and restores the original time.

## Exact Non-Renderable Flags/Attributes Used
Ghosts have `castsShadows`, `receiveShadows`, and `primaryVisibility` set to 0. They also have `overrideEnabled=1` and `overrideDisplayType=2` (Reference) so they cannot be accidentally selected by the animator.

## Exact Material Transparency Approach Used
Since standard lambert materials share transparency across all assigned objects, we generate a unique material for each sample index (e.g., `PoseGhostPreviousMat_1`, `PoseGhostPreviousMat_2`). We set `color` to blue/red and `transparency` to `(1.0 - opacity)` for R, G, and B.

## Proof of Source Safety
The `test_renderer.py` test suite explicitly queries `cmds.listConnections(cmds.listHistory(cube, future=True), type='shadingEngine')` and `cmds.keyframe(..., query=True)` before and after the renderer generates and cleans up ghosts. The tests pass, proving zero material mutation and zero keyframe mutation.

## Proof of World-Space Preservation
The `test_renderer.py` animates a source object to `tx=10.0` at frame 10. While at frame 1 (where `tx=0.0`), it captures a snapshot of frame 10. The test confirms the generated ghost is statically positioned at `tx=10.0`, proving exact evaluated world-space evaluation and independence.

## Object Bypass Behavior
`ObjectBypassStore` uses a set of ignored object IDs. `filter_targets` successfully returns only the target objects that have not been marked as bypassed.

## Proxy Source Behavior
`ProxySourceResolver` successfully returns the `proxy_root` if `source_mode="proxy"` and the proxy exists. It safely falls back to the original root if the proxy is missing.

## Scene Profile Store Behavior
`SceneProfileStore` creates a `network` node named `POSE_GHOST_PROFILE` and stores a JSON string in the `poseGhostProfileJson` attribute. The integration test proved it can save and load standard dictionary data.

## Boundary Check Results
Confirmed that `core` remains completely Maya/Qt free, `runtime` remains Maya/Qt free, and `ui` does not import adapter/runtime logic.

## Scaffold/Spec Mismatches Found
None.

## Stage 06 Safe to Start
Yes, Stage 06 is safe to start.
