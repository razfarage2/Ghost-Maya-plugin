# CONTEXT.md — MUIDrawManager Visual Probe

## Why MUIDrawManager?
Previous tests revealed that `MPxSubSceneOverride` in Python API 2.0 has severe flaws for our use case:
1. Cannot access `MShaderManager` easily for tinting.
2. `MVertexBuffer` memory operations cause hard crashes in headless mode.
3. Pointer validation is very strict (`MBoundingBox` missing causes failures).

`MUIDrawManager` circumvents these issues because it works with purely CPU-side `MPointArray`/`MColorArray` objects, handling shading and hardware buffers internally. This allows Maya to gracefully skip rendering in headless mode without crashing, and lets us easily assign color and opacity arrays to geometry.
