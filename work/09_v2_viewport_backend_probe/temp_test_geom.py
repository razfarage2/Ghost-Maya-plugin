import maya.api.OpenMayaRender as omr
import maya.api.OpenMaya as om
import maya.standalone
maya.standalone.initialize()
class Test(omr.MPxSubSceneOverride):
    def __init__(self):
        # MPxSubSceneOverride __init__ requires an MObject
        super(Test, self).__init__(om.MObject())
    def update(self, container, ctx):
        pass

def run():
    ri = omr.MRenderItem.create('test', omr.MRenderItem.MaterialSceneItem, omr.MGeometry.kTriangles)
    vb = omr.MVertexBuffer(omr.MVertexBufferDescriptor('', omr.MGeometry.kPosition, omr.MGeometry.kFloat, 3))
    vba = omr.MVertexBufferArray()
    vba.append(vb, 'positions')
    ib = omr.MIndexBuffer(omr.MGeometry.kUnsignedInt32)
    
    t = Test()
    try:
        t.setGeometryForRenderItem(ri, vba, ib, None)
        print("Success with None")
    except Exception as e:
        print("Error with None:", e)
        
    try:
        t.setGeometryForRenderItem(ri, vba, ib, om.MBoundingBox())
        print("Success with bbox")
    except Exception as e:
        print("Error with bbox:", e)

run()
