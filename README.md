# Pose Ghost — Maya 3D Onion Skinning

Pose Ghost is a planned Autodesk Maya plugin that displays translucent 3D onion-skin samples before and after the current timeline frame.

The current repository is an ICM-style scaffold and specification package. Production code is not implemented yet.

## Locked V1 Direction

- Python for Maya.
- Event-driven runtime, no polling.
- Relative frame onion-skin sampling as the primary behavior.
- Multiple previous and next samples.
- Blue previous ghosts and red next ghosts by default.
- Opacity falloff for farther samples.
- Exact world-space evaluated pose positions.
- Non-renderable viewport ghost geometry.
- Compact UI with target setup, counts, step, display mode, colors, opacity, falloff, bypass, and clear/rebuild actions.

## Start Here

1. Read `AGENTS.md`.
2. Read `CONTEXT.md`.
3. Read `BUILD_ORDER.md`.
4. Start with `work/01_project_scaffold/CONTEXT.md`.

## Primary Specs

```text
docs/spec/pose_ghost_design_spec.md
docs/spec/pose_ghost_runtime_spec.md
docs/spec/pose_ghost_ui_spec.md
docs/spec/pose_ghost_maya_api_spec.md
docs/spec/pose_ghost_data_model_spec.md
docs/spec/pose_ghost_acceptance_tests.md
```