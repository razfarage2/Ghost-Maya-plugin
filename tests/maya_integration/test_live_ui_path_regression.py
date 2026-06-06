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

    sys.path.append(os.path.abspath('src'))
    
    import maya.cmds as cmds
    from pose_ghost.core import OnionSettings, DisplayMode
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

        # ----------------------------------------------------
        # 1. Force Rebuild works through UI path
        # ----------------------------------------------------
        app.ui_adapter.scan_target_root(cube)
        app.ui_adapter.force_rebuild()
        
        prevs = cmds.listRelatives("PoseGhostPreviousGrp", children=True) or []
        vis_prevs = [p for p in prevs if cmds.getAttr(f"{p}.visibility")]
        log("Force Rebuild UI", "confirmed" if len(vis_prevs) == 3 else "fail", f"Vis prevs: {len(vis_prevs)}")

        # ----------------------------------------------------
        # 2. Show Both produces previous and next ghosts
        # ----------------------------------------------------
        app.ui_adapter.set_display_mode(DisplayMode.BOTH)
        app.ui_adapter.force_rebuild()
        prevs2 = cmds.listRelatives("PoseGhostPreviousGrp", children=True) or []
        nexts2 = cmds.listRelatives("PoseGhostNextGrp", children=True) or []
        
        vis_prevs2 = [p for p in prevs2 if cmds.getAttr(f"{p}.visibility")]
        vis_nexts2 = [n for n in nexts2 if cmds.getAttr(f"{n}.visibility")]
        
        log("Show Both UI", "confirmed" if len(vis_prevs2) > 0 and len(vis_nexts2) > 0 else "fail", 
            f"Prevs: {len(vis_prevs2)}, Nexts: {len(vis_nexts2)}")

        # ----------------------------------------------------
        # 3. Opacity 0 hides/skips visible ghosts
        # ----------------------------------------------------
        app.ui_adapter.set_appearance_settings(OnionSettings(base_opacity=0.0, opacity_falloff_enabled=False))
        # Appearance update should hide the ghost
        app.process_pending_updates()
        
        vis_prevs3 = [p for p in prevs2 if cmds.getAttr(f"{p}.visibility")]
        log("Opacity 0 Hides", "confirmed" if len(vis_prevs3) == 0 else "fail", f"Vis prevs: {len(vis_prevs3)}")

        # ----------------------------------------------------
        # 4. Opacity 0.30 updates material without geometry recapture
        # ----------------------------------------------------
        pool_size_before = len(GhostNodePool._pool)
        app.ui_adapter.set_appearance_settings(OnionSettings(base_opacity=0.30, opacity_falloff_enabled=False))
        app.process_pending_updates()
        
        vis_prevs4 = [p for p in prevs2 if cmds.getAttr(f"{p}.visibility")]
        pool_size_after = len(GhostNodePool._pool)
        
        mat_assigned = False
        if vis_prevs4:
            mats = cmds.listConnections(cmds.listHistory(vis_prevs4[0], future=True), type='shadingEngine')
            mat_assigned = "PoseGhost" in str(mats)
            
        is_safe = (len(vis_prevs4) > 0 and pool_size_before == pool_size_after and mat_assigned)
        log("Opacity Update No Recapture", "confirmed" if is_safe else "fail", f"Pool {pool_size_before}->{pool_size_after}")

        # ----------------------------------------------------
        # 5. Cache is reused through live UI path
        # ----------------------------------------------------
        # Forcing rebuild again without moving time should reuse same pool
        app.ui_adapter.force_rebuild()
        pool_size_after_rebuild = len(GhostNodePool._pool)
        log("Cache Reused on Force Rebuild", "confirmed" if pool_size_after_rebuild == pool_size_after else "fail", f"Pool {pool_size_after}->{pool_size_after_rebuild}")

        # ----------------------------------------------------
        # 6. Source selection remains restored
        # ----------------------------------------------------
        cmds.select(cube, replace=True)
        app.ui_adapter.force_rebuild()
        sel = cmds.ls(selection=True)
        log("Source Selection Restored", "confirmed" if sel and sel[0] == cube else "fail", f"Selection: {sel}")

    except Exception as e:
        log("Global UI Regression Test Error", "fail", traceback.format_exc())

    finally:
        try:
            maya.standalone.uninitialize()
        except:
            pass

    print("\n--- RESULTS JSON ---")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    run_tests()
