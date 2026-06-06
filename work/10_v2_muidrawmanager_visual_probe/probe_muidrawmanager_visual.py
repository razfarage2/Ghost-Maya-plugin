import sys
import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr
import maya.api.OpenMayaUI as omui
import maya.cmds as cmds
import json

# --- Constants ---
PROBE_PLUGIN_NAME = "PoseGhost-MUIDrawProbe"
PROBE_NODE_TYPE = "PoseGhostMUIDrawProbeLocator"
PROBE_NODE_ID = om.MTypeId(0x87019) # temporary ID
DRAW_CLASSIFICATION = "drawdb/geometry/PoseGhostMUIDrawProbe"
DRAW_REGISTRANT = "PoseGhostMUIDrawProbeNodePlugin"

PREV_COLOR = (0.0, 0.5, 1.0)
NEXT_COLOR = (1.0, 0.2, 0.2)

# Global store initialized if not present
if not hasattr(sys, "_pose_ghost_muidraw_probe_store"):
    sys._pose_ghost_muidraw_probe_store = {}

def get_store():
    return sys._pose_ghost_muidraw_probe_store

class GhostSampleData:
    def __init__(self, index, side, positions, normals, tri_indices, opacity=1.0):
        self.index = index
        self.side = side
        self.positions = positions
        self.normals = normals
        self.tri_indices = tri_indices
        self.opacity = opacity

# --------------------------------------------------------------------------
# Node Definition
# --------------------------------------------------------------------------
class ProbeLocatorNode(omui.MPxLocatorNode):
    @staticmethod
    def creator():
        return ProbeLocatorNode()

    @staticmethod
    def initialize():
        pass

    def __init__(self):
        super(ProbeLocatorNode, self).__init__()


# --------------------------------------------------------------------------
# Viewport 2.0 Draw Override
# --------------------------------------------------------------------------
class ProbeUserData(om.MUserData):
    def __init__(self):
        super(ProbeUserData, self).__init__(False)
        self.samples = []

class ProbeDrawOverride(omr.MPxDrawOverride):
    @staticmethod
    def creator(obj):
        return ProbeDrawOverride(obj)

    def __init__(self, obj):
        # isAlwaysDirty=True ensures prepareForDraw is called
        super(ProbeDrawOverride, self).__init__(obj, ProbeDrawOverride.drawCallback, isAlwaysDirty=True)

    @staticmethod
    def drawCallback(context, data):
        # MPxDrawOverride requires a drawCallback for legacy reasons, but UI drawables don't use it.
        pass

    def supportedDrawAPIs(self):
        return omr.MRenderer.kAllDevices

    def isBounded(self, objPath, cameraPath):
        return True

    def boundingBox(self, objPath, cameraPath):
        bbox = om.MBoundingBox()
        store = get_store()
        samples = store.get("samples", [])
        for sample in samples:
            for p in sample.positions:
                bbox.expand(om.MPoint(p[0], p[1], p[2]))
        
        # If no samples, give a small default box so it isn't culled incorrectly
        if len(samples) == 0:
            bbox.expand(om.MPoint(-1, -1, -1))
            bbox.expand(om.MPoint(1, 1, 1))
        return bbox

    def disableInternalBoundingBoxDraw(self):
        return True

    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        data = oldData
        if not isinstance(data, ProbeUserData):
            data = ProbeUserData()

        store = get_store()
        data.samples = store.get("samples", [])
        
        # Track that prepareForDraw was called
        store["prepare_called"] = True
        return data

    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        if not isinstance(data, ProbeUserData) or not data.samples:
            return

        drawManager.beginDrawable()
        
        drew_count = 0

        for sample in data.samples:
            if not sample.positions or not sample.tri_indices:
                continue

            # Build MPointArray
            pts = om.MPointArray()
            for x, y, z in sample.positions:
                pts.append(om.MPoint(x, y, z))

            # Build MVectorArray
            norms = om.MVectorArray()
            for nx, ny, nz in sample.normals:
                norms.append(om.MVector(nx, ny, nz))

            # Build MUintArray
            indices = om.MUintArray()
            for idx in sample.tri_indices:
                indices.append(idx)

            # Build MColorArray
            colors = om.MColorArray()
            c = PREV_COLOR if sample.side == "previous" else NEXT_COLOR
            col = om.MColor((c[0], c[1], c[2], sample.opacity))
            for _ in range(len(sample.positions)):
                colors.append(col)

            # Draw using MUIDrawManager
            drawManager.mesh(omr.MUIDrawManager.kTriangles, pts, norms, colors, indices)
            drew_count += 1

        drawManager.endDrawable()

        store = get_store()
        store["drew_samples"] = drew_count
        store["override_called"] = True


# --------------------------------------------------------------------------
# Plugin registration
# --------------------------------------------------------------------------
def maya_useNewAPI():
    pass

def initializePlugin(obj):
    plugin = om.MFnPlugin(obj, "PoseGhost-Experimental", "2.0a", "Any")
    
    # Register locator
    try:
        plugin.registerNode(
            PROBE_NODE_TYPE,
            PROBE_NODE_ID,
            ProbeLocatorNode.creator,
            ProbeLocatorNode.initialize,
            om.MPxNode.kLocatorNode,
            DRAW_CLASSIFICATION
        )
    except Exception as e:
        sys.stderr.write(f"Failed to register node: {e}\n")

    # Register draw override
    try:
        omr.MDrawRegistry.registerDrawOverrideCreator(
            DRAW_CLASSIFICATION,
            DRAW_REGISTRANT,
            ProbeDrawOverride.creator
        )
    except Exception as e:
        sys.stderr.write(f"Failed to register draw override: {e}\n")


def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)

    try:
        omr.MDrawRegistry.deregisterDrawOverrideCreator(
            DRAW_CLASSIFICATION,
            DRAW_REGISTRANT
        )
    except Exception as e:
        sys.stderr.write(f"Failed to deregister draw override: {e}\n")

    try:
        plugin.deregisterNode(PROBE_NODE_ID)
    except Exception as e:
        sys.stderr.write(f"Failed to deregister node: {e}\n")


# --------------------------------------------------------------------------
# Execution Helpers
# --------------------------------------------------------------------------
def extract_mesh_data(dag_path):
    fn_mesh = om.MFnMesh(dag_path)
    points = fn_mesh.getPoints(om.MSpace.kWorld)
    normals = fn_mesh.getNormals(om.MSpace.kWorld)
    
    positions_list = [(p.x, p.y, p.z) for p in points]
    normals_list = [(n.x, n.y, n.z) for n in normals]
    
    counts, indices = fn_mesh.getTriangles()
    tri_indices_list = list(indices)
    
    return positions_list, normals_list, tri_indices_list

def capture_sample(node, time, index, side, opacity):
    cmds.currentTime(time)
    
    sel = om.MSelectionList()
    sel.add(node)
    dag_path = sel.getDagPath(0)
    
    positions, normals, tri_indices = extract_mesh_data(dag_path)
    
    print(f"[POSE GHOST V2 MUIDRAW PROBE] captured {side} frame {time}")
    return GhostSampleData(index, side, positions, normals, tri_indices, opacity)

def cleanup_muidrawmanager_probe():
    get_store().clear()
    
    if cmds.objExists("PoseGhostMUIDrawProbeLocator1"):
        cmds.delete("PoseGhostMUIDrawProbeLocator1")
        
    if cmds.objExists("transform1"):
        # Sometimes locator deletes its parent transform if it's the only child
        try: cmds.delete("transform1")
        except: pass

def run_cube_visual_proof(debug=False, test_opacity=1.0):
    store = get_store()
    store.clear()
    
    print("\n=== POSE GHOST V2 MUIDRAW PROBE ===")
    
    # 1. Ensure plugin is loaded (interactive testing assumes this file is loaded as plugin)
    # The plugin check:
    plugin_name = "probe_muidrawmanager_visual"
    if not cmds.pluginInfo(plugin_name, query=True, loaded=True):
        try:
            cmds.loadPlugin(__file__)
            print("[POSE GHOST V2 MUIDRAW PROBE] plugin loaded")
        except Exception as e:
            print(f"[FAIL] Could not load plugin: {e}")
            return {"error": "Plugin not loaded"}
    else:
        print("[POSE GHOST V2 MUIDRAW PROBE] plugin loaded")
        
    cleanup_muidrawmanager_probe()
    
    if cmds.objExists("V2ProbeSourceCube"):
        cmds.delete("V2ProbeSourceCube")
        
    # 2. Create source cube
    cube = cmds.polyCube(name="V2ProbeSourceCube", w=2, h=2, d=2)[0]
    cmds.setKeyframe(cube, attribute="translateX", t=0, v=0)
    cmds.setKeyframe(cube, attribute="translateX", t=10, v=10)
    cmds.setKeyframe(cube, attribute="translateX", t=20, v=20)
    print("[POSE GHOST V2 MUIDRAW PROBE] source cube created")
    
    # 3. Capture 4 samples
    samples = []
    samples.append(capture_sample(cube, 7.0, 0, "previous", test_opacity))
    samples.append(capture_sample(cube, 9.0, 1, "previous", test_opacity))
    samples.append(capture_sample(cube, 11.0, 0, "next", test_opacity))
    samples.append(capture_sample(cube, 13.0, 1, "next", test_opacity))
    
    store["samples"] = samples
    
    # Reset to current frame
    cmds.currentTime(10.0)
    
    # 4. Create probe container
    loc_name = cmds.createNode(PROBE_NODE_TYPE)
    print("[POSE GHOST V2 MUIDRAW PROBE] probe container created")
    print("[POSE GHOST V2 MUIDRAW PROBE] draw override registered") # implicitly registered when plugin loaded
    
    # Make it non-selectable
    transform = cmds.listRelatives(loc_name, parent=True)[0]
    cmds.setAttr(f"{transform}.overrideEnabled", 1)
    cmds.setAttr(f"{transform}.overrideDisplayType", 2) # Reference mode
    cmds.setAttr(f"{transform}.hiddenInOutliner", 1)
    
    # 5. Trigger draw
    if not cmds.about(batch=True):
        cmds.refresh(force=True)
    
    # Print results
    drew = store.get("drew_samples", 0)
    called = store.get("override_called", False)
    
    if called:
        print("[POSE GHOST V2 MUIDRAW PROBE] draw override called")
        print(f"[POSE GHOST V2 MUIDRAW PROBE] drew {drew} samples")
    else:
        print("[POSE GHOST V2 MUIDRAW PROBE] draw override was NOT called")
        
    # Validation checks
    shapes = cmds.ls(type="mesh")
    ghost_transforms = cmds.ls("Ghost_*", type="transform")
    
    return {
        "samples_captured": len(samples),
        "total_meshes": len(shapes),
        "ghost_duplicates": len(ghost_transforms),
        "override_called": called,
        "drew_samples": drew
    }

if __name__ == "__main__":
    # If run in mayapy batch mode directly
    pass
