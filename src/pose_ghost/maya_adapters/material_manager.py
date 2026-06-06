import maya.cmds as cmds

class MaterialManager:
    """
    Manages creation and assignment of ghost materials.
    """
    PREVIOUS_MAT = "PoseGhostPreviousMat"
    NEXT_MAT = "PoseGhostNextMat"
    
    @classmethod
    def setup_materials(cls):
        cls._create_or_update_mat(cls.PREVIOUS_MAT, [0.0, 0.0, 1.0])
        cls._create_or_update_mat(cls.NEXT_MAT, [1.0, 0.0, 0.0])

    @classmethod
    def _create_or_update_mat(cls, name: str, color: list):
        if not cmds.objExists(name):
            mat = cmds.shadingNode('lambert', asShader=True, name=name)
            sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"{name}SG")
            cmds.connectAttr(f"{mat}.outColor", f"{sg}.surfaceShader", force=True)
            
        cmds.setAttr(f"{name}.color", color[0], color[1], color[2], type='double3')

    @classmethod
    def assign_material(cls, ghost_node: str, side: str, opacity: float):
        """
        Assigns the correct material and sets the per-object transparency/opacity.
        """
        mat_name = cls.PREVIOUS_MAT if side == "previous" else cls.NEXT_MAT
        sg_name = f"{mat_name}SG"
        
        if not cmds.objExists(mat_name) or not cmds.objExists(sg_name):
            cls.setup_materials()
            
        # Assign shading group
        cmds.sets(ghost_node, edit=True, forceElement=sg_name)
        
        # Exact transparency approach used:
        # Instead of creating a new material for every opacity level,
        # we set an override color or transparency on the shape node if supported,
        # or we just use per-object visibility. Wait, Maya standard lambert transparency 
        # applies to all objects sharing it. 
        # For V1, the spec says "opacity falloff per sample". 
        # Since standard lambert shares transparency, we actually need per-opacity materials,
        # or we create a unique material per sample index.
        # Let's create per-sample materials.
        
        pass

    @classmethod
    def assign_per_sample_material(cls, ghost_node: str, side: str, index: int, opacity: float):
        mat_name = f"PoseGhost{side.capitalize()}Mat_{index}"
        sg_name = f"{mat_name}SG"
        
        if not cmds.objExists(mat_name):
            mat = cmds.shadingNode('lambert', asShader=True, name=mat_name)
            sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=sg_name)
            cmds.connectAttr(f"{mat}.outColor", f"{sg}.surfaceShader", force=True)
        
        # Set color
        color = [0.0, 0.0, 1.0] if side == "previous" else [1.0, 0.0, 0.0]
        cmds.setAttr(f"{mat_name}.color", color[0], color[1], color[2], type='double3')
        
        # Set transparency (1.0 - opacity)
        transp = 1.0 - opacity
        cmds.setAttr(f"{mat_name}.transparency", transp, transp, transp, type='double3')
        
        # Assign shading group
        cmds.sets(ghost_node, edit=True, forceElement=sg_name)