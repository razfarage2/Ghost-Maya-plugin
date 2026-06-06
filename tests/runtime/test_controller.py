import unittest
from pose_ghost.runtime.controller import Controller
from pose_ghost.runtime.update_queue import UpdateQueue
from pose_ghost.runtime.event_router import (
    TimeChangeEvent, KeyEditEvent, PlaybackStartedEvent,
    PlaybackStoppedEvent, SettingsChangedEvent, ForceRebuildEvent, EnableStateChangedEvent
)
from pose_ghost.core import OnionSettings

class TestController(unittest.TestCase):
    def setUp(self):
        self.queue = UpdateQueue()
        self.controller = Controller(self.queue)

    def test_time_change_builds_plan(self):
        self.controller.handle_event(TimeChangeEvent(frame=10.0))
        self.assertTrue(self.queue.has_pending())
        req = self.queue.drain_latest()
        self.assertEqual(req["action"], "rebuild")
        self.assertIsNotNone(req["state"])

    def test_duplicate_time_change_no_rebuild(self):
        self.controller.handle_event(TimeChangeEvent(frame=10.0))
        self.queue.drain_latest() # clear it
        
        self.controller.handle_event(TimeChangeEvent(frame=10.0))
        self.assertFalse(self.queue.has_pending())

    def test_changed_frame_enqueues_rebuild(self):
        self.controller.handle_event(TimeChangeEvent(frame=10.0))
        self.queue.drain_latest()
        
        self.controller.handle_event(TimeChangeEvent(frame=11.0))
        self.assertTrue(self.queue.has_pending())

    def test_settings_change_enqueues_rebuild(self):
        self.controller.handle_event(TimeChangeEvent(frame=10.0))
        self.queue.drain_latest()
        
        new_settings = OnionSettings(base_opacity=0.9)
        self.controller.update_settings(new_settings)
        self.assertTrue(self.queue.has_pending())

    def test_disabled_does_not_enqueue_rebuild(self):
        self.controller.handle_event(EnableStateChangedEvent(enabled=False))
        req = self.queue.drain_latest()
        self.assertEqual(req["action"], "clear")
        
        self.controller.handle_event(TimeChangeEvent(frame=10.0))
        self.assertFalse(self.queue.has_pending())

    def test_force_rebuild(self):
        self.controller.handle_event(TimeChangeEvent(frame=10.0))
        self.queue.drain_latest()
        
        self.controller.handle_event(ForceRebuildEvent())
        self.assertTrue(self.queue.has_pending())

    def test_playback_suppresses_time_change(self):
        self.controller.handle_event(PlaybackStartedEvent())
        self.controller.handle_event(TimeChangeEvent(frame=10.0))
        self.assertFalse(self.queue.has_pending())

    def test_playback_stop_queues_rebuild(self):
        self.controller.handle_event(PlaybackStartedEvent())
        self.controller.handle_event(TimeChangeEvent(frame=10.0))
        self.controller.handle_event(PlaybackStoppedEvent())
        self.assertTrue(self.queue.has_pending())

    def test_key_edit_marks_dirty(self):
        self.controller.handle_event(TimeChangeEvent(frame=10.0))
        self.queue.drain_latest()
        
        self.controller.handle_event(KeyEditEvent())
        self.assertTrue(self.queue.has_pending())

    def test_key_edit_during_playback_defers_rebuild(self):
        self.controller.handle_event(PlaybackStartedEvent())
        self.controller.handle_event(KeyEditEvent())
        self.assertFalse(self.queue.has_pending())
        
        self.controller.handle_event(PlaybackStoppedEvent())
        self.assertTrue(self.queue.has_pending())

    def test_internal_time_change_guard(self):
        with self.controller.internal_time_change():
            self.controller.handle_event(TimeChangeEvent(frame=10.0))
        self.assertFalse(self.queue.has_pending())

if __name__ == '__main__':
    unittest.main()
