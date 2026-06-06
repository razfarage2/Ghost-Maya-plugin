# Pose Ghost — Maya 3D Onion Skinning Design Spec v0.4

## 1. Status

Approved logic direction: **3D onion skinning for Maya**, behaviorally aligned with the Superhive Blender 3D Onion Skinning add-on reference.

Implementation prompt: not written yet.

Build method: ICM-style staged workspace using root and local `AGENTS.md`, `CONTEXT.md`, and `REFERENCE.md` files.

## 2. Product definition

Pose Ghost is a Maya animation tool that displays multiple translucent 3D onion-skin samples around the current timeline frame.

The animator should see:

```text
Current frame:
  normal original rig/mesh

Previous sampled frames:
  blue translucent viewport ghosts

Next sampled frames:
  red translucent viewport ghosts
```

The tool exists to improve visual understanding of timing, spacing, arcs, pose progression, silhouettes, and motion flow directly inside the Maya scene while animating.

## 3. Primary behavior reference

The approved behavior reference is:

```text
https://superhivemarket.com/products/3d-onion-skinning
```

Pose Ghost should match the reference behaviorally, but it must be rebuilt for Maya. Do not copy Blender add-on code, assets, or implementation.

## 4. Source of truth

The source of truth for V1 behavior is:

```text
current Maya frame
selected target objects or target group
relative frame sampling settings
previous sample count
next sample count
frame step
playback range clamp setting
display mode
opacity/fade/color settings
object bypass list
scene profile state
```

The old keyed-pose-only model is no longer the primary source of truth.

## 5. Sampling modes

### 5.1 Primary V1 mode — Relative Frames

Relative frame sampling generates onion skins by stepping before and after the current timeline frame.

Example:

```text
Current frame: 30
Previous Count: 3
Next Count: 3
Step: 1

Previous samples:
  29, 28, 27

Next samples:
  31, 32, 33
```

Animation on twos:

```text
Current frame: 30
Previous Count: 3
Next Count: 3
Step: 2

Previous samples:
  28, 26, 24

Next samples:
  32, 34, 36
```

### 5.2 Optional / advanced mode — Keyed Poses

The original keyed-pose idea becomes an optional advanced sampler:

```text
Current frame: 27
Keyed frames: 12, 20, 25, 30, 35
Previous keyed samples: 25, 20
Next keyed samples: 30, 35
```

V1 architecture should include a seam for `KeyedPoseSampler`, but the default user experience is relative frame onion skinning.

## 6. Exact world-space rule

This is locked.

Each ghost must be generated from the object's evaluated pose at the sampled frame and must remain at that sampled frame's actual world-space position.

Forbidden unless a later spec explicitly approves it:

```text
offsetting ghosts for readability
moving ghosts beside the character
making ghosts follow the current pose
normalizing samples to the current root position
```

If a character walked forward between frames, the onion skins should show that actual progression through space.

## 7. Visual rules

Defaults:

```text
Previous samples: blue
Next samples: red
Base opacity: 0.30
Opacity falloff: enabled
Fade strength: 0.65
```

Opacity falloff should make nearest samples strongest and farther samples weaker.

Example:

```text
base opacity = 0.30
fade strength = 0.65

index 1: 0.30
index 2: 0.195
index 3: 0.12675
```

## 8. Target object support

V1 must support group scanning so the user does not manually select many parts.

Input:

```text
Target Root / Group
Optional Rig / Control Root for animation edit tracking
Optional Proxy Source Root
```

V1 supported target types:

```text
polygon meshes
skinned/deformed polygon meshes
referenced polygon meshes, as long as the current scene can snapshot them safely
```

V2 placeholder target types:

```text
NURBS curves
NURBS surfaces
Maya text curves
instances
component masks / vertex sets
```

## 9. Object bypass

The tool must support bypassing specific target objects while keeping them in the profile.

Behavior:

```text
Object is in target list.
User clicks bypass/eye icon.
Object is skipped during onion generation.
Object can be re-enabled without rescanning the group.
```

## 10. Proxy / decimated sources

To support performance, the architecture must include a proxy source path.

V1 source modes:

```text
Original Mesh
Proxy Mesh Group
```

V2 placeholder:

```text
Decimated Source Provider
```

Purpose:

```text
Allow heavy characters to generate onion skins from lower-resolution proxy geometry while preserving the original rig and render mesh.
```

## 11. Non-renderable viewport ghosts

Ghosts should be visible in the Maya viewport while working.

Ghosts must be hidden from final render through render visibility flags and/or display layer/material settings.

```text
Allowed:
  visible in viewport
  visible in playblast if the viewport displays them
  owned by Pose Ghost
  safe to delete and rebuild

Forbidden:
  visible in final render
  modifying original mesh materials
  connecting ghost geometry back to rig deformation history
```

## 12. Scene persistence

The user configures the profile once. It should reopen with the Maya scene.

Preferred storage:

```text
hidden network node:
  PoseGhostProfile_<profile_name>

string attr:
  poseGhostProfileJson
```

The profile must store:

```text
profile id/name/schema version
target root
target objects
bypassed objects
optional rig/control root
optional proxy source root
sampling settings
appearance settings
display mode
enabled state
```

## 13. Technology stack

V1:

```text
Language: Python 3 inside Maya
Maya API: maya.cmds, maya.api.OpenMaya, maya.api.OpenMayaAnim
UI: Qt/PySide compatibility layer
Testing: pytest for core, Maya integration scripts for adapters/runtime
Packaging: Maya module + shelf/menu launcher
```

V2 optional:

```text
C++ Maya plugin for Viewport 2.0 direct drawing backend
```

C++ is not needed for V1.

## 14. Architecture

```text
src/pose_ghost/core/
  Pure domain/policy logic. No Maya imports.

src/pose_ghost/maya_adapters/
  Maya API boundary code.

src/pose_ghost/runtime/
  Event orchestration, callback lifecycle, update queue, composition.

src/pose_ghost/ui/
  Compact control surface only.
```

Dependency rule:

```text
core must not import runtime, ui, maya_adapters, maya.cmds, OpenMaya, or Qt.
```

## 15. V1 acceptance summary

V1 is accepted only when it can:

```text
scan target groups
show multiple previous/next relative-frame ghosts
support step values including 1 and 2
use blue/red transparent materials
fade farther samples
preserve exact evaluated world-space positions
auto-update on frame change
auto-update after key/graph edits
avoid rebuild storms during playback
allow object bypass
store/reload scene profile
keep ghosts non-renderable
avoid modifying source rig, mesh materials, animation curves, or skin data
```