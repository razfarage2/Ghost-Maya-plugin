import maya.cmds as cmds

class TargetScanner:
    @staticmethod
    def scan_target_root(root_path: str, exclude_pose_ghost_nodes: bool = True):
        """
        Scans from a root node down to find all valid, visible, non-intermediate mesh shapes
        and returns their transform parents.
        """
        if not cmds.objExists(root_path):
            return []

        descendants = cmds.listRelatives(root_path, allDescendents=True, fullPath=True) or []
        # Include root itself if it's a transform with a mesh shape
        descendants.append(root_path)

        shapes_found = cmds.ls(descendants, type='mesh', long=True)
        valid_transforms = set()

        for s in shapes_found:
            # Filter Pose Ghost generated nodes
            if exclude_pose_ghost_nodes and ("PoseGhost" in s or "pose_ghost" in s.lower()):
                continue

            # Filter intermediate objects
            is_intermediate = cmds.getAttr(f"{s}.intermediateObject")
            if is_intermediate:
                continue

            # Filter hidden objects
            is_visible = cmds.getAttr(f"{s}.visibility")
            if not is_visible:
                continue

            # Get transform parent
            parents = cmds.listRelatives(s, parent=True, fullPath=True)
            if parents:
                # Check parent visibility too
                parent_visible = cmds.getAttr(f"{parents[0]}.visibility")
                if parent_visible:
                    valid_transforms.add(parents[0])

        return sorted(list(valid_transforms))