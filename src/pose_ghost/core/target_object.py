from dataclasses import dataclass
from typing import Optional

@dataclass
class TargetObject:
    id: str
    node_path: str
    display_name: str
    bypassed: bool = False
    source_mode: Optional[str] = None