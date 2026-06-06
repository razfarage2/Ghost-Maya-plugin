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
class TestUiScanWiring(unittest.TestCase):
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

    def test_ui_command_adapter_scan(self):
        # Create a cube under a group
        cube = cmds.polyCube(name="testCube")[0]
        grp = cmds.group(cube, name="testGrp")
        
        # We need to test the ui command adapter wiring specifically
        import pose_ghost.launcher as launcher
        app = launcher.get_app()
        app.initialize()
        
        # At start, it should be empty
        self.assertEqual(len(app.ui_adapter.current_targets), 0)
        self.assertEqual(len(app.ui_model._rows), 0)
        
        # Scan the group via the UI command path
        app.ui_adapter.scan_target_root(grp)
        
        # Assert the target list is no longer empty
        self.assertGreater(len(app.ui_adapter.current_targets), 0)
        self.assertEqual(app.ui_adapter.current_targets[0], "|testGrp|testCube")
        self.assertGreater(len(app.ui_model._rows), 0)
        self.assertEqual(app.ui_model._rows[0].node_path, "|testGrp|testCube")

        # Cleanup app singleton
        launcher.unload(clear_ghosts=True)

if __name__ == '__main__':
    unittest.main()
