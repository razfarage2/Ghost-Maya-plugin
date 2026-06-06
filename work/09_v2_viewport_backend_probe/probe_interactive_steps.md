# V2 Viewport Backend Probe — Interactive Test Steps

## Prerequisites

- Maya 2026 (or 2024+) in interactive mode.
- Viewport 2.0 renderer active (`Renderer > Viewport 2.0` in the viewport menu bar).

## Step 1: Load the Probe Plugin

Open Maya Script Editor (Python tab) and run:

```python
import maya.cmds as cmds
cmds.loadPlugin(r"G:\maya-plugins\Ghost-Maya-plugin\work\09_v2_viewport_backend_probe\probe_viewport_backend.py")
```

Expected output:
```
[Pose Ghost V2 Probe] Plugin loaded successfully.
```

## Step 2: Run the Cube Proof

```python
import sys
sys.path.insert(0, r"G:\maya-plugins\Ghost-Maya-plugin")
from work._09_v2_viewport_backend_probe import probe_viewport_backend as pvb
pvb.run_cube_proof(debug=True)  # debug=True sets opacity to 1.0 to ensure maximum visibility
```

If the `work` folder does not have `__init__.py` files, use this alternative:

```python
import importlib.util
spec = importlib.util.spec_from_file_location(
    "probe_viewport_backend",
    r"G:\maya-plugins\Ghost-Maya-plugin\work\09_v2_viewport_backend_probe\probe_viewport_backend.py"
)
pvb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pvb)
pvb.run_cube_proof()
```

## Step 3: Visual Verification

Look in the viewport. You should see:

1. **The original white cube** at frame 10 position (X ≈ 7).
2. **Two blue translucent cubes** at previous frame positions (frames 7 and 9).
3. **Two red translucent cubes** at next frame positions (frames 11 and 13).
4. Each ghost is at the **correct world-space X position** for its sampled frame.
5. Ghosts are **translucent** (you can see through them).

## Step 4: Outliner Verification

Open the Outliner (`Windows > Outliner`). You should see:

1. `V2ProbeSourceCube` — the original cube. ✅
2. **No** `Ghost_*` duplicate meshes. ✅
3. The probe locator should be **hidden** from the Outliner. ✅
4. If you toggle "Show Hidden" in Outliner, you may see the locator transform, but it's in Reference mode (non-selectable). ✅

## Step 5: Selection Verification

1. Try clicking on a ghost in the viewport.
2. It should **NOT** be selectable. ✅
3. Clicking should either select nothing or the original cube (if it's behind). ✅

## Step 6: Opacity Update (No Geometry Rebuild)

```python
pvb.update_opacity("PoseGhostProbeLocator1", 0.5)
```

The ghosts should become **more transparent** without any geometry rebuild. The viewport updates instantly.

## Step 7: Camera Movement Verification

1. Orbit the camera around the scene.
2. The ghosts should **remain in world-space position** — they are real 3D geometry, not screen overlays.
3. They should rotate correctly with the camera like normal 3D objects. ✅

## Step 8: Cleanup

```python
pvb.cleanup_cube_proof()
```

Then unload the plugin:
```python
cmds.unloadPlugin("probe_viewport_backend")
```

## Expected Automated Check Results

The `run_cube_proof()` function prints automated checks:

| Check | Expected |
|-------|----------|
| Ghost mesh DAG duplicates | 0 |
| Locator node exists | True |
| Locator non-selectable | True (reference mode) |
| Hidden from outliner | True |
| Source cube keys preserved | 5 keys |
| Samples captured | 4 |

## What If Nothing Appears?

1. **Check viewport renderer**: Must be Viewport 2.0, not Legacy Default Viewport.
2. **Check Maya version**: API requires Maya 2016+ for MPxSubSceneOverride.
3. **Check Script Editor output** for any error messages.
4. **Try refreshing**: `cmds.refresh(force=True)` after running.
