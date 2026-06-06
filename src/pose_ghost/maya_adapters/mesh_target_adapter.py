import maya.cmds as cmds
from pose_ghost.core import TargetObject

class MeshTargetAdapter:
    @staticmethod
    def to_target_object(node_path: str) -> TargetObject:
        """
        Converts a Maya node path to a core TargetObject model.
        """
        short_name = node_path.split('|')[-1]
        # In a real scenario, stable_key might use a UUID: cmds.ls(node_path, uuid=True)[0]
        # Using path as ID for simplicity in V1 unless UUIDs are strictly required.
        node_id = node_path 
        
        return TargetObject(
            id=node_id,
            node_path=node_path,
            display_name=short_name,
            bypassed=False,
            source_mode="original"
        )