import unittest
import time
from pose_ghost.core import OnionSettings
from pose_ghost.runtime.controller import Controller
from pose_ghost.runtime.update_queue import UpdateQueue
from pose_ghost.runtime.event_router import (
    KeyEditEvent, TimeChangeEvent, HeavyRigModeEvent, ForceRebuildEvent
)

class TestStaleDirtyState(unittest.TestCase):
    def setUp(self):
        self.queue = UpdateQueue()
        self.controller = Controller(self.queue)

    def test_key_edit_marks_stale_and_enqueues_status(self):
        self.controller.handle_event(KeyEditEvent(timestamp=100.0))
        self.assertTrue(self.controller.is_stale)
        self.assertEqual(self.controller.dirty_reason, "Animation changed")
        self.assertEqual(self.controller.last_dirty_time, 100.0)
        self.assertTrue(self.controller.pending_auto_rebuild)
        
        # Check queue
        reqs = self.queue._requests
        self.assertEqual(len(reqs), 2)
        self.assertEqual(reqs[0]["action"], "status")
        self.assertEqual(reqs[0]["text"], "Status: Stale — animation changed")
        self.assertEqual(reqs[1]["action"], "invalidate_cache")

    def test_debounce_ignores_quick_edits(self):
        self.controller.handle_event(KeyEditEvent(timestamp=time.time()))
        self.controller.check_debounce()
        # Should still be pending because 300ms hasn't elapsed
        self.assertTrue(self.controller.pending_auto_rebuild)

    def test_debounce_triggers_after_delay(self):
        self.controller.handle_event(KeyEditEvent(timestamp=time.time() - 0.5))
        self.controller.check_debounce()
        # Should trigger auto rebuild
        self.assertFalse(self.controller.pending_auto_rebuild)
        self.assertFalse(self.controller.is_stale) # Cleared by force_enqueue
        
        # Last queue item should be a multi request
        req = self.queue.drain_latest()
        self.assertIsNotNone(req)
        self.assertEqual(req["action"], "multi")
        reqs = req["requests"]
        
        has_status = any(r["action"] == "status" and r["text"] == "Status: Live" for r in reqs)
        self.assertTrue(has_status)
        
        has_rebuild = any(r["action"] == "rebuild" for r in reqs)
        self.assertTrue(has_rebuild)

    def test_heavy_rig_mode_prevents_auto_rebuild(self):
        self.controller.handle_event(HeavyRigModeEvent(enabled=True))
        self.controller.handle_event(KeyEditEvent(timestamp=time.time() - 0.5))
        
        self.assertTrue(self.controller.is_stale)
        self.assertFalse(self.controller.pending_auto_rebuild)
        
        self.controller.check_debounce()
        # Still stale because rebuild was not enqueued
        self.assertTrue(self.controller.is_stale)

if __name__ == '__main__':
    unittest.main()
