# work/09_v2_viewport_backend_probe/ AGENTS.md

This folder contains the V2 Viewport Backend Feasibility Spike.

## Purpose

Prove or disprove whether Pose Ghost can draw transparent onion-skin geometry
directly in Maya's Viewport 2.0 pipeline without creating duplicate ghost mesh
DAG nodes.

## Rules

- This is a probe/spike, not production code.
- Do not delete or modify V1 renderer.
- Keep probe scripts self-contained.
- Document what works and what does not honestly.
- If something requires interactive Maya to prove, say so.

## Read before changing

```text
AGENTS.md (root)
docs/spec/pose_ghost_maya_api_spec.md
docs/references/maya_api_reference.md
docs/references/superhive_3d_onion_skinning_reference.md
```
