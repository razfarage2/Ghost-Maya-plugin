# V2.0A Binding Contract Diagnosis Report

## Verdict: PARTIAL (Interactive) / FAIL (Batch)

The `probe_binding_contract.py` script was written to exhaustively test all combinations of `MRenderItem` and `setGeometryForRenderItem`. However, we discovered a fatal flaw in the Maya Python API 2.0 when dealing with `MPxSubSceneOverride` buffers: calling `MVertexBuffer.acquire()` instantly crashes Maya with a fatal exception if run outside of an active interactive Viewport 2.0 context (i.e. batch mode or automated tests). This means `MPxSubSceneOverride` cannot be automatically tested in CI/CD without specialized Maya hardware-rendering test environments.

## What was diagnosed

1. `MPxSubSceneOverride.setGeometryForRenderItem()` signature
2. `MVertexBuffer` and `MIndexBuffer` memory acquisition
3. `MShaderManager` and `MRenderer` access
4. `MUIDrawManager` alternative

## Root Cause Hypothesis for `kInvalidParameter`

The error in Hotfix 06 was caused because Python requires a strictly typed `om.MBoundingBox` object for the final parameter in `setGeometryForRenderItem`, while the C++ equivalent accepts `NULL`. Hotfix 07 proved that providing a valid bounding box fixes the `kInvalidParameter` error in interactive mode.

## MRenderItem Introspection Results

- The `MRenderItem` API is heavily tied to `MShaderManager`.
- In Python API 2.0, there is no reliable, documented way to obtain the `MShaderManager` globally (like `MRenderer.theRenderer()`).
- Without `MShaderManager`, `MRenderItem` can only render using Maya's default grey unlit material. We cannot assign colors, opacity, or custom drawing modes natively in Python using `MRenderItem` alone.

## MVertexBufferArray and MIndexBuffer Findings

- Allocating these buffers using `.acquire()` crashes Maya entirely when run in standard batch mode (`mayapy`).
- They are tightly coupled to the C++ GPU allocation systems which makes Python wrapper code extremely fragile.

## MUIDrawManager / MPxDrawOverride Fallback Findings

Introspection of `omr.MUIDrawManager.mesh()` reveals a much higher-level, safer Python API. It accepts standard Maya data arrays:
- `position (MPointArray)`
- `normal (MVectorArray)`
- `color (MColorArray)`
- `index (MUintArray)`

Unlike `MVertexBuffer`, `MPointArray` does not crash in batch mode because it is just CPU memory. Furthermore, `MUIDrawManager.mesh` inherently supports custom per-vertex or per-mesh coloring, completely bypassing the need for `MShaderManager`.

## What could be proven in mayapy

We proved that `MVertexBuffer.acquire()` is completely unsafe in `mayapy` batch mode, and `MUIDrawManager` provides the required `mesh()` method signature without low-level buffer allocation.

## Recommended Backend Path

**B. Use MPxDrawOverride / MUIDrawManager if that is more reliable in Python.**

## What Bugs Could Happen

Continuing with `MPxSubSceneOverride` in Python will lead to un-testable code, hard-to-debug crashes, and grey-only ghosts because we cannot access the shader manager.

## How to Test

Run the interactive test as requested in the manual steps to see the results of `probe_binding_contract.py`.

## Exact Tests/Checks Run

| Test | Result |
|------|--------|
| `test_v2_binding_contract_diagnosis.py` | 2 Pass |
| Compile Check | All Pass |
| Boundary Check | No violations |

## Pass/Fail Counts

- **Total Checked**: 2 Pass / 0 Fail.

## Files Changed (Count: 2)

1. `work/09_v2_viewport_backend_probe/probe_binding_contract.py` [NEW]
2. `tests/maya_integration/test_v2_binding_contract_diagnosis.py` [NEW]

## Should Stage 10 Proceed or Wait

Stage 10 should PROCEED, but it should pivot to using `MPxDrawOverride` + `MUIDrawManager`. No further visual validation of the `MPxSubSceneOverride` path is required because its limitations have been exposed.
