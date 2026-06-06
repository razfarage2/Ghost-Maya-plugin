import maya.cmds as cmds
from pose_ghost.core import SamplePlan
from .evaluated_snapshot_capture import EvaluatedSnapshotCapture
from .material_manager import MaterialManager
from .display_layer_manager import DisplayLayerManager
from .ghost_node_pool import GhostNodePool

class MeshSnapshotRenderer:
    @classmethod
    def render(cls, sample_plan: SamplePlan, target_meshes: list[str]):
        """
        Renders the ghost snapshots for a given plan and list of targets.
        """
        sel = cmds.ls(selection=True) or []
        cmds.refresh(suspend=True)
        try:
            # We no longer clear_all(). We just ensure groups exist.
            DisplayLayerManager.setup_groups()

            if sample_plan.is_empty() or not target_meshes:
                GhostNodePool.hide_unused(set())
                return

            active_keys = set()
            prev_grp = DisplayLayerManager.get_group("previous")
            next_grp = DisplayLayerManager.get_group("next")

            # Process Previous
            for sample in sample_plan.previous_samples:
                if sample.opacity <= 0.001:
                    continue
                for target in target_meshes:
                    key = (target, sample.frame)
                    active_keys.add(key)
                    
                    ghost = GhostNodePool.get_node(target, sample.frame)
                    if not ghost:
                        ghost_name = f"Ghost_{target.split('|')[-1]}_{int(sample.frame)}"
                        ghost = EvaluatedSnapshotCapture.capture_snapshot(target, sample.frame, ghost_name)
                        if ghost:
                            GhostNodePool.add_node(target, sample.frame, ghost)
                            DisplayLayerManager.make_non_renderable(ghost)
                    
                    if ghost:
                        parents = cmds.listRelatives(ghost, parent=True)
                        current_parent = parents[0] if parents else None
                        if current_parent != prev_grp:
                            cmds.parent(ghost, prev_grp)
                        cmds.setAttr(f"{ghost}.visibility", 1)
                        MaterialManager.assign_per_sample_material(ghost, "previous", sample.index, sample.opacity)

            # Process Next
            for sample in sample_plan.next_samples:
                if sample.opacity <= 0.001:
                    continue
                for target in target_meshes:
                    key = (target, sample.frame)
                    active_keys.add(key)
                    
                    ghost = GhostNodePool.get_node(target, sample.frame)
                    if not ghost:
                        ghost_name = f"Ghost_{target.split('|')[-1]}_{int(sample.frame)}"
                        ghost = EvaluatedSnapshotCapture.capture_snapshot(target, sample.frame, ghost_name)
                        if ghost:
                            GhostNodePool.add_node(target, sample.frame, ghost)
                            DisplayLayerManager.make_non_renderable(ghost)
                    
                    if ghost:
                        parents = cmds.listRelatives(ghost, parent=True)
                        current_parent = parents[0] if parents else None
                        if current_parent != next_grp:
                            cmds.parent(ghost, next_grp)
                        cmds.setAttr(f"{ghost}.visibility", 1)
                        MaterialManager.assign_per_sample_material(ghost, "next", sample.index, sample.opacity)

            # Hide unused
            GhostNodePool.hide_unused(active_keys)

        finally:
            cmds.refresh(suspend=False)
            cmds.refresh(force=True)
            
            if sel:
                valid_sel = [n for n in sel if cmds.objExists(n)]
                if valid_sel:
                    cmds.select(valid_sel, replace=True)
                else:
                    cmds.select(clear=True)
            else:
                cmds.select(clear=True)

    @classmethod
    def apply_appearance_only(cls, sample_plan: SamplePlan, target_meshes: list[str]):
        """
        Updates materials and visibility of existing active ghosts without recapturing geometry.
        """
        if sample_plan.is_empty() or not target_meshes:
            GhostNodePool.hide_unused(set())
            return
            
        active_keys = set()
        
        for sample in sample_plan.previous_samples:
            if sample.opacity <= 0.001:
                continue
            for target in target_meshes:
                key = (target, sample.frame)
                ghost = GhostNodePool.get_node(target, sample.frame)
                if ghost:
                    active_keys.add(key)
                    cmds.setAttr(f"{ghost}.visibility", 1)
                    MaterialManager.assign_per_sample_material(ghost, "previous", sample.index, sample.opacity)
                    
        for sample in sample_plan.next_samples:
            if sample.opacity <= 0.001:
                continue
            for target in target_meshes:
                key = (target, sample.frame)
                ghost = GhostNodePool.get_node(target, sample.frame)
                if ghost:
                    active_keys.add(key)
                    cmds.setAttr(f"{ghost}.visibility", 1)
                    MaterialManager.assign_per_sample_material(ghost, "next", sample.index, sample.opacity)
                    
        GhostNodePool.hide_unused(active_keys)

    @classmethod
    def cleanup(cls):
        GhostNodePool.clear()
        DisplayLayerManager.clear_all()