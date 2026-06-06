import unittest
from pose_ghost.ui.qt_compat import QT_AVAILABLE, HAS_PYSIDE2, HAS_PYSIDE6

class TestQtCompat(unittest.TestCase):
    def test_safe_import(self):
        # We just want to ensure it imported without crashing
        self.assertIsInstance(QT_AVAILABLE, bool)
        self.assertIsInstance(HAS_PYSIDE2, bool)
        self.assertIsInstance(HAS_PYSIDE6, bool)

if __name__ == '__main__':
    unittest.main()
