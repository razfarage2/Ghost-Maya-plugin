# Maya API Reference Notes

These are implementation references for the Maya adapter/runtime layers. Confirm exact API behavior in Maya during `work/02_maya_api_probe/` before relying on it.

## Time-change callback

Candidate V1 backend:

```python
maya.api.OpenMaya.MDGMessage.addDelayedTimeChangeCallback
```

Purpose:

- Receive time changes from the dependency graph.
- Use with a debounced update queue.
- Do not use polling as the normal runtime strategy.

## Animation edit callbacks

Candidate V1 backends:

```python
maya.api.OpenMayaAnim.MAnimMessage.addAnimCurveEditedCallback
maya.api.OpenMayaAnim.MAnimMessage.addAnimKeyframeEditedCallback
```

Purpose:

- Mark onion skins dirty when keys or graph/tangent data are edited.
- Rebuild after debounce or next safe idle/update window.

## Playback state

Candidate command:

```python
cmds.play(q=True, state=True)
```

Purpose:

- Avoid rebuilding on every playback frame.
- Rebuild once playback stops or when user settles on a new frame.

## Mesh snapshot capture

Potential APIs/commands:

```python
cmds.currentTime(...)
cmds.refresh(suspend=True/False)
maya.api.OpenMaya.MFnMesh
cmds.polyEvaluate
cmds.setAttr(..., '.primaryVisibility', False)
```

Exact implementation must be proven during API probe.

## UI

Use a Qt compatibility adapter:

```python
try:
    from PySide6 import QtCore, QtWidgets, QtGui
except ImportError:
    from PySide2 import QtCore, QtWidgets, QtGui
```

Do not hardcode a single Maya/PySide version until the target Maya version range is confirmed.

## V2 Viewport 2.0 backend

V2 may research a C++ Viewport 2.0 draw backend:

- `MDrawRegistry`
- `MPxGeometryOverride`
- `MPxSubSceneOverride`

This is not V1. V1 uses Python mesh snapshots.