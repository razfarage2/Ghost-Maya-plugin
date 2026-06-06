"""
V2 Viewport Backend Probe — API Availability Check
===================================================

Runs in mayapy (headless). Checks which VP2 render classes
are importable in the current Maya Python environment.

Usage:
    mayapy probe_api_availability.py
"""
import sys
import json

def probe_api_availability():
    results = {}
    maya_version = "unknown"

    # --- Maya standalone init ---
    try:
        import maya.standalone
        maya.standalone.initialize(name='python')
    except Exception as e:
        print(json.dumps({"error": f"Failed to init Maya standalone: {e}"}))
        sys.exit(1)

    try:
        import maya.cmds as cmds
        maya_version = cmds.about(version=True)
        results["maya_version"] = maya_version
        results["api_mode"] = cmds.about(apiVersion=True) if hasattr(cmds.about, '__call__') else "unknown"
        try:
            results["api_version"] = str(cmds.about(apiVersion=True))
        except:
            results["api_version"] = "unknown"
    except Exception as e:
        results["maya_version_error"] = str(e)

    # --- VP2 Render API Classes ---
    vp2_classes = [
        ("MPxSubSceneOverride", "maya.api.OpenMayaRender", "MPxSubSceneOverride"),
        ("MPxDrawOverride", "maya.api.OpenMayaRender", "MPxDrawOverride"),
        ("MRenderItem", "maya.api.OpenMayaRender", "MRenderItem"),
        ("MVertexBuffer", "maya.api.OpenMayaRender", "MVertexBuffer"),
        ("MVertexBufferDescriptor", "maya.api.OpenMayaRender", "MVertexBufferDescriptor"),
        ("MIndexBuffer", "maya.api.OpenMayaRender", "MIndexBuffer"),
        ("MGeometry", "maya.api.OpenMayaRender", "MGeometry"),
        ("MShaderManager", "maya.api.OpenMayaRender", "MShaderManager"),
        ("MRenderer", "maya.api.OpenMayaRender", "MRenderer"),
        ("MDrawRegistry", "maya.api.OpenMayaRender", "MDrawRegistry"),
        ("MUIDrawManager", "maya.api.OpenMayaRender", "MUIDrawManager"),
        ("MFrameContext", "maya.api.OpenMayaRender", "MFrameContext"),
    ]

    # --- Core API Classes ---
    core_classes = [
        ("MPxLocatorNode", "maya.api.OpenMaya", "MPxLocatorNode"),
        ("MPxNode", "maya.api.OpenMaya", "MPxNode"),
        ("MFnMesh", "maya.api.OpenMaya", "MFnMesh"),
        ("MFnDagNode", "maya.api.OpenMaya", "MFnDagNode"),
        ("MDagPath", "maya.api.OpenMaya", "MDagPath"),
        ("MSelectionList", "maya.api.OpenMaya", "MSelectionList"),
        ("MFnPlugin", "maya.api.OpenMaya", "MFnPlugin"),
        ("MPoint", "maya.api.OpenMaya", "MPoint"),
        ("MPointArray", "maya.api.OpenMaya", "MPointArray"),
        ("MFloatPointArray", "maya.api.OpenMaya", "MFloatPointArray"),
        ("MIntArray", "maya.api.OpenMaya", "MIntArray"),
        ("MFloatVectorArray", "maya.api.OpenMaya", "MFloatVectorArray"),
    ]

    all_classes = vp2_classes + core_classes
    api_results = {}
    for label, module_path, class_name in all_classes:
        try:
            mod = __import__(module_path, fromlist=[class_name])
            cls = getattr(mod, class_name, None)
            if cls is not None:
                api_results[label] = {
                    "available": True,
                    "module": module_path,
                    "type": str(type(cls).__name__),
                }
            else:
                api_results[label] = {"available": False, "reason": f"Not found in {module_path}"}
        except ImportError as e:
            api_results[label] = {"available": False, "reason": f"ImportError: {e}"}
        except Exception as e:
            api_results[label] = {"available": False, "reason": f"Error: {e}"}

    results["api_classes"] = api_results

    # --- MDrawRegistry classification strings ---
    try:
        import maya.api.OpenMayaRender as omr
        if hasattr(omr.MDrawRegistry, 'registerSubSceneOverrideCreator'):
            results["registerSubSceneOverrideCreator"] = "available"
        else:
            results["registerSubSceneOverrideCreator"] = "not_available"

        if hasattr(omr.MDrawRegistry, 'registerDrawOverrideCreator'):
            results["registerDrawOverrideCreator"] = "available"
        else:
            results["registerDrawOverrideCreator"] = "not_available"
    except Exception as e:
        results["draw_registry_methods"] = f"Error: {e}"

    # --- MShaderManager stock shaders ---
    try:
        import maya.api.OpenMayaRender as omr
        renderer = omr.MRenderer.theRenderer()
        if renderer:
            shader_mgr = renderer.getShaderManager()
            if shader_mgr:
                results["shader_manager"] = "available"
                # Check stock shader constants
                stock_shaders = []
                for attr_name in dir(omr.MShaderManager):
                    if attr_name.startswith('k3d') or attr_name.startswith('k2d'):
                        stock_shaders.append(attr_name)
                results["stock_shader_constants"] = stock_shaders[:20]
            else:
                results["shader_manager"] = "null_in_batch"
        else:
            results["shader_manager"] = "no_renderer_in_batch"
    except Exception as e:
        results["shader_manager"] = f"Error: {e}"

    # --- MVertexBufferDescriptor semantics ---
    try:
        import maya.api.OpenMayaRender as omr
        semantics = []
        for attr_name in dir(omr.MGeometry):
            if attr_name.startswith('kPosition') or attr_name.startswith('kNormal') or \
               attr_name.startswith('kColor') or attr_name.startswith('kTexture') or \
               attr_name.startswith('kTangent'):
                semantics.append(attr_name)
        results["vertex_semantics"] = semantics
    except Exception as e:
        results["vertex_semantics"] = f"Error: {e}"

    # --- MFnMesh data extraction test (cube) ---
    try:
        import maya.cmds as cmds
        import maya.api.OpenMaya as om

        cmds.file(new=True, force=True)
        cube = cmds.polyCube(name="probeTestCube")[0]
        cmds.setKeyframe(cube, t=1, v=0, at='tx')
        cmds.setKeyframe(cube, t=10, v=5, at='tx')
        cmds.currentTime(5, update=True)

        sel = om.MSelectionList()
        sel.add(cube)
        dag_path = sel.getDagPath(0)

        # Extend to shape
        if dag_path.apiType() == om.MFn.kTransform:
            dag_path.extendToShape()

        fn_mesh = om.MFnMesh(dag_path)

        points = fn_mesh.getPoints(om.MSpace.kWorld)
        num_verts = len(points)

        tri_counts, tri_indices = fn_mesh.getTriangles()
        num_triangles = sum(tri_counts)
        num_tri_indices = len(tri_indices)

        normals = fn_mesh.getNormals(om.MSpace.kWorld)
        num_normals = len(normals)

        results["mesh_data_extraction"] = {
            "success": True,
            "num_vertices": num_verts,
            "num_triangles": num_triangles,
            "num_triangle_indices": num_tri_indices,
            "num_normals": num_normals,
            "sample_vertex_0": [round(points[0].x, 4), round(points[0].y, 4), round(points[0].z, 4)],
        }

        cmds.file(new=True, force=True)
    except Exception as e:
        import traceback
        results["mesh_data_extraction"] = {"success": False, "error": traceback.format_exc()}

    # --- Summary ---
    vp2_available = sum(1 for k, v in api_results.items()
                        if k in [c[0] for c in vp2_classes] and v.get("available"))
    vp2_total = len(vp2_classes)
    results["summary"] = {
        "maya_version": maya_version,
        "vp2_classes_available": f"{vp2_available}/{vp2_total}",
        "all_vp2_available": vp2_available == vp2_total,
        "mpx_sub_scene_override_available": api_results.get("MPxSubSceneOverride", {}).get("available", False),
        "mpx_draw_override_available": api_results.get("MPxDrawOverride", {}).get("available", False),
        "mesh_data_extractable": results.get("mesh_data_extraction", {}).get("success", False),
    }

    print("\n=== V2 VIEWPORT BACKEND PROBE — API AVAILABILITY ===\n")
    print(json.dumps(results, indent=2))

    try:
        maya.standalone.uninitialize()
    except:
        pass

if __name__ == "__main__":
    probe_api_availability()
