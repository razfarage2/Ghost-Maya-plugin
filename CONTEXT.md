# CONTEXT.md — Pose Ghost Root Context

## Current Source of Truth

The current approved source of truth is **Pose Ghost spec v0.4** in `docs/spec/`.

Pose Ghost is a Maya 3D onion-skinning plugin. It should behave like the approved Superhive Blender 3D Onion Skinning reference, but it must be implemented cleanly for Maya with Python, Maya event callbacks, evaluated mesh snapshots, and clean architecture boundaries.

## Locked Product Definition

Pose Ghost dynamically displays translucent onion-skin poses around the current Maya timeline frame:

```text
Current frame:
  original rig/mesh shown normally

Previous samples:
  blue transparent ghosts

Next samples:
  red transparent ghosts
```

The ghosts preserve the sampled frame's exact evaluated world-space pose and position.

## Locked Architecture Definition

```text
core/          pure policy and deterministic logic
maya_adapters/ Maya API boundary details
runtime/       event orchestration and lifecycle
ui/            compact control surface
```

Dependency direction:

```text
ui -> runtime -> core
runtime -> maya_adapters through explicit boundary contracts
maya_adapters -> core models allowed
core -> no Maya, no UI, no runtime imports
```

## Current Build State

No production code is implemented yet. The repository is ready for staged Codex work.

Start at `BUILD_ORDER.md`.

## Routing Rules

| Request | Route |
|---|---|
| Change product behavior | `docs/spec/pose_ghost_design_spec.md` first |
| Change runtime/event behavior | `docs/spec/pose_ghost_runtime_spec.md` first |
| Change UI | `docs/spec/pose_ghost_ui_spec.md` first |
| Use Maya API | `docs/spec/pose_ghost_maya_api_spec.md` first |
| Add data classes/models | `docs/spec/pose_ghost_data_model_spec.md` first |
| Add tests | `docs/spec/pose_ghost_acceptance_tests.md` and `tests/CONTEXT.md` first |
| Implement core logic | `src/pose_ghost/core/` local docs first |
| Implement Maya code | `src/pose_ghost/maya_adapters/` local docs first |
| Implement runtime | `src/pose_ghost/runtime/` local docs first |
| Implement UI | `src/pose_ghost/ui/` local docs first |

## Do Not Build Yet Without Stage Context

Do not start from a generic plugin implementation. Work stage-by-stage using the ICM folders in `work/`.