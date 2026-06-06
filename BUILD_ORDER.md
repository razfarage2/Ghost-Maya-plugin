# Pose Ghost Build Order — Maya 3D Onion Skinning v0.4

## Build Rule

Do not skip stages. Each stage must write its report before the next stage starts.

Every Codex task must include a report with:

```text
what changed
the logic according to Codex
what bugs could happen
how to test
how this relates to the spec / approved decision
what could be a v2 improvement
exact tests run
pass/fail counts
```

## Stage 01 — Project Scaffold

Folder:

```text
work/01_project_scaffold/
```

Goal:

```text
Verify/create Python package structure.
Verify every major folder has AGENTS.md, CONTEXT.md, REFERENCE.md.
Create pyproject/module placeholders if needed.
No Maya logic yet.
```

Read:

```text
AGENTS.md
CONTEXT.md
docs/spec/pose_ghost_design_spec.md
docs/policies/clean_code.md
docs/policies/clean_architecture.md
work/01_project_scaffold/CONTEXT.md
```

Output:

```text
work/01_project_scaffold/output/scaffold_report.md
```

Acceptance:

```text
folder structure exists
routing files exist
no production logic added
report written
```

## Stage 02 — Maya API Probe

Folder:

```text
work/02_maya_api_probe/
```

Goal:

```text
Prove Maya APIs before architecture implementation.
```

Must probe:

```text
target group scanning
visible/non-intermediate mesh filtering
Maya delayed time-change callback
MAnim key/curve edit callbacks
whether tangent/graph handle edits trigger callbacks
playback state query
profile network-node JSON storage
evaluated world-space mesh snapshot capture
transparent non-renderable material/layer setup
callback cleanup
```

Output:

```text
work/02_maya_api_probe/output/maya_api_probe_report.md
```

Acceptance:

```text
all candidate APIs confirmed or fallback documented
no full plugin implementation yet
```

## Stage 03 — Core Logic

Folder:

```text
work/03_core_logic/
```

Goal:

```text
Implement pure Python core logic with no Maya imports.
```

Implement:

```text
OnionSettings
OnionSample
SamplePlan
RelativeFrameSampler
OpacityFalloff
DisplayMode
GhostState comparison
TargetObject model
KeyedPoseSampler placeholder/seam
```

Tests:

```text
tests/core/test_relative_frame_sampler.py
tests/core/test_opacity_falloff.py
tests/core/test_display_mode.py
tests/core/test_sample_plan.py
tests/core/test_ghost_state.py
```

Output:

```text
work/03_core_logic/output/core_logic_report.md
```

Acceptance:

```text
core tests pass
core has no Maya/Qt imports
relative frame sampling supports counts, step, clamp, display mode, falloff
```

## Stage 04 — Event Runtime

Folder:

```text
work/04_event_runtime/
```

Goal:

```text
Implement runtime orchestration without renderer details.
```

Implement:

```text
controller
event_router
update_queue
callback_registry
lifecycle
composition_root skeleton
internal time-change guard
playback skip behavior
key-edit dirty state
```

Output:

```text
work/04_event_runtime/output/event_runtime_report.md
```

Acceptance:

```text
runtime can accept time/key/playback events
runtime creates desired SamplePlan
runtime debounces rebuild requests
runtime does not poll
callback IDs can be cleaned up
```

## Stage 05 — Mesh Snapshot Renderer

Folder:

```text
work/05_mesh_snapshot_renderer/
```

Goal:

```text
Implement Maya mesh snapshot renderer for N previous and N next samples.
```

Implement:

```text
target_scanner
mesh_target_adapter
evaluated_snapshot_capture
mesh_snapshot_renderer
material_manager
display_layer_manager
object_bypass_store
proxy_source_resolver
scene_profile_store if not already implemented
```

Must support:

```text
multiple samples
blue/red materials
opacity falloff
exact world-space positions
non-renderable flags
Pose Ghost-owned node cleanup
object bypass
proxy source root path
```

Output:

```text
work/05_mesh_snapshot_renderer/output/renderer_report.md
```

Acceptance:

```text
simple animated mesh creates correct onion ghosts
ghosts do not modify source mesh/material/rig
ghosts clear cleanly
```

## Stage 06 — UI Panel

Folder:

```text
work/06_ui_panel/
```

Goal:

```text
Build compact Maya UI control surface.
```

Implement:

```text
qt_compat
pose_ghost_panel
object_list_model
shortcuts placeholder
```

UI controls:

```text
Target Root / Pick / Scan
Optional Rig Root / Pick / Scan
Sampling Mode
Previous Count
Next Count
Frame Step
Clamp to Playback Range
Show Both / Previous / Next
Previous Color
Next Color
Base Opacity
Opacity Falloff
Fade Strength
Object list + bypass toggles
Ghost Source Mode
Proxy Root
Enable / Disable
Clear Ghosts
Force Rebuild
Save Profile
```

Output:

```text
work/06_ui_panel/output/ui_report.md
```

Acceptance:

```text
UI commands call controller only
UI does not contain core/runtime/renderer logic
invalid values are blocked or corrected
```

## Stage 07 — Integration Validation

Folder:

```text
work/07_integration_validation/
```

Goal:

```text
Validate full behavior inside Maya.
```

Test scenes:

```text
simple animated cube/mesh
skinned/deformed mesh
referenced character mesh
multi-object character group
proxy mesh group
large/heavy target group if available
```

Required validation:

```text
multiple previous/next samples
step 1 and step 2
range clamp
opacity falloff
object bypass
timeline scrub update
playback skip + stop rebuild
key edit dirty update
scene save/reopen
ghost cleanup
non-destructive source validation
```

Output:

```text
work/07_integration_validation/output/integration_validation_report.md
work/07_integration_validation/output/known_bugs.md
work/07_integration_validation/output/v2_recommendations.md
```

Acceptance:

```text
Raz live Maya validation passes or issues are documented with reproduction steps
```

## Stage 08 — Packaging and Installation

Folder:

```text
work/08_packaging_installation/
```

Goal:

```text
Package the tool as a Maya module/shelf/menu installable package.
```

Implement:

```text
Maya module file
shelf/menu launcher
install notes
uninstall notes
version metadata
```

Output:

```text
work/08_packaging_installation/output/packaging_report.md
```

Acceptance:

```text
fresh Maya session can load Pose Ghost
callback cleanup works on unload
scaffold install docs are clear
```