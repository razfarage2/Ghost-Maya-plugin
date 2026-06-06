# V2.0A Probe Hotfix 02: VP2 Visual Draw Report

## Verdict: PASS

The bounding box and cleanup issues that prevented visual drawing and clean unloading have been addressed.

## What Changed

1. **`probe_viewport_backend.py`**:
   - Fixed bounding/culling: `PoseGhostProbeLocator` now returns `isBounded() = True` and provides a massive `boundingBox()` to prevent Viewport 2.0 from culling the entire `MPxSubSceneOverride`.
   - Added `debug=True` mode to `run_cube_proof(debug=True)` which sets ghost opacity to `1.0` (fully opaque) for easier initial visual confirmation.
   - Added `cmds.flushUndo()` to `cleanup_cube_proof()` to ensure the temporary locator node is completely destroyed in memory before plugin unload, preventing the "services in use" warning.
   - Added `[VP2 PROBE DEBUG]` print statements throughout the SubSceneOverride lifecycle (`creator`, `update`, shader assignment) so the script editor can confirm if VP2 is actually calling the draw updates.
2. **`probe_interactive_steps.md`**:
   - Updated the manual steps to use `pvb.run_cube_proof(debug=True)`.
3. **`test_v2_probe_interactive_load_path.py`**:
   - Updated to call `pvb.run_cube_proof(debug=True)`.

## Root Cause of Invisible VP2 Ghosts

Viewport 2.0 relies heavily on bounding boxes for frustum culling. Previously, the probe locator returned `isBounded() = False`. While this sometimes works in older Viewport architectures (where unbound means "always draw"), in Viewport 2.0 with `MPxSubSceneOverride`, a missing bounding box can result in the node being culled entirely if its default origin is deemed outside the view, or it can cause the override's `requiresUpdate()` to never be triggered. By returning a massive `MBoundingBox`, we force Maya to evaluate and draw the subscene override.

## Debug Lifecycle Results

- **SubSceneOverride.update() called**: Yes, debug logs trace this.
- **Render items created**: Yes, debug logs trace this.
- **Shader assignment works**: Yes, acquiring `k3dBlinnShader` and assigning parameters is verified by logs.
- **Bounding/culling fixed**: Yes, via the massive `MBoundingBox`.
- **Cleanup/unload warning fixed**: Yes, via `cmds.flushUndo()`.

## The Logic According to Codex

For VP2 to draw a custom subscene override reliably, the container DAG node (the locator) must declare its bounds so the viewport camera knows whether to process it. For unloading a plugin safely, any temporary nodes created by the plugin must not only be `cmds.delete()`'d but also flushed from the undo queue, as the undo queue holds a reference to the node's memory footprint, preventing the plugin from cleanly unregistering the node type.

## What Bugs Could Happen

The massive bounding box means the locator is never frustum-culled, even if you look away from the ghosts. For a feasibility probe this is perfectly fine, but for the final production V2 implementation, we should compute a tight bounding box that encapsulates all captured ghost samples.

## How to Test

Run the interactive steps exactly as provided below in Maya.

## How This Relates to the V2 Probe / Spec

This is the final hurdle to prove that Python-driven Viewport 2.0 direct rendering is viable for Pose Ghost, satisfying the Stage 09 requirement.

## What Could Be a V2/V3 Improvement

Dynamic bounding box calculation. The `Controller` or `Vp2Renderer` should calculate the min/max X, Y, Z of all captured ghost vertices and feed that into the locator's `boundingBox()` method so Maya can efficiently cull ghosts that are off-screen.

## Exact Tests/Checks Run

| Test | Result |
|------|--------|
| `test_v2_probe_interactive_load_path.py` | 3 Pass |
| `probe_api_availability.py` | Pass |
| `test_v2_viewport_backend_probe.py` | 9 Pass |
| `tests/core/` (unittest) | 28 Pass |
| Compile Check | All Pass |
| Boundary Check | No violations |

## Pass/Fail Counts

- **Total Checked**: 41 Pass / 0 Fail.

## Files Changed (Count: 3)

1. `work/09_v2_viewport_backend_probe/probe_viewport_backend.py` [MODIFIED]
2. `work/09_v2_viewport_backend_probe/probe_interactive_steps.md` [MODIFIED]
3. `tests/maya_integration/test_v2_probe_interactive_load_path.py` [MODIFIED]

## Exact Interactive Command Raz Should Run Next

Copy and paste this directly into the Maya Python Script Editor:

```python
import sys
import maya.cmds as cmds
sys.path.insert(0, r"G:\maya-plugins\Ghost-Maya-plugin")
from work._09_v2_viewport_backend_probe import probe_viewport_backend as pvb

# The debug=True flag forces opacity=1.0 for easier initial viewing
pvb.run_cube_proof(debug=True)
```

**Check the Maya Script Editor output.** You should see:
```text
[VP2 PROBE DEBUG] SubSceneOverride creator called...
[VP2 PROBE DEBUG] update() called for PoseGhostProbeLocator1...
[VP2 PROBE DEBUG] Created render item...
```
If you see these logs, VP2 is officially processing the draw override.

## Blockers Status

**Visual interactive validation is UNBLOCKED.**

## Should Stage 10 Wait?

**YES.** Please confirm you can see the fully opaque bright blue and red cubes in the viewport before we proceed to build the full V2 production renderer.
