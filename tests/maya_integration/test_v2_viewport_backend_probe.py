"""
V2 Viewport Backend Probe — Automated Feasibility Test
=======================================================

Tests what can be proven in mayapy (headless):
- API class availability
- Mesh data extraction via MFnMesh (no duplicate needed)
- Plugin load/register feasibility
- No source mesh mutation
- No ghost DAG node creation

Visual viewport tests require interactive Maya — see probe_interactive_steps.md.
"""
import sys
import os
import json
import traceback

def run_tests():
    results = {}
    def log(name, status, details=""):
        results[name] = {"status": status, "details": str(details)}
        print(f"[{status.upper()}] {name}: {details}")

    try:
        import maya.standalone
        maya.standalone.initialize(name='python')
    except Exception as e:
        print(json.dumps({"error": f"Failed to init Maya: {e}"}))
        return

    sys.path.insert(0, os.path.abspath('src'))

    import maya.cmds as cmds
    import maya.api.OpenMaya as om

    # ---- Test 1: VP2 API Class Availability ----
    try:
        import maya.api.OpenMayaRender as omr
        required_classes = [
            'MPxSubSceneOverride', 'MRenderItem', 'MVertexBuffer',
            'MVertexBufferDescriptor', 'MIndexBuffer', 'MGeometry',
            'MShaderManager', 'MDrawRegistry', 'MRenderer',
            'MPxDrawOverride', 'MUIDrawManager'
        ]
        missing = []
        for cls_name in required_classes:
            if not hasattr(omr, cls_name):
                missing.append(cls_name)

        if not missing:
            log("VP2 API Classes Available", "pass", f"All {len(required_classes)} classes found")
        else:
            log("VP2 API Classes Available", "fail", f"Missing: {missing}")
    except Exception as e:
        log("VP2 API Classes Available", "fail", traceback.format_exc())

    # ---- Test 2: MDrawRegistry Methods ----
    try:
        has_sso = hasattr(omr.MDrawRegistry, 'registerSubSceneOverrideCreator')
        has_do = hasattr(omr.MDrawRegistry, 'registerDrawOverrideCreator')
        log("MDrawRegistry Registration Methods", "pass" if (has_sso and has_do) else "fail",
            f"SubSceneOverride={has_sso}, DrawOverride={has_do}")
    except Exception as e:
        log("MDrawRegistry Registration Methods", "fail", traceback.format_exc())

    # ---- Test 3: MFnMesh Data Extraction (No Duplication) ----
    try:
        cmds.file(new=True, force=True)
        cube = cmds.polyCube(name="v2ProbeTestCube")[0]
        cmds.setKeyframe(cube, t=1, v=0, at='tx')
        cmds.setKeyframe(cube, t=10, v=5, at='tx')
        cmds.setKeyframe(cube, t=20, v=10, at='tx')

        # Count meshes before
        meshes_before = len(cmds.ls(type='mesh'))

        # Capture at frame 5
        cmds.currentTime(5, update=True)
        cmds.getAttr(f"{cube}.worldMatrix[0]")

        sel = om.MSelectionList()
        sel.add(cube)
        dag_path = sel.getDagPath(0)
        if dag_path.apiType() == om.MFn.kTransform:
            dag_path.extendToShape()

        fn_mesh = om.MFnMesh(dag_path)
        points = fn_mesh.getPoints(om.MSpace.kWorld)
        tri_counts, tri_indices = fn_mesh.getTriangles()

        # Count meshes after — should be the same (no duplication)
        meshes_after = len(cmds.ls(type='mesh'))

        if meshes_before == meshes_after and len(points) > 0 and len(tri_indices) > 0:
            log("MFnMesh Data Extraction (No Duplicate)", "pass",
                f"verts={len(points)}, tris={sum(tri_counts)}, "
                f"meshes before={meshes_before}, after={meshes_after}")
        else:
            log("MFnMesh Data Extraction (No Duplicate)", "fail",
                f"meshes before={meshes_before}, after={meshes_after}")
    except Exception as e:
        log("MFnMesh Data Extraction (No Duplicate)", "fail", traceback.format_exc())

    # ---- Test 4: World-Space Position Accuracy ----
    try:
        cmds.currentTime(10, update=True)
        cmds.getAttr(f"{cube}.worldMatrix[0]")

        sel = om.MSelectionList()
        sel.add(cube)
        dag_path = sel.getDagPath(0)
        if dag_path.apiType() == om.MFn.kTransform:
            dag_path.extendToShape()
        fn_mesh = om.MFnMesh(dag_path)
        pts_f10 = fn_mesh.getPoints(om.MSpace.kWorld)

        # At frame 10, tx should be 5.0
        # Cube center should be at X=5.0
        avg_x = sum(p.x for p in pts_f10) / len(pts_f10)
        expected_x = 5.0
        close_enough = abs(avg_x - expected_x) < 0.01

        log("World-Space Position Accuracy", "pass" if close_enough else "fail",
            f"avg_x={avg_x:.4f}, expected={expected_x}")
    except Exception as e:
        log("World-Space Position Accuracy", "fail", traceback.format_exc())

    # ---- Test 5: Source Mesh Not Mutated ----
    try:
        keys = cmds.keyframe(cube, query=True, timeChange=True) or []
        mats = cmds.listConnections(f"{cube}Shape", type='shadingEngine') or []

        # Original should have 3 keyframes and the default initialShadingGroup
        keys_ok = len(keys) == 3
        # Check original material is still assigned
        has_default = any('initialShadingGroup' in m for m in mats)

        log("Source Mesh Not Mutated", "pass" if (keys_ok and has_default) else "fail",
            f"keys={len(keys)}, default_material={has_default}")
    except Exception as e:
        log("Source Mesh Not Mutated", "fail", traceback.format_exc())

    # ---- Test 6: Plugin Load/Register (mayapy) ----
    try:
        plugin_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..', 'work', '09_v2_viewport_backend_probe', 'probe_viewport_backend.py'
        )
        plugin_path = os.path.normpath(plugin_path)

        if not os.path.exists(plugin_path):
            # Try alternative path
            plugin_path = os.path.abspath(
                'work/09_v2_viewport_backend_probe/probe_viewport_backend.py'
            )

        if os.path.exists(plugin_path):
            cmds.loadPlugin(plugin_path)
            loaded = cmds.pluginInfo(plugin_path, query=True, loaded=True)

            if loaded:
                # Create the locator node
                locator = cmds.createNode("PoseGhostProbeLocator", name="testProbeLocator")
                locator_exists = cmds.objExists(locator)

                # Count mesh shapes — should NOT have any ghost duplicates
                all_meshes = cmds.ls(type='mesh')
                ghost_meshes = [m for m in all_meshes if 'Ghost_' in m]

                cmds.delete(locator)
                parents = cmds.ls("testProbeLocator*")
                for p in parents:
                    if cmds.objExists(p):
                        cmds.delete(p)

                cmds.unloadPlugin(plugin_path)

                log("Plugin Load/Register/Unload", "pass",
                    f"loaded={loaded}, locator_created={locator_exists}, "
                    f"ghost_duplicates={len(ghost_meshes)}")
            else:
                log("Plugin Load/Register/Unload", "fail", "Plugin did not load")
        else:
            log("Plugin Load/Register/Unload", "skip", f"Plugin file not found at {plugin_path}")
    except Exception as e:
        log("Plugin Load/Register/Unload", "fail", traceback.format_exc())

    # ---- Test 7: Vertex Buffer Descriptor Creation ----
    try:
        import maya.api.OpenMayaRender as omr

        pos_desc = omr.MVertexBufferDescriptor(
            "", omr.MGeometry.kPosition, omr.MGeometry.kFloat, 3
        )
        norm_desc = omr.MVertexBufferDescriptor(
            "", omr.MGeometry.kNormal, omr.MGeometry.kFloat, 3
        )

        pos_buf = omr.MVertexBuffer(pos_desc)
        norm_buf = omr.MVertexBuffer(norm_desc)
        idx_buf = omr.MIndexBuffer(omr.MGeometry.kUnsignedInt32)

        log("Vertex/Index Buffer Creation", "pass",
            f"pos_buf={type(pos_buf).__name__}, norm_buf={type(norm_buf).__name__}, "
            f"idx_buf={type(idx_buf).__name__}")
    except Exception as e:
        log("Vertex/Index Buffer Creation", "fail", traceback.format_exc())

    # ---- Test 8: Boundary Check — Core Has No Maya Imports ----
    try:
        core_dir = os.path.abspath('src/pose_ghost/core')
        violations = []
        for root, dirs, files in os.walk(core_dir):
            for f in files:
                if f.endswith('.py') and f != '__pycache__':
                    fpath = os.path.join(root, f)
                    with open(fpath, 'r') as fh:
                        for i, line in enumerate(fh, 1):
                            stripped = line.strip()
                            if stripped.startswith('#'):
                                continue
                            if 'import maya' in stripped or 'from maya' in stripped:
                                violations.append(f"{f}:{i}: {stripped}")
                            if 'from PySide' in stripped or 'import PySide' in stripped:
                                violations.append(f"{f}:{i}: {stripped}")

        if not violations:
            log("Boundary: Core No Maya/Qt Imports", "pass", "No violations")
        else:
            log("Boundary: Core No Maya/Qt Imports", "fail", str(violations))
    except Exception as e:
        log("Boundary: Core No Maya/Qt Imports", "fail", traceback.format_exc())

    # ---- Test 9: RendererBackend Protocol Importable ----
    try:
        from pose_ghost.maya_adapters.renderer_backend import RendererBackend
        log("RendererBackend Protocol Import", "pass", f"Protocol class: {RendererBackend}")
    except Exception as e:
        log("RendererBackend Protocol Import", "fail", traceback.format_exc())

    # ---- Cleanup ----
    try:
        cmds.file(new=True, force=True)
    except:
        pass

    try:
        maya.standalone.uninitialize()
    except:
        pass

    # ---- Summary ----
    print("\n--- RESULTS JSON ---")
    print(json.dumps(results, indent=2))

    passed = sum(1 for v in results.values() if v["status"] == "pass")
    failed = sum(1 for v in results.values() if v["status"] == "fail")
    skipped = sum(1 for v in results.values() if v["status"] == "skip")
    print(f"\nTotal: {len(results)} | Pass: {passed} | Fail: {failed} | Skip: {skipped}")

if __name__ == "__main__":
    run_tests()
