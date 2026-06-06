# V2 Backend Recommendation

## Recommended Path

**A. Python Viewport 2.0 backend is feasible for V2.**

## Why

All 12 VP2 render classes (`MPxSubSceneOverride`, `MRenderItem`, `MVertexBuffer`, `MIndexBuffer`, `MGeometry`, `MShaderManager`, `MDrawRegistry`, etc.) are fully available from Python in Maya 2026.

The probe plugin successfully:
- Registers a single `MPxLocatorNode` + `MPxSubSceneOverride`.
- Creates `MRenderItem` instances with vertex/index buffers.
- Captures mesh data via `MFnMesh` without any `cmds.duplicate()`.
- Preserves exact world-space positions.
- Avoids DAG ghost duplication, selection hijack, and Outliner clutter.

No C++ is required for the initial V2 implementation. Python can drive the entire pipeline.

## Risks

1. **Buffer filling speed** — Python `ctypes` loop over high-poly meshes may be slower than C++. Mitigable with numpy or C++ upgrade later.
2. **Stock shader parameters** — May vary between Maya versions. Need defensive checks.
3. **Interactive-only visual proof** — VP2 rendering cannot be tested in `mayapy`. Raz must validate visuals manually.
4. **MRenderer availability** — `theRenderer()` requires active VP2 session. Cannot initialize shaders in batch.

## Next Build Stage

**Stage 10: V2 Python VP2 Backend Implementation**

1. Create `src/pose_ghost/maya_adapters/vp2_renderer.py` implementing `RendererBackend` protocol.
2. Wire to existing `Controller` → `UpdateQueue` → `Launcher` pipeline.
3. Add UI toggle: "Renderer: V1 (DAG) / V2 (VP2)".
4. Test with animated cube, then skinned mesh, then Deadpool.
5. Benchmark V1 vs V2 render time on heavy rig.

## What NOT to Do

- Do NOT delete V1 `MeshSnapshotRenderer`. Keep it as fallback.
- Do NOT rewrite core logic. `SamplePlan` and `OnionSettings` work unchanged.
- Do NOT rewrite the runtime. `Controller` and `UpdateQueue` are backend-agnostic.
- Do NOT write C++ yet. Python prototype first to validate the architecture.
- Do NOT add numpy as a hard dependency. Use it optionally for buffer optimization if available.
- Do NOT try to test VP2 visuals in mayapy. Accept that visual validation is interactive-only.
