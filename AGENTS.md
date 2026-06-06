# AGENTS.md — Pose Ghost Root Router

> You are working on **Pose Ghost** — a Maya 3D onion-skinning plugin.
> The approved design spec is the source of truth for architecture, runtime behavior, UI, and acceptance tests.

## Approved Specification

Read these before changing code:

```text
docs/spec/pose_ghost_design_spec.md
docs/spec/pose_ghost_runtime_spec.md
docs/spec/pose_ghost_ui_spec.md
docs/spec/pose_ghost_maya_api_spec.md
docs/spec/pose_ghost_data_model_spec.md
docs/spec/pose_ghost_acceptance_tests.md
```

Read these policies before continuing:

```text
docs/policies/clean_architecture.md
docs/policies/clean_code.md
```

Read these references when relevant:

```text
docs/references/icm.pdf
docs/references/superhive_3d_onion_skinning_reference.md
docs/references/maya_api_reference.md
docs/references/root_agents_example_devir.md
```

## Repo Map — Where To Go

| Work needed | Go to |
|---|---|
| Project routing, source of truth, build order | root `AGENTS.md`, `CONTEXT.md`, `REFERENCE.md`, `BUILD_ORDER.md` |
| Product and technical specs | `docs/spec/` |
| Clean-code and architecture policies | `docs/policies/` |
| External/reference behavior | `docs/references/` |
| Python package source | `src/pose_ghost/` |
| Pure logic, no Maya imports | `src/pose_ghost/core/` |
| Maya-specific code and boundary adapters | `src/pose_ghost/maya_adapters/` |
| Runtime orchestration and callback lifecycle | `src/pose_ghost/runtime/` |
| Compact Qt UI | `src/pose_ghost/ui/` |
| Pure Python tests | `tests/core/` |
| Maya integration tests/scripts | `tests/maya_integration/` |
| ICM work stages | `work/` |

Each major folder has local routing/context docs. Before changing a folder, read that folder's:

```text
AGENTS.md
CONTEXT.md
REFERENCE.md
```

## Current Implementation Reality

This repository is a scaffold and specification package. Production code is not implemented yet.

The source of truth is the current spec version: **v0.4**.

The product is no longer a simple previous/next keyed-pose ghost tool. It is now a **Maya 3D onion-skinning tool** modeled behaviorally on the Superhive Blender 3D Onion Skinning add-on reference.

## Non-Negotiable Rules

1. **The spec is the source of truth.** If code and spec disagree, flag the deviation in the report. Do not silently resolve it in code's favor.
2. **Read local docs before changing code.** Use the relevant `AGENTS.md`, `CONTEXT.md`, and `REFERENCE.md` for the folder.
3. **No polling timeline loop.** Runtime must use Maya event/callback mechanisms and a debounced update queue.
4. **No source rig mutation.** Do not modify rig controls, animation curves, constraints, skinClusters, or original materials.
5. **Viewport-only ghosts.** Ghosts are visible in Maya viewport/playblast context but must be hidden from final render.
6. **Exact evaluated pose position.** Ghosts preserve the evaluated world-space position of the sampled frame. No visual offset unless a future spec explicitly approves it.
7. **Core must remain Maya-free.** `src/pose_ghost/core/` must not import `maya.cmds`, `maya.api.OpenMaya`, Qt, or other Maya framework APIs.
8. **Maya API details stay at the boundary.** Put Maya calls in `maya_adapters/` or runtime boundary glue.
9. **UI stays thin.** UI must not contain sample-planning, animation-callback, or mesh-capture logic.
10. **If unsure, stop and flag it.** Do not invent behavior.

## Locked Current Contracts

### Product behavior

- Multiple previous and next onion-skin samples.
- Primary sampling mode: relative frames around the current timeline frame.
- Optional future/advanced sampling mode: keyed poses.
- Previous samples are blue by default.
- Next samples are red by default.
- Farther samples can fade to lower opacity.
- Counts, step, opacity, fade, colors, display mode, and target bypass are configurable.
- Playback should not trigger rebuild storms.
- Key/graph edits should mark onion skins dirty and update automatically.

### Runtime behavior

- Time changes use an event-driven Maya API callback backend.
- Animation edits use Maya animation-message callbacks where feasible.
- Heavy rebuilds are debounced.
- Internal time changes during snapshot capture are guarded to prevent recursion.
- Callback IDs are tracked and cleaned up.

### Build discipline

Every Codex task must be narrow. Do not bundle unrelated stages unless the prompt explicitly approves that scope.

Every Codex task must write a report including:

- what changed
- the logic according to Codex
- what bugs could happen
- how to test
- how this relates to the spec / approved decision
- what could be a v2 improvement
- exact tests run
- pass/fail counts

Passing tests are not final proof. Maya live validation by Raz is the validation layer.