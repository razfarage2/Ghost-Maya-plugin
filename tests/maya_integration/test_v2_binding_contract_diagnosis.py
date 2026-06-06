import sys
import maya.cmds as cmds
import maya.standalone

def log(name, status, details=""):
    print(f"[{status.upper()}] {name}: {details}")

def run():
    maya.standalone.initialize()
    cmds.loadPlugin("matrixNodes", quiet=True)
    
    probe_dir = r"G:\maya-plugins\Ghost-Maya-plugin\work\09_v2_viewport_backend_probe"
    if probe_dir not in sys.path:
        sys.path.insert(0, probe_dir)

    try:
        cmds.loadPlugin(r"G:\maya-plugins\Ghost-Maya-plugin\work\09_v2_viewport_backend_probe\probe_viewport_backend.py")
    except Exception as e:
        log("Plugin Load", "fail", str(e))
        return

    import probe_binding_contract
    
    try:
        results = probe_binding_contract.run_binding_diagnosis()
        log("Binding Diagnosis Execution", "pass", f"Tested {len(results)} combinations")
        
        # Verify no DAG duplicates
        ghosts = cmds.ls("Ghost_*", type="transform")
        if not ghosts:
            log("No DAG Duplicates", "pass", "0 duplicates found")
        else:
            log("No DAG Duplicates", "fail", f"{len(ghosts)} duplicates found")
            
    except Exception as e:
        log("Binding Diagnosis Execution", "fail", str(e))

if __name__ == "__main__":
    run()
