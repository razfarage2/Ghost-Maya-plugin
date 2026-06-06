import maya.cmds as cmds

class DisplayLayerManager:
    """
    Manages the Maya display groups and layers for Pose Ghost.
    """
    ROOT_GRP = "PoseGhostGrp"
    PREV_GRP = "PoseGhostPreviousGrp"
    NEXT_GRP = "PoseGhostNextGrp"
    
    @classmethod
    def setup_groups(cls):
        if not cmds.objExists(cls.ROOT_GRP):
            cmds.group(empty=True, name=cls.ROOT_GRP)
            # Make root non-renderable? We can just leave it as transform.
            
        if not cmds.objExists(cls.PREV_GRP):
            cmds.group(empty=True, name=cls.PREV_GRP, parent=cls.ROOT_GRP)
            
        if not cmds.objExists(cls.NEXT_GRP):
            cmds.group(empty=True, name=cls.NEXT_GRP, parent=cls.ROOT_GRP)

    @classmethod
    def get_group(cls, side: str) -> str:
        cls.setup_groups()
        return cls.PREV_GRP if side == "previous" else cls.NEXT_GRP

    @classmethod
    def clear_all(cls):
        if cmds.objExists(cls.ROOT_GRP):
            cmds.delete(cls.ROOT_GRP)

    @classmethod
    def clear_side(cls, side: str):
        grp = cls.PREV_GRP if side == "previous" else cls.NEXT_GRP
        if cmds.objExists(grp):
            children = cmds.listRelatives(grp, children=True, fullPath=True)
            if children:
                cmds.delete(children)

    @classmethod
    def make_non_renderable(cls, node: str):
        """
        Sets non-renderable flags on the shapes of the given node.
        """
        shapes = cmds.listRelatives(node, shapes=True, fullPath=True) or []
        for s in shapes:
            if cmds.objExists(f"{s}.castsShadows"):
                cmds.setAttr(f"{s}.castsShadows", 0)
            if cmds.objExists(f"{s}.receiveShadows"):
                cmds.setAttr(f"{s}.receiveShadows", 0)
            if cmds.objExists(f"{s}.primaryVisibility"):
                cmds.setAttr(f"{s}.primaryVisibility", 0)
            
            # Optional: Display overrides
            if cmds.objExists(f"{s}.overrideEnabled"):
                cmds.setAttr(f"{s}.overrideEnabled", 1)
                cmds.setAttr(f"{s}.overrideDisplayType", 2) # 2 = Reference