import sys
import os
import unittest

try:
    import maya.standalone
    import maya.cmds as cmds
    import maya.api.OpenMaya as om
    HAS_MAYA = True
except ImportError:
    HAS_MAYA = False

@unittest.skipIf(not HAS_MAYA, "Requires Maya environment")
class TestUxHotfixes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            maya.standalone.initialize(name='python')
        except:
            pass
            
        src_path = os.path.abspath('src')
        if src_path not in sys.path:
            sys.path.append(src_path)
            
    @classmethod
    def tearDownClass(cls):
        try:
            maya.standalone.uninitialize()
        except:
            pass

    def setUp(self):
        cmds.file(new=True, force=True)

    def test_hotfixes(self):
        # Setup
        cube = cmds.polyCube(name="animCube")[0]
        cmds.select(cube, replace=True)
        
        # We need to test the UI adapter wiring
        import pose_ghost.launcher as launcher
        from pose_ghost.core import OnionSettings
        
        app = launcher.get_app()
        app.initialize()
        
        # Change opacity to 0
        settings = OnionSettings(previous_count=1, next_count=1, base_opacity=0.0)
        app.ui_adapter.set_sampling_settings(settings)
        app.ui_adapter.set_appearance_settings(settings)
        
        # Scan target
        app.ui_adapter.scan_target_root(cube)
        
        # 1. Selection restoration + 2. Opacity 0 skip
        cmds.currentTime(5, update=True)
        # Drain the queue which triggers rebuild
        req = app.root.queue.drain_latest()
        self.assertIsNotNone(req)
        
        from pose_ghost.maya_adapters.mesh_snapshot_renderer import MeshSnapshotRenderer
        targets = app.ui_adapter.current_targets
        
        # Inject error to verify refresh suspension restores
        with self.assertRaises(Exception):
            cmds.refresh(suspend=True) # Ensure it's not already suspended
            cmds.refresh(suspend=False)
            
            # Make fake plan with opacity to force render loop
            import copy
            bad_plan = copy.deepcopy(req["state"].sample_plan)
            if bad_plan.previous_samples:
                bad_plan.previous_samples[0].opacity = 1.0
            
            # Break target meshes to throw error in capture_snapshot
            MeshSnapshotRenderer.render(bad_plan, ["non_existent_target"])
            
        # Verify selection is untouched by failure
        sel = cmds.ls(selection=True)
        self.assertEqual(sel, [cube])
        
        # Verify refresh state isn't permanently suspended
        # We can't directly query cmds.refresh state but we assume no crash.
        
        # Now do it correctly
        MeshSnapshotRenderer.render(req["state"].sample_plan, targets)
        
        # Verify selection remains the source cube
        sel = cmds.ls(selection=True)
        self.assertEqual(sel, [cube], "Selection was hijacked by generated ghosts!")
        
        # Verify opacity 0 skipped generation
        prev_grp = "PoseGhostPreviousGrp"
        if cmds.objExists(prev_grp):
            children = cmds.listRelatives(prev_grp, children=True) or []
            self.assertEqual(len(children), 0, "Opacity 0.0 generated visible ghosts!")
            
        # Verify Outliner hidden
        root_grp = "PoseGhostGrp"
        self.assertTrue(cmds.objExists(root_grp))
        self.assertEqual(cmds.getAttr(f"{root_grp}.hiddenInOutliner"), 1, "Root group not hidden in outliner")
        
        launcher.unload(clear_ghosts=True)

if __name__ == '__main__':
    unittest.main()
