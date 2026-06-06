import unittest
from pose_ghost.runtime.callback_registry import CallbackRegistry

class TestCallbackRegistry(unittest.TestCase):
    def test_register_and_clear(self):
        registry = CallbackRegistry()
        
        removed_ids = []
        def remover(cb_id):
            removed_ids.append(cb_id)
            
        registry.register("id1", remover)
        registry.register("id2", remover)
        
        registry.clear()
        
        self.assertIn("id1", removed_ids)
        self.assertIn("id2", removed_ids)
        self.assertEqual(len(removed_ids), 2)
        
    def test_clear_is_idempotent(self):
        registry = CallbackRegistry()
        
        removed_ids = []
        def remover(cb_id):
            removed_ids.append(cb_id)
            
        registry.register("id1", remover)
        
        registry.clear()
        registry.clear()
        
        self.assertEqual(len(removed_ids), 1)

if __name__ == '__main__':
    unittest.main()
