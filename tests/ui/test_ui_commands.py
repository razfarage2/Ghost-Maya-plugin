import unittest
from pose_ghost.ui.ui_commands import FakeUiCommands

class TestUiCommands(unittest.TestCase):
    def test_fake_records_calls(self):
        fake = FakeUiCommands()
        fake.enable()
        fake.scan_target_root("|test")
        
        self.assertEqual(len(fake.calls), 2)
        self.assertEqual(fake.calls[0]["method"], "enable")
        self.assertEqual(fake.calls[1]["method"], "scan_target_root")
        self.assertEqual(fake.calls[1]["args"][0], "|test")

if __name__ == '__main__':
    unittest.main()
