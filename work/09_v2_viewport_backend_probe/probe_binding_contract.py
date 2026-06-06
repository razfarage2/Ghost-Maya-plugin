import sys
import traceback
import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr
import maya.cmds as cmds

def run_binding_diagnosis():
    print("\n=== VP2 BINDING CONTRACT DIAGNOSIS ===\n")
    
    results = []

    # Try different Render Item Types
    item_types = [
        ("MaterialSceneItem", omr.MRenderItem.MaterialSceneItem),
        ("NonMaterialSceneItem", omr.MRenderItem.NonMaterialSceneItem),
        ("DecorationItem", omr.MRenderItem.DecorationItem)
    ]
    
    geom_types = [
        ("Triangles", omr.MGeometry.kTriangles),
        ("Lines", omr.MGeometry.kLines),
        ("Points", omr.MGeometry.kPoints)
    ]
    
    # We will create an MPxSubSceneOverride instance to call setGeometryForRenderItem
    class DummyOverride(omr.MPxSubSceneOverride):
        def __init__(self, obj):
            super(DummyOverride, self).__init__(obj)
        def supportedDrawAPIs(self):
            return omr.MRenderer.kAllDevices
        def update(self, container, frameContext):
            pass

    # Create dummy node to attach to
    if not cmds.pluginInfo("probe_viewport_backend", query=True, loaded=True):
        print("[FAIL] probe_viewport_backend plugin must be loaded first.")
        return
        
    try:
        node_name = cmds.createNode("PoseGhostProbeLocator")
        sel = om.MSelectionList()
        sel.add(node_name)
        mobj = sel.getDependNode(0)
    except Exception as e:
        print(f"[FAIL] Could not create dummy locator: {e}")
        return

    override = DummyOverride(mobj)
    
    print("Testing setGeometryForRenderItem combinations...")
    
    for item_name, item_type in item_types:
        for geom_name, geom_type in geom_types:
            name = f"test_{item_name}_{geom_name}"
            try:
                ri = omr.MRenderItem.create(name, item_type, geom_type)
                
                # Mock acquisition if in batch mode to prevent hard crash
                is_batch = cmds.about(batch=True)
                
                # Create position buffer
                pos_desc = omr.MVertexBufferDescriptor("", omr.MGeometry.kPosition, omr.MGeometry.kFloat, 3)
                pos_buf = omr.MVertexBuffer(pos_desc)
                if not is_batch:
                    pos_data = pos_buf.acquire(3, True)
                    if pos_data:
                        pos_buf.commit(pos_data)
                
                vba = omr.MVertexBufferArray()
                vba.append(pos_buf, "positions")
                
                # Create index buffer
                ib = omr.MIndexBuffer(omr.MGeometry.kUnsignedInt32)
                if not is_batch:
                    ib_data = ib.acquire(3, True)
                    if ib_data:
                        ib.commit(ib_data)
                    
                bbox = om.MBoundingBox(om.MPoint(0,0,0), om.MPoint(1,1,1))
                
                override.setGeometryForRenderItem(ri, vba, ib, bbox)
                status = "PASS"
                err_msg = ""
            except Exception as e:
                status = "FAIL"
                err_msg = str(e)
            
            results.append({
                "Backend": "MPxSubSceneOverride",
                "Item Type": item_name,
                "Primitive": geom_name,
                "Shader": "none",
                "Binding": status,
                "Error": err_msg
            })
            print(f"[{status}] {item_name} | {geom_name} | {err_msg}")

    print("\n--- Diagnostic Matrix ---")
    print("Backend | Item Type | Primitive | Shader | Geometry Binding | Error")
    for r in results:
        print(f"{r['Backend']} | {r['Item Type']} | {r['Primitive']} | {r['Shader']} | {r['Binding']} | {r['Error']}")

    cmds.delete(node_name)
    return results

if __name__ == "__main__":
    run_binding_diagnosis()
