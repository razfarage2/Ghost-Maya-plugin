# Pose Ghost Uninstallation Guide

## 1. Unloading the Tool
If you want to unload the tool safely without restarting Maya, run the following Python command in the Script Editor to cleanly remove all internal callbacks and close the UI:
```python
import pose_ghost.launcher as pg
pg.unload()
```

If you also wish to delete all Pose Ghost mesh nodes from the current scene during unload:
```python
import pose_ghost.launcher as pg
pg.unload(clear_ghosts=True)
```

## 2. Removing Module Files
1. Navigate to your Maya modules directory (e.g., `C:\Users\<username>\Documents\maya\modules`).
2. Delete the `PoseGhost.mod` file or the symlink.
3. You can now safely delete the repository folder from your hard drive.

## 3. Removing Shelf Buttons
1. Right-click the Pose Ghost shelf button in Maya.
2. Select **Delete**.

## 4. Cleaning Scene Nodes
If you saved a scene while Pose Ghost was active, you may have ghost groups left behind.
- Pose Ghost **does not** modify your source rig, source meshes, materials, or animation keys. You can safely delete these groups manually in the Outliner:
  - `PoseGhostGrp` (and all children: `PoseGhostPreviousGrp`, `PoseGhostNextGrp`)
  - Maya Display Layers starting with `PoseGhost...`
  - Materials starting with `PoseGhost...`

You can also run this script to clean them automatically before unloading:
```python
from pose_ghost.maya_adapters.mesh_snapshot_renderer import MeshSnapshotRenderer
MeshSnapshotRenderer.cleanup()
```
