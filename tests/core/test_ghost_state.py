import unittest
from pose_ghost.core import GhostState, SamplePlan, OnionSettings, OnionSample, DisplayMode

class TestGhostState(unittest.TestCase):
    def setUp(self):
        self.settings = OnionSettings()
        self.plan = SamplePlan()
        self.plan.previous_samples.append(OnionSample(frame=10.0, side="previous", index=1, opacity=0.5))
        self.state = GhostState(sample_plan=self.plan, settings=self.settings, target_signature="target_v1")

    def test_unchanged_state(self):
        new_plan = SamplePlan()
        new_plan.previous_samples.append(OnionSample(frame=10.0, side="previous", index=1, opacity=0.5))
        new_settings = OnionSettings()
        
        self.assertFalse(self.state.requires_rebuild(new_plan, new_settings, "target_v1"))

    def test_changed_target_signature(self):
        self.assertTrue(self.state.requires_rebuild(self.plan, self.settings, "target_v2"))

    def test_changed_sample_frames(self):
        new_plan = SamplePlan()
        new_plan.previous_samples.append(OnionSample(frame=11.0, side="previous", index=1, opacity=0.5))
        self.assertTrue(self.state.requires_rebuild(new_plan, self.settings, "target_v1"))

    def test_changed_display_mode(self):
        new_settings = OnionSettings(display_mode=DisplayMode.PREVIOUS)
        self.assertTrue(self.state.requires_rebuild(self.plan, new_settings, "target_v1"))

    def test_changed_opacity(self):
        new_settings = OnionSettings(base_opacity=0.5)
        self.assertFalse(self.state.requires_rebuild(self.plan, new_settings, "target_v1"))

if __name__ == '__main__':
    unittest.main()