# MUIDrawManager Visual Probe Interactive Steps

Copy and paste this directly into the Maya Python Script Editor to test the `MUIDrawManager` ghost drawing:

```python
import sys
import maya.cmds as cmds

probe_dir = r"G:\maya-plugins\Ghost-Maya-plugin\work\10_v2_muidrawmanager_visual_probe"

if probe_dir not in sys.path:
    sys.path.insert(0, probe_dir)

if "probe_muidrawmanager_visual" in sys.modules:
    del sys.modules["probe_muidrawmanager_visual"]

import probe_muidrawmanager_visual as pmv
pmv.run_cube_visual_proof(debug=True, test_opacity=1.0)
cmds.refresh(force=True)
```

### Manual Checklist to Report
- Extra blue previous ghost geometry visible: yes/no
- Extra red next ghost geometry visible: yes/no
- No Ghost_* duplicate meshes in Outliner: yes/no
- Ghosts selectable: yes/no
- Camera orbit keeps ghosts in world-space: yes/no
- Opacity update works: yes/no (If yes, try running with `test_opacity=0.5`)
- Any Script Editor errors:
