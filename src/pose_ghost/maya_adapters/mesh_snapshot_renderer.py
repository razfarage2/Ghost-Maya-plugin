import maya.cmds as cmds
from pose_ghost.core import SamplePlan
from .evaluated_snapshot_capture import EvaluatedSnapshotCapture
from .material_manager import MaterialManager
from .display_layer_manager import DisplayLayerManager

class MeshSnapshotRenderer:
    @classmethod
    def render(cls, sample_plan: SamplePlan, target_meshes: list[str]):
        """
        Renders the ghost snapshots for a given plan and list of targets.
        """
        # Save selection
        sel = cmds.ls(selection=True) or []
        
        # Suspend viewport
        cmds.refresh(suspend=True)
        try:
            # Cleanup old ghosts
            DisplayLayerManager.clear_all()
            DisplayLayerManager.setup_groups()

            if sample_plan.is_empty() or not target_meshes:
                return

            # Render Previous
            prev_grp = DisplayLayerManager.get_group("previous")
            for sample in sample_plan.previous_samples:
                if sample.opacity <= 0.001:
                    continue
                for target in target_meshes:
                    ghost_name = f"Ghost_Prev_{sample.index}_{target.split('|')[-1]}"
                    ghost = EvaluatedSnapshotCapture.capture_snapshot(target, sample.frame, ghost_name)
                    
                    if ghost:
                        cmds.parent(ghost, prev_grp)
                        DisplayLayerManager.make_non_renderable(ghost)
                        MaterialManager.assign_per_sample_material(ghost, "previous", sample.index, sample.opacity)

            # Render Next
            next_grp = DisplayLayerManager.get_group("next")
            for sample in sample_plan.next_samples:
                if sample.opacity <= 0.001:
                    continue
                for target in target_meshes:
                    ghost_name = f"Ghost_Next_{sample.index}_{target.split('|')[-1]}"
                    ghost = EvaluatedSnapshotCapture.capture_snapshot(target, sample.frame, ghost_name)
                    
                    if ghost:
                        cmds.parent(ghost, next_grp)
                        DisplayLayerManager.make_non_renderable(ghost)
                        MaterialManager.assign_per_sample_material(ghost, "next", sample.index, sample.opacity)
        finally:
            cmds.refresh(suspend=False)
            cmds.refresh(force=True)
            
            # Restore selection safely
            if sel:
                valid_sel = [n for n in sel if cmds.objExists(n)]
                if valid_sel:
                    cmds.select(valid_sel, replace=True)
                else:
                    cmds.select(clear=True)
            else:
                cmds.select(clear=True)

    @classmethod
    def cleanup(cls):
        DisplayLayerManager.clear_all()