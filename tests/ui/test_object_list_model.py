import unittest
from pose_ghost.ui.object_list_model import ObjectListModel, TargetRowData

class TestObjectListModel(unittest.TestCase):
    def test_set_and_get_rows(self):
        model = ObjectListModel()
        rows = [
            TargetRowData("id1", "Obj1", "|group|Obj1", False, "original"),
            TargetRowData("id2", "Obj2", "|group|Obj2", True, "original")
        ]
        model.set_rows(rows)
        
        fetched = model.get_rows()
        self.assertEqual(len(fetched), 2)
        self.assertEqual(fetched[0].object_id, "id1")

    def test_set_bypass(self):
        model = ObjectListModel()
        rows = [TargetRowData("id1", "Obj1", "|group|Obj1", False, "original")]
        model.set_rows(rows)
        
        self.assertFalse(model.get_row("id1").bypassed)
        model.set_bypass("id1", True)
        self.assertTrue(model.get_row("id1").bypassed)

if __name__ == '__main__':
    unittest.main()
