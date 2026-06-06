import maya.cmds as cmds
from .target_scanner import TargetScanner

class TargetScanCache:
    """
    Caches the results of a target hierarchy scan.
    """
    _cache: dict[str, list[str]] = {}

    @classmethod
    def get_or_scan(cls, root_path: str, force: bool = False) -> list[str]:
        if not cmds.objExists(root_path):
            cls._cache.pop(root_path, None)
            return []

        if force or root_path not in cls._cache:
            cls._cache[root_path] = TargetScanner.scan_target_root(root_path)
            return cls._cache[root_path]

        # Validate existing cache
        valid_nodes = []
        for node in cls._cache[root_path]:
            if cmds.objExists(node):
                valid_nodes.append(node)
        
        # Update cache if nodes disappeared
        if len(valid_nodes) != len(cls._cache[root_path]):
            cls._cache[root_path] = valid_nodes
            
        return cls._cache[root_path]

    @classmethod
    def invalidate(cls, root_path: str):
        cls._cache.pop(root_path, None)

    @classmethod
    def clear(cls):
        cls._cache.clear()
