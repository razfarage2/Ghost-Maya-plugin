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

    # Simulate module path addition
    src_path = os.path.abspath('src')
    sys.path.append(src_path)

    try:
        # 1. Import Launcher
        import maya.cmds as cmds
        cmds.file(new=True, force=True)
        import pose_ghost.launcher as launcher
        log("Import Launcher", "confirmed", "Import successful.")

        print("Calling show...")
        # 2. Show (Headless fallback expected since Qt is unavailable in mayapy by default)
        launcher.show()
        print("Show finished.")
        
        app = launcher.get_app()
        is_init = app._initialized
        has_cbs = len(app.root.registry._callbacks) > 0
        
        log("Show/Initialize", "confirmed" if is_init and has_cbs else "fail", f"Init: {is_init}, Callbacks active: {has_cbs}")

        # 3. Unload Validation
        launcher.unload(clear_ghosts=True)
        
        # Verify app destroyed or cleanup success
        # The global _APP_INSTANCE is set to None by unload()
        is_cleared = launcher._APP_INSTANCE is None
        # But wait, app instance is a local variable here.
        cbs_after = len(app.root.registry._callbacks)
        
        log("Unload/Cleanup", "confirmed" if is_cleared and cbs_after == 0 else "fail", f"App Cleared: {is_cleared}, Callbacks remaining: {cbs_after}")

    except Exception as e:
        log("Global Load Validation Error", "fail", traceback.format_exc())

    print("\n--- RESULTS JSON ---")
    print(json.dumps(results, indent=2))

    try:
        maya.standalone.uninitialize()
    except:
        pass

if __name__ == "__main__":
    run_tests()
