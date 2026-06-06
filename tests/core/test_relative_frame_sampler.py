import unittest
from pose_ghost.core import OnionSettings, RelativeFrameSampler, DisplayMode

class TestRelativeFrameSampler(unittest.TestCase):
    def test_default_sampling(self):
        settings = OnionSettings(previous_count=3, next_count=3, frame_step=1, clamp_to_playback_range=False)
        plan = RelativeFrameSampler.generate_plan(30.0, settings)
        
        prev_frames = [s.frame for s in plan.previous_samples]
        next_frames = [s.frame for s in plan.next_samples]
        
        self.assertEqual(prev_frames, [29.0, 28.0, 27.0])
        self.assertEqual(next_frames, [31.0, 32.0, 33.0])
        
    def test_frame_step(self):
        settings = OnionSettings(previous_count=3, next_count=3, frame_step=2, clamp_to_playback_range=False)
        plan = RelativeFrameSampler.generate_plan(30.0, settings)
        
        prev_frames = [s.frame for s in plan.previous_samples]
        next_frames = [s.frame for s in plan.next_samples]
        
        self.assertEqual(prev_frames, [28.0, 26.0, 24.0])
        self.assertEqual(next_frames, [32.0, 34.0, 36.0])

    def test_display_mode_previous(self):
        settings = OnionSettings(display_mode=DisplayMode.PREVIOUS, previous_count=3, next_count=3, clamp_to_playback_range=False)
        plan = RelativeFrameSampler.generate_plan(30.0, settings)
        self.assertEqual(len(plan.previous_samples), 3)
        self.assertEqual(len(plan.next_samples), 0)

    def test_display_mode_next(self):
        settings = OnionSettings(display_mode=DisplayMode.NEXT, previous_count=3, next_count=3, clamp_to_playback_range=False)
        plan = RelativeFrameSampler.generate_plan(30.0, settings)
        self.assertEqual(len(plan.previous_samples), 0)
        self.assertEqual(len(plan.next_samples), 3)

    def test_clamp_to_playback_range_true(self):
        settings = OnionSettings(previous_count=5, next_count=5, clamp_to_playback_range=True, playback_min_frame=28.0, playback_max_frame=32.0)
        plan = RelativeFrameSampler.generate_plan(30.0, settings)
        
        prev_frames = [s.frame for s in plan.previous_samples]
        next_frames = [s.frame for s in plan.next_samples]
        
        self.assertEqual(prev_frames, [29.0, 28.0])
        self.assertEqual(next_frames, [31.0, 32.0])

    def test_clamp_to_playback_range_false(self):
        settings = OnionSettings(previous_count=5, next_count=5, clamp_to_playback_range=False, playback_min_frame=28.0, playback_max_frame=32.0)
        plan = RelativeFrameSampler.generate_plan(30.0, settings)
        
        self.assertEqual(len(plan.previous_samples), 5)
        self.assertEqual(len(plan.next_samples), 5)

    def test_zero_counts(self):
        settings = OnionSettings(previous_count=0, next_count=0)
        plan = RelativeFrameSampler.generate_plan(30.0, settings)
        self.assertEqual(len(plan.previous_samples), 0)
        self.assertEqual(len(plan.next_samples), 0)
        
    def test_negative_counts_normalized(self):
        settings = OnionSettings(previous_count=-5, next_count=-1)
        plan = RelativeFrameSampler.generate_plan(30.0, settings)
        self.assertEqual(len(plan.previous_samples), 0)
        self.assertEqual(len(plan.next_samples), 0)

if __name__ == '__main__':
    unittest.main()