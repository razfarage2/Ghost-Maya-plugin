import unittest
from pose_ghost.ui.pose_ghost_panel import PoseGhostPanel
from pose_ghost.ui.ui_commands import FakeUiCommands
from pose_ghost.ui.qt_compat import QT_AVAILABLE
from pose_ghost.core import DisplayMode

class TestPoseGhostPanelLogic(unittest.TestCase):
    def setUp(self):
        self.commands = FakeUiCommands()
        self.panel = PoseGhostPanel(self.commands)

    def test_build_ui_returns_widget_if_qt(self):
        widget = self.panel.build_ui()
        if QT_AVAILABLE:
            self.assertIsNotNone(widget)
        else:
            self.assertIsNone(widget)

    def test_seam_calls(self):
        if not QT_AVAILABLE:
            self.skipTest("Qt not available")
            
        self.panel.build_ui()
        
        # Test basic button clicks route to commands
        self.panel.btn_enable.setChecked(False) # triggers toggle
        self.panel._on_display_mode_changed(1) # Show Previous
        
        methods_called = [c["method"] for c in self.commands.calls]
        self.assertIn("disable", methods_called)
        self.assertIn("set_display_mode", methods_called)

        # Find the set_display_mode call
        mode_call = next(c for c in self.commands.calls if c["method"] == "set_display_mode")
        self.assertEqual(mode_call["args"][0], DisplayMode.PREVIOUS)

if __name__ == '__main__':
    unittest.main()
