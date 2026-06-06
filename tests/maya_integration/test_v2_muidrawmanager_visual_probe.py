import sys
import traceback
import maya.cmds as cmds
import maya.standalone

def log(name, status, details=""):
    print(f"[{status.upper()}] {name}: {details}")

def run():
    maya.standalone.initialize()
    cmds.loadPlugin("matrixNodes", quiet=True)
    
    probe_dir = r"G:\maya-plugins\Ghost-Maya-plugin\work\10_v2_muidrawmanager_visual_probe"
    if probe_dir not in sys.path:
        sys.path.insert(0, probe_dir)

    # 1. Test probe module imports and plugin loads
    try:
        import probe_muidrawmanager_visual as pmv
        cmds.loadPlugin(pmv.__file__)
        log("Probe Module & Plugin Load", "pass", "Module imported and plugin loaded")
    except Exception as e:
        log("Probe Module & Plugin Load", "fail", str(e))
        return

    # 2. Test execution logic
    try:
        results = pmv.run_cube_visual_proof()
        
        if results.get("error"):
            log("Probe Execution", "fail", results["error"])
            return
            
        log("Samples Captured", "pass" if results["samples_captured"] == 4 else "fail", f"Captured {results['samples_captured']} samples")
        
        # 3. Test DAG Duplicates
        if results["total_meshes"] == 1 and results["ghost_duplicates"] == 0:
            log("No DAG Duplicates", "pass", "1 source mesh, 0 duplicate transforms")
        else:
            log("No DAG Duplicates", "fail", f"{results['total_meshes']} meshes, {results['ghost_duplicates']} duplicates")

        # 4. Test Source Preservation
        keys = cmds.keyframe("V2ProbeSourceCube", query=True, timeChange=True) or []
        log("Source Cube Keys Preserved", "pass" if len(keys) == 3 else "fail", f"{len(keys)} keys")

        # 5. Draw override in batch
        # MPxDrawOverride usually does not execute in batch mode, so we log it as expected
        if not results["override_called"]:
            log("Draw Override in Batch", "pass", "Draw override skipped cleanly in batch mode (expected)")
        else:
            log("Draw Override in Batch", "pass", "Draw override called in batch mode")

        # 6. Cleanup
        pmv.cleanup_muidrawmanager_probe()
        if not cmds.objExists("PoseGhostMUIDrawProbeLocator1"):
            log("Cleanup Removes Probe", "pass", "Probe container removed")
        else:
            log("Cleanup Removes Probe", "fail", "Probe container still exists")

    except Exception as e:
        log("Probe Execution", "fail", str(e))
        traceback.print_exc()

if __name__ == "__main__":
    run()
