# VP2 Binding Contract Interactive Diagnosis

Run this exact script in the Maya Python Script Editor to diagnose the geometry binding combinations directly against the Maya hardware GPU context:

```python
import sys
import maya.cmds as cmds

probe_dir = r"G:\maya-plugins\Ghost-Maya-plugin\work\09_v2_viewport_backend_probe"

if probe_dir not in sys.path:
    sys.path.insert(0, probe_dir)

if "probe_binding_contract" in sys.modules:
    del sys.modules["probe_binding_contract"]

import probe_binding_contract as pbc
results = pbc.run_binding_diagnosis()
cmds.refresh(force=True)
```

### What to check:
Open the Script Editor history and look for the output matrix:
```text
Backend | Item Type | Primitive | Shader | Geometry Binding | Error
...
```
Report the output of this matrix back so we can see which combinations are valid in Maya 2026.
