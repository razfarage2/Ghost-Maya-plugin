"""
V2 Viewport Backend Probe — MPxSubSceneOverride Plugin
======================================================

EXPERIMENTAL — This is a feasibility probe, NOT production code.

This plugin registers:
  1. PoseGhostProbeLocator  — A single MPxLocatorNode acting as a container.
  2. PoseGhostProbeSSO      — An MPxSubSceneOverride drawing ghost mesh data
                              directly in VP2 without creating DAG duplicate nodes.

Usage (interactive Maya only):
    import maya.cmds as cmds
    cmds.loadPlugin(r"G:\\maya-plugins\\Ghost-Maya-plugin\\work\\09_v2_viewport_backend_probe\\probe_viewport_backend.py")

    # Then run the interactive proof:
    from work._09_v2_viewport_backend_probe import probe_viewport_backend as pvb
    pvb.run_cube_proof()
"""

import sys
import ctypes
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaRender as omr
import maya.cmds as cmds

# --------------------------------------------------------------------------
# Maya 2.0 API flag
# --------------------------------------------------------------------------
maya_useNewAPI = True

# --------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------
LOCATOR_TYPE_NAME = "PoseGhostProbeLocator"
LOCATOR_TYPE_ID = om.MTypeId(0x00138500)  # Temporary dev ID — replace for production
LOCATOR_DRAW_DB = "drawdb/subscene/PoseGhostProbeLocator"
LOCATOR_DRAW_CLASSIFY = "drawdb/subscene/PoseGhostProbeLocator"

PREV_COLOR = (0.15, 0.35, 0.95, 1.0)   # Blue
NEXT_COLOR = (0.95, 0.20, 0.15, 1.0)   # Red
PLUGIN_NAME = "probe_viewport_backend"

def is_probe_plugin_loaded() -> bool:
    try:
        return cmds.pluginInfo(PLUGIN_NAME, query=True, loaded=True)
    except:
        return False


def _disable_render_item_shadows(item):
    """Safely attempt to disable shadows on the render item without crashing."""
    try:
        if hasattr(item, 'setCastsShadows'):
            item.setCastsShadows(False)
        if hasattr(item, 'setReceivesShadows'):
            item.setReceivesShadows(False)
    except Exception as e:
        print(f"[VP2 PROBE DEBUG] Could not disable shadows: {e}")


# --------------------------------------------------------------------------
# Ghost sample data container (pure Python — no DAG nodes)
# --------------------------------------------------------------------------
class GhostSampleData:
    """Holds captured mesh vertex/index data for one ghost sample."""
    __slots__ = ('frame', 'side', 'index', 'opacity',
                 'positions', 'normals', 'tri_indices', 'num_triangles')

    def __init__(self, frame, side, index, opacity, positions, normals, tri_indices, num_triangles):
        self.frame = frame
        self.side = side           # "previous" or "next"
        self.index = index         # 0-based sample index
        self.opacity = opacity     # 0.0 .. 1.0
        self.positions = positions # list of (x, y, z) tuples
        self.normals = normals     # list of (nx, ny, nz) tuples
        self.tri_indices = tri_indices   # flat list of int
        self.num_triangles = num_triangles


# --------------------------------------------------------------------------
# Global sample storage (attached to a locator node name)
# --------------------------------------------------------------------------
if not hasattr(sys, "_pose_ghost_v2_probe_store"):
    sys._pose_ghost_v2_probe_store = {}

_ghost_data_store = sys._pose_ghost_v2_probe_store


def set_ghost_data(locator_name, samples):
    """Store ghost sample data for a locator. Called by the probe runner."""
    _ghost_data_store[locator_name] = samples
    print(f"[VP2 PROBE DEBUG] set_ghost_data: store_id={id(_ghost_data_store)}, module={__name__}")
    print(f"[VP2 PROBE DEBUG] set_ghost_data: locator={locator_name}, samples={len(samples)}")
    
    # Force a viewport refresh so the SubSceneOverride picks up the new data
    try:
        if cmds.objExists(locator_name):
            # Touch an attribute to dirty the node
            cmds.dgdirty(locator_name)
            cmds.refresh(force=True)
    except:
        pass


def clear_ghost_data(locator_name):
    """Clear ghost sample data for a locator."""
    _ghost_data_store.pop(locator_name, None)
    try:
        if cmds.objExists(locator_name):
            cmds.dgdirty(locator_name)
    except:
        pass


# --------------------------------------------------------------------------
# MPxLocatorNode — Single container node (NO mesh duplication)
# --------------------------------------------------------------------------
class PoseGhostProbeLocator(omui.MPxLocatorNode):
    """
    A single locator node that acts as a draw container for all ghost samples.
    No mesh duplication. No Outliner clutter beyond this one node.
    """

    @staticmethod
    def creator():
        return PoseGhostProbeLocator()

    @staticmethod
    def initialize():
        pass  # No custom attributes needed for the probe

    def compute(self, plug, data):
        return None

    def isBounded(self):
        return True  # Must be True for VP2 to avoid culling if bounds are missing

    def boundingBox(self):
        # Huge bounding box for probe so it's never culled
        return om.MBoundingBox(om.MPoint(-100000, -100000, -100000), om.MPoint(100000, 100000, 100000))


# --------------------------------------------------------------------------
# MPxSubSceneOverride — VP2 direct drawing
# --------------------------------------------------------------------------
class PoseGhostProbeSubSceneOverride(omr.MPxSubSceneOverride):
    """
    Draws ghost mesh data directly in Viewport 2.0 without creating
    any duplicate mesh DAG nodes.

    Each ghost sample becomes one MRenderItem with:
    - MVertexBuffer for positions/normals
    - MIndexBuffer for triangle indices
    - A stock shader with per-sample color and transparency
    """

    def __init__(self, obj):
        super(PoseGhostProbeSubSceneOverride, self).__init__(obj)
        self._render_items = {}  # key -> MRenderItem name
        try:
            self._locator_name = om.MFnDependencyNode(obj).name()
        except:
            self._locator_name = "PoseGhostProbeLocator1"  # Probe fallback
        self._last_data_id = None

    @staticmethod
    def creator(obj):
        print(f"[VP2 PROBE DEBUG] SubSceneOverride creator called for {om.MFnDependencyNode(obj).name()}")
        return PoseGhostProbeSubSceneOverride(obj)

    def supportedDrawAPIs(self):
        return omr.MRenderer.kAllDevices

    def requiresUpdate(self, container, frameContext):
        # Always update — the override checks internally if data changed
        return True

    def update(self, container, frameContext):
        # We stored the node name in __init__ because MDagPath.getAPathTo can fail in some contexts
        if not self._locator_name:
            print("[VP2 PROBE DEBUG] update() called, but _locator_name is empty")
            return

        samples = _ghost_data_store.get(self._locator_name, [])
        # Also fall back to the first available data store if name mismatched (probe only)
        if not samples and _ghost_data_store:
            # For the probe, we just want to prove it works
            samples = list(_ghost_data_store.values())[0]

        print(f"[VP2 PROBE DEBUG] update() called for {self._locator_name}, rendering {len(samples)} samples.")
        print(f"[VP2 PROBE DEBUG] update() store: id={id(_ghost_data_store)}, module={__name__}")

        # Build a set of expected render item names
        expected_names = set()
        for s in samples:
            name = f"ghost_{s.side}_{s.index}"
            expected_names.add(name)

        # Remove stale render items
        stale = [n for n in self._render_items if n not in expected_names]
        for n in stale:
            container.remove(n)
            del self._render_items[n]

        # Create or update render items for each sample
        for s in samples:
            if s.opacity <= 0.001:
                continue

            ri_name = f"ghost_{s.side}_{s.index}"

            # Get or create the render item
            render_item = container.find(ri_name)
            if render_item is None:
                render_item = omr.MRenderItem.create(
                    ri_name,
                    omr.MRenderItem.MaterialSceneItem,
                    omr.MGeometry.kTriangles
                )
                render_item.setDrawMode(omr.MGeometry.kShaded | omr.MGeometry.kTextured)
                _disable_render_item_shadows(render_item)
                render_item.setSelectionMask(om.MSelectionMask())  # Non-selectable
                if hasattr(render_item, "setExcludedFromPostEffects"):
                    try:
                        render_item.setExcludedFromPostEffects(True)
                    except:
                        pass
                container.add(render_item)
                self._render_items[ri_name] = ri_name
                print(f"[VP2 PROBE DEBUG] Created render item: {ri_name}")

            # Enable and set shader
            render_item.enable(True)
            self._set_shader(render_item, s)

            # Set geometry
            self._set_geometry(render_item, s)


    def _set_shader(self, render_item, sample):
        """Assign a stock shader with per-sample color and transparency."""
        try:
            renderer = omr.MRenderer.theRenderer()
        except AttributeError:
            print("[VP2 PROBE DEBUG] MRenderer.theRenderer() not available in this Python API 2.0 version. Falling back to default shader.")
            return

        if renderer is None:
            return
        shader_mgr = renderer.getShaderManager()
        if shader_mgr is None:
            return

        # Use k3dBlinnShader for a decent lit transparent look
        shader = shader_mgr.getStockShader(omr.MShaderManager.k3dBlinnShader)
        if shader is None:
            print("[VP2 PROBE DEBUG] Failed to get k3dBlinnShader")
            return
        else:
            print(f"[VP2 PROBE DEBUG] Successfully acquired k3dBlinnShader for {sample.side}_{sample.index}")

        # Set color based on side
        if sample.side == "previous":
            color = PREV_COLOR
        else:
            color = NEXT_COLOR

        # Apply with per-sample opacity
        diffuse = [color[0], color[1], color[2], sample.opacity]
        shader.setParameter("diffuseColor", diffuse)
        shader.setParameter("transparency", [1.0 - sample.opacity] * 3)
        shader.setIsTransparent(True)

        render_item.setShader(shader)
        print(f"[VP2 PROBE DEBUG] Shader configured. Opacity: {sample.opacity}")

    def _set_geometry(self, render_item, sample):
        """Populate vertex/index buffers from captured mesh data."""
        num_verts = len(sample.positions)
        num_indices = len(sample.tri_indices)

        if num_verts == 0 or num_indices == 0:
            return

        print(f"[VP2 PROBE DEBUG] _set_geometry started for {sample.side}_{sample.index}")
        # --- Vertex buffer: positions ---
        pos_desc = omr.MVertexBufferDescriptor(
            "", omr.MGeometry.kPosition, omr.MGeometry.kFloat, 3
        )
        pos_buffer = omr.MVertexBuffer(pos_desc)
        pos_data = pos_buffer.acquire(num_verts, True)  # writable
        if pos_data is None:
            print("[VP2 PROBE DEBUG] Failed to acquire position buffer")
            return
        
        # Calculate bounding box
        bbox = om.MBoundingBox()

        # Fill position data using ctypes
        float_ptr = ctypes.cast(pos_data, ctypes.POINTER(ctypes.c_float))
        for i, (x, y, z) in enumerate(sample.positions):
            float_ptr[i * 3] = x
            float_ptr[i * 3 + 1] = y
            float_ptr[i * 3 + 2] = z
            bbox.expand(om.MPoint(x, y, z))
        pos_buffer.commit(pos_data)
        print("[VP2 PROBE DEBUG] Committed position buffer")

        # --- Vertex buffer: normals ---
        norm_desc = omr.MVertexBufferDescriptor(
            "", omr.MGeometry.kNormal, omr.MGeometry.kFloat, 3
        )
        norm_buffer = omr.MVertexBuffer(norm_desc)
        norm_data = norm_buffer.acquire(num_verts, True)
        if norm_data is not None:
            float_ptr = ctypes.cast(norm_data, ctypes.POINTER(ctypes.c_float))
            for i, (nx, ny, nz) in enumerate(sample.normals):
                idx = min(i, len(sample.normals) - 1)
                float_ptr[i * 3] = sample.normals[idx][0]
                float_ptr[i * 3 + 1] = sample.normals[idx][1]
                float_ptr[i * 3 + 2] = sample.normals[idx][2]
            norm_buffer.commit(norm_data)
            print("[VP2 PROBE DEBUG] Committed normal buffer")

        # --- Index buffer ---
        idx_buffer = omr.MIndexBuffer(omr.MGeometry.kUnsignedInt32)
        idx_data = idx_buffer.acquire(num_indices, True)
        if idx_data is None:
            return

        uint_ptr = ctypes.cast(idx_data, ctypes.POINTER(ctypes.c_uint))
        for i, idx in enumerate(sample.tri_indices):
            uint_ptr[i] = idx
        idx_buffer.commit(idx_data)
        print("[VP2 PROBE DEBUG] Committed index buffer")

        # --- Assign to render item ---
        vb_list = omr.MVertexBufferArray()
        vb_list.append(pos_buffer, "positions")
        if norm_data is not None:
            vb_list.append(norm_buffer, "normals")

        print("[VP2 PROBE DEBUG] Calling setGeometryForRenderItem...")
        self.setGeometryForRenderItem(render_item, vb_list, idx_buffer, bbox)
        print("[VP2 PROBE DEBUG] setGeometryForRenderItem SUCCESS")


# --------------------------------------------------------------------------
# Plugin registration
# --------------------------------------------------------------------------
def initializePlugin(obj):
    plugin = om.MFnPlugin(obj, "PoseGhost-Experimental", "2.0a", "Any")

    # Register locator node
    try:
        plugin.registerNode(
            LOCATOR_TYPE_NAME,
            LOCATOR_TYPE_ID,
            PoseGhostProbeLocator.creator,
            PoseGhostProbeLocator.initialize,
            om.MPxNode.kLocatorNode,
            LOCATOR_DRAW_CLASSIFY
        )
    except Exception as e:
        om.MGlobal.displayError(f"Failed to register {LOCATOR_TYPE_NAME}: {e}")
        raise

    # Register SubSceneOverride
    try:
        omr.MDrawRegistry.registerSubSceneOverrideCreator(
            LOCATOR_DRAW_DB,
            "PoseGhostProbeSSO",
            PoseGhostProbeSubSceneOverride.creator
        )
    except Exception as e:
        om.MGlobal.displayError(f"Failed to register SubSceneOverride: {e}")
        raise

    om.MGlobal.displayInfo("[Pose Ghost V2 Probe] Plugin loaded successfully.")


def uninitializePlugin(obj):
    plugin = om.MFnPlugin(obj)

    try:
        omr.MDrawRegistry.deregisterSubSceneOverrideCreator(
            LOCATOR_DRAW_DB,
            "PoseGhostProbeSSO"
        )
    except:
        pass

    try:
        plugin.deregisterNode(LOCATOR_TYPE_ID)
    except:
        pass

    # Clear all stored data
    _ghost_data_store.clear()
    om.MGlobal.displayInfo("[Pose Ghost V2 Probe] Plugin unloaded.")


# --------------------------------------------------------------------------
# Mesh data capture utility (no DAG duplication)
# --------------------------------------------------------------------------
def capture_mesh_data(source_node, frame):
    """
    Capture vertex positions, normals, and triangle indices from a mesh
    at a given frame using MFnMesh. NO cmds.duplicate() — data only.

    Returns: (positions, normals, tri_indices, num_triangles) or None
    """
    orig_time = cmds.currentTime(query=True)
    try:
        cmds.currentTime(frame, update=True)

        # Force evaluation
        cmds.getAttr(f"{source_node}.worldMatrix[0]")

        # Get DAG path to shape
        sel = om.MSelectionList()
        sel.add(source_node)
        dag_path = sel.getDagPath(0)
        if dag_path.apiType() == om.MFn.kTransform:
            dag_path.extendToShape()

        fn_mesh = om.MFnMesh(dag_path)

        # World-space positions
        points = fn_mesh.getPoints(om.MSpace.kWorld)
        positions = [(p.x, p.y, p.z) for p in points]

        # World-space normals (per-vertex averaged)
        # MFnMesh.getNormals gives per-face-vertex normals.
        # For the probe, we use getVertexNormals for per-vertex.
        try:
            vert_normals = fn_mesh.getVertexNormals(False, om.MSpace.kWorld)
            normals = [(n.x, n.y, n.z) for n in vert_normals]
        except:
            # Fallback: face-vertex normals averaged manually
            normals = [(0, 1, 0)] * len(positions)

        # Triangle indices
        tri_counts, tri_indices = fn_mesh.getTriangles()
        num_triangles = sum(tri_counts)
        indices = list(tri_indices)

        return positions, normals, indices, num_triangles

    finally:
        cmds.currentTime(orig_time, update=True)


# --------------------------------------------------------------------------
# Interactive cube proof runner
# --------------------------------------------------------------------------
def run_cube_proof(debug=False):
    """
    Interactive Maya proof-of-concept:
    1. Creates an animated cube.
    2. Creates a single PoseGhostProbeLocator.
    3. Captures mesh data at previous/next frames (NO duplication).
    4. Feeds data to the SubSceneOverride for VP2 direct drawing.
    5. Reports results.

    Run this from Maya Script Editor after loading the plugin.
    """
    print(f"\n=== POSE GHOST V2 VIEWPORT BACKEND PROBE (Debug={debug}) ===\n")

    # Ensure plugin is loaded
    if not is_probe_plugin_loaded():
        # Try to load it automatically using __file__
        try:
            cmds.loadPlugin(__file__)
        except Exception as e:
            pass
            
        if not is_probe_plugin_loaded():
            print(f"[ERROR] Plugin '{PLUGIN_NAME}' not loaded. Load it first with:")
            print(f'  cmds.loadPlugin(r"{__file__}")')
            return

    # Clean up any previous probe
    cleanup_cube_proof()

    # 1. Create animated cube
    cube = cmds.polyCube(name="V2ProbeSourceCube")[0]
    cmds.setKeyframe(cube, t=1, v=0, at='tx')
    cmds.setKeyframe(cube, t=5, v=3, at='tx')
    cmds.setKeyframe(cube, t=10, v=7, at='tx')
    cmds.setKeyframe(cube, t=15, v=4, at='tx')
    cmds.setKeyframe(cube, t=20, v=10, at='tx')
    cmds.currentTime(10, update=True)
    print(f"[OK] Created animated cube: {cube}")

    # 2. Create locator (single node — the ONLY node we add)
    locator = cmds.createNode(LOCATOR_TYPE_NAME, name="PoseGhostProbeLocator1")
    # Get the transform parent
    parents = cmds.listRelatives(locator, parent=True)
    locator_transform = parents[0] if parents else locator

    # Hide from outliner, make non-selectable
    cmds.setAttr(f"{locator_transform}.hiddenInOutliner", True)
    cmds.setAttr(f"{locator_transform}.overrideEnabled", True)
    cmds.setAttr(f"{locator_transform}.overrideDisplayType", 2)  # Reference
    print(f"[OK] Created probe locator: {locator} (transform: {locator_transform})")

    # 3. Capture mesh data at sample frames (NO duplication)
    current_frame = cmds.currentTime(query=True)
    sample_frames = [
        {"frame": current_frame - 3, "side": "previous", "index": 0, "opacity": 0.35},
        {"frame": current_frame - 1, "side": "previous", "index": 1, "opacity": 0.25},
        {"frame": current_frame + 1, "side": "next", "index": 0, "opacity": 0.35},
        {"frame": current_frame + 3, "side": "next", "index": 1, "opacity": 0.25},
    ]

    if debug:
        # Visual debug mode: max opacity so ghosts are completely obvious
        for sf in sample_frames:
            sf["opacity"] = 1.0

    samples = []
    for sf in sample_frames:
        data = capture_mesh_data(cube, sf["frame"])
        if data:
            positions, normals, tri_indices, num_tris = data
            sample = GhostSampleData(
                frame=sf["frame"],
                side=sf["side"],
                index=sf["index"],
                opacity=sf["opacity"],
                positions=positions,
                normals=normals,
                tri_indices=tri_indices,
                num_triangles=num_tris,
            )
            samples.append(sample)
            print(f"[OK] Captured {sf['side']} frame {sf['frame']}: "
                  f"{len(positions)} verts, {num_tris} tris (NO DUPLICATE)")

    # 4. Feed data to SubSceneOverride
    set_ghost_data(locator, samples)
    cmds.currentTime(current_frame, update=True)
    cmds.refresh(force=True)
    print(f"[OK] Fed {len(samples)} ghost samples to VP2 SubSceneOverride")

    # 5. Verify results
    print("\n--- VERIFICATION ---")

    # Check: no duplicate mesh nodes created
    all_meshes = cmds.ls(type='mesh')
    ghost_meshes = [m for m in all_meshes if 'Ghost_' in m or 'ghost_' in m.lower()]
    non_probe_meshes = [m for m in all_meshes if m != f"{cube}Shape"]
    print(f"[CHECK] Total mesh shapes in scene: {len(all_meshes)}")
    print(f"[CHECK] Ghost mesh DAG duplicates: {len(ghost_meshes)}")
    print(f"[{'PASS' if len(ghost_meshes) == 0 else 'FAIL'}] No ghost DAG duplicates: "
          f"{'confirmed' if len(ghost_meshes) == 0 else 'FAILED'}")

    # Check: locator exists
    locator_exists = cmds.objExists(locator)
    print(f"[{'PASS' if locator_exists else 'FAIL'}] Locator node exists: {locator_exists}")

    # Check: locator is non-selectable
    override_type = cmds.getAttr(f"{locator_transform}.overrideDisplayType")
    print(f"[{'PASS' if override_type == 2 else 'FAIL'}] Locator non-selectable (reference mode): "
          f"{'confirmed' if override_type == 2 else 'FAILED'}")

    # Check: hidden from outliner
    hidden = cmds.getAttr(f"{locator_transform}.hiddenInOutliner")
    print(f"[{'PASS' if hidden else 'FAIL'}] Hidden from outliner: {'confirmed' if hidden else 'FAILED'}")

    # Check: source cube not mutated
    cube_keys = cmds.keyframe(cube, query=True, timeChange=True) or []
    print(f"[{'PASS' if len(cube_keys) == 5 else 'FAIL'}] Source cube keys preserved: "
          f"{len(cube_keys)} keys (expected 5)")

    print("\n--- VISUAL VERIFICATION (manual) ---")
    print("Look in the viewport. You should see:")
    print("  - 2 blue translucent cubes (previous frames)")
    print("  - 2 red translucent cubes (next frames)")
    print("  - At different X positions along the animation path")
    print("  - The original white cube at frame 10")
    print("  - NO ghost meshes in the Outliner")
    print("  - Ghosts are NOT selectable with the mouse")
    print()
    print("If you see the colored ghosts -> V2 VP2 backend is FEASIBLE!")
    print("If you see nothing extra    -> Check viewport is in VP2 mode (Renderer > Viewport 2.0)")
    print()

    return {
        "ghost_dag_duplicates": len(ghost_meshes),
        "locator_exists": locator_exists,
        "non_selectable": override_type == 2,
        "hidden_outliner": hidden,
        "source_keys_preserved": len(cube_keys) == 5,
        "samples_captured": len(samples),
    }


def cleanup_cube_proof():
    """Clean up the probe scene objects."""
    clear_ghost_data("PoseGhostProbeLocator1")

    for node in ["V2ProbeSourceCube", "PoseGhostProbeLocator1"]:
        if cmds.objExists(node):
            cmds.delete(node)

    # Clean up any transform parents
    for node in cmds.ls("PoseGhostProbeLocator*"):
        if cmds.objExists(node):
            try:
                cmds.delete(node)
            except:
                pass

    # Flush undo queue so the deleted locator node is actually destroyed
    # before the plugin unloads, preventing "services in use" warning.
    cmds.flushUndo()
    print("[OK] Probe cleanup complete.")


def update_opacity(locator_name, opacity_multiplier):
    """
    Prove opacity can be updated without geometry rebuild.
    Just modifies the opacity field in existing sample data and re-dirties.
    """
    samples = _ghost_data_store.get(locator_name, [])
    for s in samples:
        s.opacity = s.opacity * opacity_multiplier

    if cmds.objExists(locator_name):
        cmds.dgdirty(locator_name)
        cmds.refresh(force=True)
    print(f"[OK] Updated opacity by {opacity_multiplier}x for {len(samples)} samples (no geometry rebuild)")
