import sys
import os
import unittest

try:
    import maya.standalone
    import maya.cmds as cmds
    HAS_MAYA = True
except ImportError:
    HAS_MAYA = False

@unittest.skipIf(not HAS_MAYA, "Requires Maya environment")
class TestCacheOptimization(unittest.TestCase):
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

    def test_target_scan_cache(self):
        cube = cmds.polyCube(name="testCube")[0]
        grp = cmds.group(cube, name="testGrp")
        
        from pose_ghost.maya_adapters.target_scan_cache import TargetScanCache
        from pose_ghost.maya_adapters.target_scanner import TargetScanner
        TargetScanCache.clear()
        
        # Monkeypatch TargetScanner to count calls
        orig_scan = TargetScanner.scan_target_root
        scan_count = 0
        def mock_scan(*args, **kwargs):
            nonlocal scan_count
            scan_count += 1
            return orig_scan(*args, **kwargs)
        TargetScanner.scan_target_root = mock_scan
        
        try:
            res1 = TargetScanCache.get_or_scan(grp)
            self.assertEqual(scan_count, 1)
            self.assertEqual(len(res1), 1)
            
            # Second call should use cache
            res2 = TargetScanCache.get_or_scan(grp)
            self.assertEqual(scan_count, 1)
            self.assertEqual(res1, res2)
            
            # Force call should rescan
            res3 = TargetScanCache.get_or_scan(grp, force=True)
            self.assertEqual(scan_count, 2)
            self.assertEqual(res1, res3)
            
            # Delete object, should invalidate cache next call
            cmds.delete(cube)
            res4 = TargetScanCache.get_or_scan(grp)
            # It drops invalid nodes without full rescan in this implementation
            self.assertEqual(len(res4), 0)
        finally:
            TargetScanner.scan_target_root = orig_scan
            TargetScanCache.clear()

    def test_snapshot_reuse(self):
        cube = cmds.polyCube(name="animCube")[0]
        
        import pose_ghost.launcher as launcher
        from pose_ghost.core import OnionSettings
        from pose_ghost.maya_adapters.ghost_node_pool import GhostNodePool
        
        app = launcher.get_app()
        app.initialize()
        
        settings = OnionSettings(previous_count=2, next_count=2, base_opacity=0.5)
        app.ui_adapter.set_sampling_settings(settings)
        app.ui_adapter.set_appearance_settings(settings)
        app.ui_adapter.scan_target_root(cube)
        
        cmds.currentTime(10, update=True)
        # Drain the queue to rebuild
        req = app.root.queue.drain_latest()
        
        # Manually invoke render to simulate drain
        from pose_ghost.maya_adapters.mesh_snapshot_renderer import MeshSnapshotRenderer
        targets = app.ui_adapter.current_targets
        MeshSnapshotRenderer.render(req["state"].sample_plan, targets)
        
        pool_size_1 = len(GhostNodePool._pool)
        self.assertEqual(pool_size_1, 4) # 2 prev, 2 next
        
        # Scrub timeline by 1 frame
        cmds.currentTime(11, update=True)
        req2 = app.root.queue.drain_latest()
        MeshSnapshotRenderer.render(req2["state"].sample_plan, targets)
        
        # Due to overlap, frame 9 and 10 and 12 were already generated or needed.
        # It should reuse cached nodes rather than growing by 4.
        # new frames needed: 13, 8 (if step is 1)
        pool_size_2 = len(GhostNodePool._pool)
        self.assertLess(pool_size_2, pool_size_1 + 4)
        
        launcher.unload(clear_ghosts=True)

    def test_material_only_update(self):
        cube = cmds.polyCube(name="matCube")[0]
        
        import pose_ghost.launcher as launcher
        from pose_ghost.core import OnionSettings
        from pose_ghost.maya_adapters.ghost_node_pool import GhostNodePool
        
        app = launcher.get_app()
        app.initialize()
        
        settings = OnionSettings(previous_count=1, next_count=1, base_opacity=0.1)
        app.ui_adapter.set_sampling_settings(settings)
        app.ui_adapter.set_appearance_settings(settings)
        app.ui_adapter.scan_target_root(cube)
        
        cmds.currentTime(5, update=True)
        req = app.root.queue.drain_latest()
        from pose_ghost.maya_adapters.mesh_snapshot_renderer import MeshSnapshotRenderer
        targets = app.ui_adapter.current_targets
        MeshSnapshotRenderer.render(req["state"].sample_plan, targets)
        
        # Get ghost node for prev
        ghost_node = list(GhostNodePool._pool.values())[0]
        self.assertTrue(cmds.getAttr(f"{ghost_node}.visibility"))
        
        # Change opacity to trigger appearance only
        settings.base_opacity = 0.3
        app.ui_adapter.set_appearance_settings(settings)
        
        req2 = app.root.queue.drain_latest()
        self.assertEqual(req2["action"], "appearance")
        
        MeshSnapshotRenderer.apply_appearance_only(req2["state"].sample_plan, targets)
        
        # Pool size should not change
        self.assertEqual(len(GhostNodePool._pool), 2)
        
        # Change opacity to 0 to test skipping
        settings.base_opacity = 0.0
        app.ui_adapter.set_appearance_settings(settings)
        req3 = app.root.queue.drain_latest()
        MeshSnapshotRenderer.apply_appearance_only(req3["state"].sample_plan, targets)
        
        # Should be hidden
        self.assertFalse(cmds.getAttr(f"{ghost_node}.visibility"))

        launcher.unload(clear_ghosts=True)

if __name__ == '__main__':
    unittest.main()
