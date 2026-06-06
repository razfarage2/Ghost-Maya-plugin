import unittest
from pose_ghost.core import OnionSettings
from pose_ghost.runtime.controller import Controller
from pose_ghost.runtime.update_queue import UpdateQueue
from pose_ghost.runtime.event_router import HeavyRigModeEvent

class TestHeavyModeStatus(unittest.TestCase):
    def setUp(self):
        self.queue = UpdateQueue()
        self.controller = Controller(self.queue)

    def test_heavy_rig_mode_status_update(self):
        self.controller.handle_event(HeavyRigModeEvent(enabled=True))
        
        self.assertTrue(self.controller.heavy_rig_mode_enabled)
        req = self.queue.drain_latest()
        self.assertIsNotNone(req)
        self.assertEqual(req["action"], "multi")
        reqs = req["requests"]
        self.assertTrue(any(r["action"] == "status" and r["text"] == "Status: Heavy Rig Mode — ghosts frozen" for r in reqs))

    def test_heavy_rig_mode_off_status_update(self):
        self.controller.handle_event(HeavyRigModeEvent(enabled=True))
        self.queue._requests.clear() # clear queue
        
        self.controller.handle_event(HeavyRigModeEvent(enabled=False))
        
        self.assertFalse(self.controller.heavy_rig_mode_enabled)
        # Should enqueue a status Live and a rebuild (evaluate and enqueue)
        reqs = self.queue._requests
        self.assertTrue(any(r["action"] == "status" and r["text"] == "Status: Live" for r in reqs))

if __name__ == '__main__':
    unittest.main()
