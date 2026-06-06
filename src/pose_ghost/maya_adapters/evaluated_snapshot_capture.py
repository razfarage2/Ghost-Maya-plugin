import maya.cmds as cmds

class EvaluatedSnapshotCapture:
    @staticmethod
    def capture_snapshot(source_node: str, frame: float, ghost_name: str) -> str:
        """
        Captures a standalone mesh snapshot at a requested frame.
        The exact capture approach chosen:
        - Temporarily change current time to sample frame.
        - Evaluate via cmds.duplicate(rr=True).
        - Restore original time.
        - This preserves exact world-space transform and cleans history for simple meshes.
        """
        orig_time = cmds.currentTime(query=True)
        
        try:
            # Set time to sample frame
            cmds.currentTime(frame, update=True)
            
            # Force evaluation of the source node so DG updates in batch mode
            cmds.getAttr(f"{source_node}.worldMatrix[0]")
            
            # Capture using duplicate with returnRootsOnly and without history
            # For complex rigs, duplicate rr=True might still bring along some constraints or connections.
            # In a robust V1, we duplicate and parent to world if needed.
            duplicates = cmds.duplicate(source_node, returnRootsOnly=True, name=ghost_name)
            if not duplicates:
                return ""
                
            ghost = duplicates[0]
            
            # Ensure it's not connected
            # In some cases cmds.duplicate leaves incoming connections on transforms. 
            # We explicitly unlock and sever connections to be safe.
            for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']:
                cmds.setAttr(f"{ghost}.{attr}", lock=False)
                connections = cmds.listConnections(f"{ghost}.{attr}", plugs=True, source=True, destination=False)
                if connections:
                    cmds.disconnectAttr(connections[0], f"{ghost}.{attr}")

            # Parent to world if it was parented to a rig
            parents = cmds.listRelatives(ghost, parent=True)
            if parents:
                ghost = cmds.parent(ghost, world=True)[0]

            return ghost
            
        finally:
            # Restore time
            cmds.currentTime(orig_time, update=True)