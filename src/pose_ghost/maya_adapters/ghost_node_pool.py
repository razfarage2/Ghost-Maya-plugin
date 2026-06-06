import maya.cmds as cmds
import collections

class GhostNodePool:
    """
    Manages a pool of duplicated ghost nodes keyed by (target_path, frame).
    """
    _pool: dict[tuple[str, float], str] = collections.OrderedDict()
    MAX_SIZE = 100

    @classmethod
    def get_node(cls, target_path: str, frame: float) -> str:
        key = (target_path, frame)
        if key in cls._pool:
            node = cls._pool[key]
            # Move to end to mark as recently used
            cls._pool.move_to_end(key)
            if cmds.objExists(node):
                return node
            else:
                # Node was deleted externally
                cls._pool.pop(key)
        return ""

    @classmethod
    def add_node(cls, target_path: str, frame: float, node: str):
        key = (target_path, frame)
        if key in cls._pool:
            old_node = cls._pool.pop(key)
            if cmds.objExists(old_node) and old_node != node:
                cmds.delete(old_node)
                
        cls._pool[key] = node
        cls._evict_oldest()

    @classmethod
    def hide_unused(cls, active_keys: set[tuple[str, float]]):
        """
        Hides all nodes in the pool that are not in the active_keys set.
        """
        for key, node in cls._pool.items():
            if key not in active_keys:
                if cmds.objExists(node):
                    if cmds.getAttr(f"{node}.visibility"):
                        cmds.setAttr(f"{node}.visibility", 0)

    @classmethod
    def clear(cls):
        for node in cls._pool.values():
            if cmds.objExists(node):
                cmds.delete(node)
        cls._pool.clear()

    @classmethod
    def invalidate_target(cls, target_path: str):
        keys_to_remove = [k for k in cls._pool.keys() if k[0] == target_path]
        for k in keys_to_remove:
            node = cls._pool.pop(k)
            if cmds.objExists(node):
                cmds.delete(node)

    @classmethod
    def _evict_oldest(cls):
        while len(cls._pool) > cls.MAX_SIZE:
            key, node = cls._pool.popitem(last=False)
            if cmds.objExists(node):
                cmds.delete(node)
