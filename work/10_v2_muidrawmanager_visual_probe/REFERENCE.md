# REFERENCE.md — MUIDrawManager Visual Probe

## `MPxDrawOverride` API reference

```python
import maya.api.OpenMayaRender as omr

class MyDrawOverride(omr.MPxDrawOverride):
    @staticmethod
    def creator(obj):
        return MyDrawOverride(obj)

    def __init__(self, obj):
        super(MyDrawOverride, self).__init__(obj, None, isAlwaysDirty=False)
        
    def supportedDrawAPIs(self):
        return omr.MRenderer.kAllDevices
        
    def isBounded(self, objPath, cameraPath):
        return True
        
    def boundingBox(self, objPath, cameraPath):
        # return om.MBoundingBox
        pass
        
    def disableInternalBoundingBoxDraw(self):
        return True
        
    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        # prepare UserData
        return data
        
    def hasUIDrawables(self):
        return True
        
    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        # use drawManager.mesh(mode, positions, normals, colors, indices)
        pass
```
