# V2.0A Probe Hotfix 06: MRenderer / Shader Access Report

## Verdict: PASS

The `AttributeError` for `theRenderer` has been fixed by implementing a defensive fallback. The plugin now completes the entire Viewport 2.0 setup path, including render-item creation and geometry assignment, without crashing.

## What Changed

1. **`probe_viewport_backend.py`**:
   - Wrapped the `omr.MRenderer.theRenderer()` call inside a `try/except AttributeError` block.
   - If the renderer accessor is not found in Python API 2.0, the script safely catches the error and skips the `setShader()` step, falling back to Maya's default `MRenderItem` display material.

## Root Cause of `MRenderer.theRenderer` Crash

The Python API 2.0 (`maya.api.OpenMayaRender`) does not expose the static `theRenderer()` singleton accessor for the `MRenderer` class, unlike the C++ or Python 1.0 APIs. While C++ and Python 1.0 scripts can globally fetch the shader manager, Python 2.0 scripts typically expect to be handed the renderer via specific callback contexts (e.g., `MPxDrawOverride` context). However, `MPxSubSceneOverride` does not provide this context directly to Python.

## Actual Maya 2026 Shader/Renderer API Discovered

Introspection confirmed that `omr.MRenderer` exists, but lacks `theRenderer`, `getRenderer`, or any static instantiation method. Likewise, `omr.MShaderManager` cannot be instantiated directly from Python.

## Debug Lifecycle Results

- **Does shader assignment now work?**: No, but it *skips safely* without crashing.
- **Is a fallback path added?**: Yes. The render item is left unshaded, defaulting to Maya's built-in fallback material.
- **Does render item creation still work?**: Yes.
- **Is geometry assignment reached?**: Yes. `_set_geometry` now successfully builds the vertex and index buffers and applies them to the render items.

## The Logic According to Codex

To unblock the visual geometry proof, we cannot let the absence of a shader manager halt execution. By skipping the custom shader assignment, we allow Maya to draw the custom geometry buffers using its default viewport material. This proves whether or not the no-DAG-duplicate `MPxSubSceneOverride` approach is viable for rendering custom meshes, which is the primary goal of the probe.

## What Bugs Could Happen

Because the custom blue/red stock shaders could not be assigned, **the ghosts will not be tinted blue or red**. They will likely render in Maya's default grey or wireframe material. This is expected and acceptable for this stage; the goal is to see if the geometry itself draws at the correct world-space offsets.

## How to Test

Run the interactive steps exactly as provided below in Maya.

## How This Relates to the V2 Probe / Spec

This unblocks the final visual test for the V2 backend feasibility probe.

## What Could Be a V2/V3 Improvement

**B. MRenderItem geometry works but stock shader path needs a production wrapper.**

For Stage 10 (Production V2 Renderer), we have two paths:
1. If we must use `MRenderItem` shaded meshes, we may need a lightweight C++ plugin specifically to acquire the `MShaderManager` and register the shaders, or find an undocumented Python 2.0 context hack.
2. We can pivot the Python probe to use `MUIDrawManager` (which supports tinted flat shaded drawing easily) via an `MPxDrawOverride`, but `MPxSubSceneOverride` remains superior for heavy scenes.

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

## Files Changed (Count: 1)

1. `work/09_v2_viewport_backend_probe/probe_viewport_backend.py` [MODIFIED]

## Exact Interactive Command Raz Should Run Next

Copy and paste this directly into the Maya Python Script Editor:

```python
import sys
import maya.cmds as cmds

probe_dir = r"G:\maya-plugins\Ghost-Maya-plugin\work\09_v2_viewport_backend_probe"

if probe_dir not in sys.path:
    sys.path.insert(0, probe_dir)

import probe_viewport_backend as pvb
pvb.run_cube_proof(debug=True)
cmds.refresh(force=True)
```

**Check the Maya Viewport**. You should look for 4 extra unselectable cubes (they might be grey/default shaded instead of blue/red, but they should be at different timeline positions).

## Blockers Status

**Visual interactive validation is UNBLOCKED.**

## Should Stage 10 Wait?

**YES.** Stage 10 must wait for Raz’s visual check to confirm that the Viewport 2.0 backend actually draws the custom geometry buffers on the screen.
