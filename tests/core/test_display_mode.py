import unittest
from pose_ghost.core import DisplayMode, OnionSettings

class TestDisplayMode(unittest.TestCase):
    def test_display_mode_validation(self):
        self.assertTrue(DisplayMode.is_valid("both"))
        self.assertTrue(DisplayMode.is_valid("previous"))
        self.assertTrue(DisplayMode.is_valid("next"))
        self.assertFalse(DisplayMode.is_valid("invalid_mode"))
        
    def test_settings_mode_normalization(self):
        settings = OnionSettings(display_mode="previous")
        self.assertEqual(settings.display_mode, DisplayMode.PREVIOUS)
        
    def test_settings_invalid_mode(self):
        with self.assertRaises(ValueError):
            OnionSettings(display_mode="invalid")

if __name__ == '__main__':
    unittest.main()