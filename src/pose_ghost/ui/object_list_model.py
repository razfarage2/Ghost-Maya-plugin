# src/pose_ghost/ui/object_list_model.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class TargetRowData:
    object_id: str
    display_name: str
    node_path: str
    bypassed: bool
    source_mode: str

class ObjectListModel:
    """
    Holds target rows for display in the UI.
    """
    def __init__(self):
        self._rows: List[TargetRowData] = []
        
    def set_rows(self, rows: List[TargetRowData]):
        self._rows = list(rows)
        
    def get_rows(self) -> List[TargetRowData]:
        return list(self._rows)
        
    def get_row(self, object_id: str) -> Optional[TargetRowData]:
        for row in self._rows:
            if row.object_id == object_id:
                return row
        return None
        
    def set_bypass(self, object_id: str, bypassed: bool):
        row = self.get_row(object_id)
        if row:
            row.bypassed = bypassed
            
    def clear(self):
        self._rows.clear()