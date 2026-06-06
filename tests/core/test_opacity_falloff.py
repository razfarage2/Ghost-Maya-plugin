import unittest
from pose_ghost.core import OpacityFalloff

class TestOpacityFalloff(unittest.TestCase):
    def test_falloff_disabled(self):
        op1 = OpacityFalloff.calculate_opacity(1, 0.5, 0.8, False)
        op2 = OpacityFalloff.calculate_opacity(2, 0.5, 0.8, False)
        op3 = OpacityFalloff.calculate_opacity(3, 0.5, 0.8, False)
        
        self.assertEqual(op1, 0.5)
        self.assertEqual(op2, 0.5)
        self.assertEqual(op3, 0.5)

    def test_falloff_enabled(self):
        op1 = OpacityFalloff.calculate_opacity(1, 0.5, 0.8, True)
        op2 = OpacityFalloff.calculate_opacity(2, 0.5, 0.8, True)
        op3 = OpacityFalloff.calculate_opacity(3, 0.5, 0.8, True)
        
        self.assertAlmostEqual(op1, 0.5)
        self.assertAlmostEqual(op2, 0.4)    # 0.5 * 0.8
        self.assertAlmostEqual(op3, 0.32)   # 0.5 * 0.8 * 0.8

    def test_opacity_clamped(self):
        # Even if base opacity is high or fade is > 1 (though Settings normally normalizes), Falloff clamps
        op_high = OpacityFalloff.calculate_opacity(1, 1.5, 1.0, True)
        self.assertEqual(op_high, 1.0)
        
        op_low = OpacityFalloff.calculate_opacity(5, 0.5, 0.0, True)
        self.assertEqual(op_low, 0.0)

if __name__ == '__main__':
    unittest.main()