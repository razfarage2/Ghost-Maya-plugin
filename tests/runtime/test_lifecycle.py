import unittest
from pose_ghost.runtime.lifecycle import Lifecycle
from pose_ghost.runtime.callback_registry import CallbackRegistry
from pose_ghost.runtime.update_queue import UpdateQueue

class MockRenderer:
    def __init__(self):
        self.cleanup_called = False
        
    def cleanup(self):
        self.cleanup_called = True

class TestLifecycle(unittest.TestCase):
    def test_shutdown_cleans_up(self):
        registry = CallbackRegistry()
        queue = UpdateQueue()
        renderer = MockRenderer()
        
        registry.register("id1", lambda x: None)
        queue.enqueue("req")
        
        lifecycle = Lifecycle(registry, queue, renderer)
        lifecycle.shutdown()
        
        self.assertFalse(queue.has_pending())
        # registry internal size should be 0
        self.assertEqual(len(registry._callbacks), 0)
        self.assertTrue(renderer.cleanup_called)

    def test_shutdown_idempotent(self):
        registry = CallbackRegistry()
        queue = UpdateQueue()
        renderer = MockRenderer()
        
        lifecycle = Lifecycle(registry, queue, renderer)
        lifecycle.shutdown()
        lifecycle.shutdown() # Should not raise

if __name__ == '__main__':
    unittest.main()
