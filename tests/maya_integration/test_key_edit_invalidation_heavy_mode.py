import sys
import os
import json
import traceback
import time

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

    sys.path.append(os.path.abspath('src'))
    
    import maya.cmds as cmds
    from pose_ghost.core import OnionSettings
    import pose_ghost.launcher as launcher
    from pose_ghost.maya_adapters.ghost_node_pool import GhostNodePool

    try:
        cmds.file(new=True, force=True)

        app = launcher.get_app()
        app.initialize()

        # Build rig
        cube = cmds.polyCube(name="animCube")[0]
        cmds.setKeyframe(cube, t=1, v=0, at='tx')
        cmds.setKeyframe(cube, t=10, v=10, at='tx')
        cmds.setKeyframe(cube, t=20, v=20, at='tx')
        
        cmds.currentTime(15, update=True)

        # 1. Setup
        app.ui_adapter.scan_target_root(cube)
        app.ui_adapter.force_rebuild()
        
        pool_size_before = len(GhostNodePool._pool)
        
        # 2. Key Edit Cache Invalidation
        cmds.setKeyframe(cube, t=15, v=15, at='tx') # triggers key edit event
        
        app.process_pending_updates() # Processes the status and invalidate_cache
        
        # Invalidation should clear the targeted cache entries
        pool_size_after_invalidate = len(GhostNodePool._pool)
        log("Key Edit Invalidates Cache", "confirmed" if pool_size_after_invalidate == 0 else "fail", f"Pool {pool_size_before}->{pool_size_after_invalidate}")
        
        # 3. Debounce Rebuild
        time.sleep(0.4) # Wait for debounce
        app.root.controller.check_debounce() # Manually trigger check
        app.process_pending_updates() # Process the auto rebuild
        
        pool_size_after_rebuild = len(GhostNodePool._pool)
        log("Debounced Auto-Rebuild", "confirmed" if pool_size_after_rebuild > 0 else "fail", f"Pool {pool_size_after_invalidate}->{pool_size_after_rebuild}")
        
        # 4. Heavy Rig Mode prevents auto rebuild
        app.ui_adapter.set_heavy_rig_mode(True)
        cmds.setKeyframe(cube, t=15, v=16, at='tx') # key edit
        
        app.process_pending_updates() # process invalidation
        pool_size_after_heavy_invalidate = len(GhostNodePool._pool)
        
        time.sleep(0.4)
        app.root.controller.check_debounce()
        app.process_pending_updates()
        
        pool_size_after_heavy_debounce = len(GhostNodePool._pool)
        log("Heavy Mode Prevents Auto-Rebuild", "confirmed" if pool_size_after_heavy_debounce == pool_size_after_heavy_invalidate else "fail", f"Pool {pool_size_after_heavy_invalidate}->{pool_size_after_heavy_debounce}")

        # 5. Heavy Rig Mode allows Force Rebuild
        app.ui_adapter.force_rebuild()
        pool_size_after_heavy_force = len(GhostNodePool._pool)
        log("Heavy Mode Allows Force Rebuild", "confirmed" if pool_size_after_heavy_force > 0 else "fail", f"Pool {pool_size_after_heavy_debounce}->{pool_size_after_heavy_force}")

    except Exception as e:
        log("Integration Test Error", "fail", traceback.format_exc())

    finally:
        try:
            maya.standalone.uninitialize()
        except:
            pass

    print("\n--- RESULTS JSON ---")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    run_tests()
