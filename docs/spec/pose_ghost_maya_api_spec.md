# Pose Ghost Maya API Spec v0.4

## 1. Purpose

This spec defines the Maya-specific implementation boundary. Maya APIs must stay out of the pure core.

## 2. V1 language and API stack

```text
Python 3 inside Maya
maya.cmds
maya.api.OpenMaya
maya.api.OpenMayaAnim
Qt/PySide compatibility adapter
```

## 3. Time-change backend

Primary candidate:

```python
maya.api.OpenMaya.MDGMessage.addDelayedTimeChangeCallback
```

Responsibilities:

```text
receive current time changes
forward event to runtime/event_router.py
do not perform heavy rebuild inside callback directly
```

## 4. Animation edit backend

Primary candidates:

```python
maya.api.OpenMayaAnim.MAnimMessage.addAnimCurveEditedCallback
maya.api.OpenMayaAnim.MAnimMessage.addAnimKeyframeEditedCallback
```

Responsibilities:

```text
watch animation/key/graph edits
mark onion state dirty
trigger debounced rebuild if safe
```

Probe requirement:

```text
Confirm whether tangent/graph handle edits trigger the selected callbacks in the target Maya version.
If not, document fallback.
```

## 5. Playback state backend

Candidate:

```python
cmds.play(q=True, state=True)
```

Responsibilities:

```text
return whether Maya playback is active
enable runtime to skip rebuilds during playback
```

## 6. Scene profile store

Recommended storage:

```text
network node: PoseGhostProfile_<profile_name>
string attribute: poseGhostProfileJson
```

Responsibilities:

```text
create profile node in current scene
save/load JSON profile
validate stored node paths
support schema_version migration later
never write into referenced rig files
```

## 7. Target scanner

Input:

```text
target root DAG path
```

V1 include:

```text
visible polygon mesh shapes
non-intermediate shapes
referenced meshes if readable/snapshot-able
```

V1 exclude:

```text
intermediate shapes
hidden objects if option says hidden objects are excluded
Pose Ghost generated nodes
construction/helper meshes if clearly marked/excluded
```

## 8. Mesh target adapter

Responsibilities:

```text
resolve object identity
read evaluated mesh world-space data
return snapshot-ready geometry payload
handle missing/deleted nodes gracefully
```

## 9. Evaluated snapshot capture

Capture must produce standalone ghost geometry.

Flow:

```text
store original time
activate internal time-change guard
for each sample frame:
  set current time to sample frame
  force/evaluate scene as needed
  capture each active target mesh in world space
restore original time
clear internal guard
```

Implementation detail must be proven during API probe.

## 10. Mesh snapshot renderer

Responsibilities:

```text
delete/reuse old Pose Ghost-owned ghost nodes
create standalone mesh snapshots
assign side/index material
parent under ghost groups
mark non-renderable
lock or protect transforms
avoid original materials and rig connections
```

Node organization:

```text
POSE_GHOST_GRP
  POSE_GHOST_PREVIOUS_GRP
  POSE_GHOST_NEXT_GRP
```

Display layers:

```text
POSE_GHOST_PREVIOUS_LYR
POSE_GHOST_NEXT_LYR
```

Materials:

```text
POSE_GHOST_PREVIOUS_MAT_<opacity/index>
POSE_GHOST_NEXT_MAT_<opacity/index>
```

## 11. Render visibility flags

Ghosts must be non-renderable.

Potential flags to set where applicable:

```text
primaryVisibility = false
castsShadows = false
receiveShadows = false
visibleInReflections = false
visibleInRefractions = false
motionBlur = false
```

Exact flags differ by node/render context. Probe and document.

## 12. Qt compatibility

UI imports must go through `ui/qt_compat.py`.

Pattern:

```python
try:
    from PySide6 import QtCore, QtWidgets, QtGui
except ImportError:
    from PySide2 import QtCore, QtWidgets, QtGui
```

Target Maya version range must be confirmed before simplifying this.

## 13. V2 Viewport 2.0 backend

V1 does not use C++.

V2 may add:

```text
C++ Viewport 2.0 direct drawing backend
MDrawRegistry
MPxGeometryOverride
MPxSubSceneOverride
```

Purpose:

```text
avoid creating scene ghost nodes
improve heavy-scene performance
draw ghosts directly in viewport
```

Keep this behind `GhostRendererBackend` so V1 Python renderer can be replaced.