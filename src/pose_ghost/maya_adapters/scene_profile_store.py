import json
import maya.cmds as cmds

class SceneProfileStore:
    NODE_NAME = "POSE_GHOST_PROFILE"
    ATTR_NAME = "poseGhostProfileJson"

    @classmethod
    def _get_or_create_node(cls) -> str:
        if not cmds.objExists(cls.NODE_NAME):
            node = cmds.createNode('network', name=cls.NODE_NAME)
            cmds.addAttr(node, longName=cls.ATTR_NAME, dataType='string')
            return node
        
        # Ensure attr exists
        if not cmds.objExists(f"{cls.NODE_NAME}.{cls.ATTR_NAME}"):
            cmds.addAttr(cls.NODE_NAME, longName=cls.ATTR_NAME, dataType='string')
            
        return cls.NODE_NAME

    @classmethod
    def save_profile(cls, profile_dict: dict):
        node = cls._get_or_create_node()
        data_str = json.dumps(profile_dict)
        cmds.setAttr(f"{node}.{cls.ATTR_NAME}", data_str, type='string')

    @classmethod
    def load_profile(cls) -> dict:
        if not cmds.objExists(f"{cls.NODE_NAME}.{cls.ATTR_NAME}"):
            return {}
            
        data_str = cmds.getAttr(f"{cls.NODE_NAME}.{cls.ATTR_NAME}")
        if not data_str:
            return {}
            
        try:
            return json.loads(data_str)
        except json.JSONDecodeError:
            return {}