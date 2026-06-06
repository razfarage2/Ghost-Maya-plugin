import unittest
from pose_ghost.runtime.event_router import TimeChangeEvent

class TestEventRouter(unittest.TestCase):
    def test_event_instantiation(self):
        event = TimeChangeEvent(frame=10.0)
        self.assertEqual(event.frame, 10.0)

if __name__ == '__main__':
    unittest.main()
