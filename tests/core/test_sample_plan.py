import unittest
from pose_ghost.core import SamplePlan, OnionSample

class TestSamplePlan(unittest.TestCase):
    def test_is_empty(self):
        plan = SamplePlan()
        self.assertTrue(plan.is_empty())
        
        plan.previous_samples.append(OnionSample(frame=10.0, side="previous", index=1, opacity=0.5))
        self.assertFalse(plan.is_empty())

    def test_all_samples(self):
        plan = SamplePlan()
        plan.previous_samples.append(OnionSample(frame=10.0, side="previous", index=1, opacity=0.5))
        plan.next_samples.append(OnionSample(frame=30.0, side="next", index=1, opacity=0.5))
        
        samples = plan.all_samples()
        self.assertEqual(len(samples), 2)
        self.assertEqual(samples[0].frame, 10.0)
        self.assertEqual(samples[1].frame, 30.0)

    def test_frame_signature(self):
        plan = SamplePlan()
        plan.previous_samples.append(OnionSample(frame=10.0, side="previous", index=1, opacity=0.5))
        plan.next_samples.append(OnionSample(frame=30.0, side="next", index=1, opacity=0.5))
        
        sig = plan.frame_signature()
        self.assertEqual(sig, "prev:[10.0]|next:[30.0]")

if __name__ == '__main__':
    unittest.main()