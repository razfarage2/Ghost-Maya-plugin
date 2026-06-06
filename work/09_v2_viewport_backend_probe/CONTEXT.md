# work/09_v2_viewport_backend_probe/ CONTEXT.md

## Goal

V2 feasibility spike: draw onion-skin ghosts directly in Maya's VP2 pipeline
using MPxSubSceneOverride or MPxDrawOverride, bypassing DAG node duplication.

## Key API Candidates

```text
maya.api.OpenMayaRender.MPxSubSceneOverride
maya.api.OpenMayaRender.MRenderItem
maya.api.OpenMayaRender.MVertexBuffer
maya.api.OpenMayaRender.MGeometry
maya.api.OpenMayaRender.MPxDrawOverride
maya.api.OpenMayaRender.MUIDrawManager
```

## Current State

- V1 renderer uses cmds.duplicate to create DAG ghost nodes.
- V1 is functional for simple/medium rigs but slow for heavy rigs.
- Superhive (Blender reference) draws ghosts via GPU shader batches — no scene objects.
- Maya equivalent is VP2 MRenderItem / MVertexBuffer approach.

## Probe Strategy

1. Check API class availability in mayapy.
2. Create a minimal custom locator node with MPxSubSceneOverride.
3. Feed captured mesh vertex data as MVertexBuffer.
4. Draw transparent colored geometry per sample.
5. Prove no DAG ghost duplication needed.
6. Document what requires interactive Maya vs mayapy.
