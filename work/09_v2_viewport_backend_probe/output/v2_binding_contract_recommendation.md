# V2.0A Binding Contract Recommendation

## Recommended Backend Path

**B. Use MPxDrawOverride / MUIDrawManager if that is more reliable in Python.**

## Why?

The diagnosis phase proved that the Python API 2.0 `MPxSubSceneOverride` path has three major roadblocks that make it unsuitable for a pure-Python production plugin:

1. **Untestable in CI/CD:** Calling `MVertexBuffer.acquire()` in batch mode without a GPU context instantly hard-crashes Maya. This makes unit testing the viewport logic impossible.
2. **Missing Shader Access:** `omr.MRenderer.theRenderer()` does not exist in Python 2.0, meaning we cannot acquire an `MShaderManager`. Without it, we cannot assign the required blue/red transparency to `MRenderItem`s.
3. **Fragile Memory Binding:** `setGeometryForRenderItem` is very strict on pointer types (e.g. rejecting Python `None` for bounding boxes), which constantly breaks without robust C++ memory layouts.

## The Alternative

`omr.MUIDrawManager.mesh()` accepts standard `MPointArray`, `MVectorArray`, and `MColorArray`.
- These arrays are CPU-bound and **safe to instantiate and test in batch mode**.
- `MUIDrawManager` handles coloring and transparency natively through the `color` array, completely bypassing the need for an `MShaderManager`.
- It fulfills the core requirement: **No duplicate DAG nodes**. 

## Recommended Next Implementation Scope

Stage 10 should implement a new `MPxDrawOverride` class using `MUIDrawManager`. The next immediate step is to build a `probe_muidrawmanager_fallback.py` to visually verify the blue/red transparent ghosts in Maya using this new, safer architecture.
