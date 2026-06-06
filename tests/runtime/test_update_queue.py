import unittest
from pose_ghost.runtime.update_queue import UpdateQueue

class TestUpdateQueue(unittest.TestCase):
    def test_enqueue_and_drain(self):
        queue = UpdateQueue()
        self.assertFalse(queue.has_pending())
        
        queue.enqueue("request1")
        self.assertTrue(queue.has_pending())
        
        req = queue.drain_latest()
        self.assertEqual(req, "request1")
        self.assertFalse(queue.has_pending())
        
    def test_enqueue_overwrites(self):
        queue = UpdateQueue()
        queue.enqueue("request1")
        queue.enqueue("request2")
        
        req = queue.drain_latest()
        self.assertEqual(req, "request2")
        
    def test_clear(self):
        queue = UpdateQueue()
        queue.enqueue("request1")
        queue.clear()
        
        self.assertFalse(queue.has_pending())

if __name__ == '__main__':
    unittest.main()
