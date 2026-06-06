"""
V2 Viewport Backend Probe — Interactive Load Path Test
======================================================

Tests the exact import/load sequence that Raz uses in the Maya UI.
Ensures run_cube_proof() doesn't fail with a false "Plugin not loaded"
when imported normally.
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

    import maya.cmds as cmds

    try:
        # Step 1: Set up paths
        probe_dir = os.path.abspath('work/09_v2_viewport_backend_probe')
        probe_path = os.path.join(probe_dir, "probe_viewport_backend.py")

        if probe_dir not in sys.path:
            sys.path.insert(0, probe_dir)

        # Step 2: Unload if already loaded
        if cmds.pluginInfo("probe_viewport_backend", query=True, loaded=True):
            cmds.unloadPlugin("probe_viewport_backend", force=True)

        if "probe_viewport_backend" in sys.modules:
            del sys.modules["probe_viewport_backend"]

        # Step 3: Load the plugin via file path
        cmds.loadPlugin(probe_path)
        is_loaded = cmds.pluginInfo("probe_viewport_backend", query=True, loaded=True)
        
        log("Plugin Registry Load", "pass" if is_loaded else "fail",
            f"loaded={is_loaded}")

        # Step 4: Import the module
        import probe_viewport_backend as pvb

        # Step 5: Test the helper method
        helper_result = pvb.is_probe_plugin_loaded()
        log("is_probe_plugin_loaded Helper", "pass" if helper_result else "fail",
            f"result={helper_result}")

        # Step 6: Run the cube proof
        # In batch mode, visual VP2 stuff isn't proven, but the script logic should
        # get all the way through node creation and data feeding without 
        # exiting early due to the plugin load check.
        proof_results = pvb.run_cube_proof(debug=True)
        
        if proof_results is not None:
            # We successfully got to the end of the proof returning a dict
            log("run_cube_proof Execution", "pass",
                f"Returned successfully: {proof_results}")
        else:
            log("run_cube_proof Execution", "fail",
                "Returned None. It likely failed the plugin load check and returned early.")

    except Exception as e:
        log("Interactive Load Path Test", "fail", traceback.format_exc())

    finally:
        try:
            cmds.file(new=True, force=True)
            maya.standalone.uninitialize()
        except:
            pass

    # ---- Summary ----
    print("\n--- RESULTS JSON ---")
    print(json.dumps(results, indent=2))

    passed = sum(1 for v in results.values() if v["status"] == "pass")
    failed = sum(1 for v in results.values() if v["status"] == "fail")
    print(f"\nTotal: {len(results)} | Pass: {passed} | Fail: {failed}")

if __name__ == "__main__":
    run_tests()
