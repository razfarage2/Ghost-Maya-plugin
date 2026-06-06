# src/pose_ghost/maya_adapters/renderer_backend.py
"""
EXPERIMENTAL — RendererBackend protocol for Pose Ghost.

This defines the interface that both V1 (MeshSnapshotRenderer)
and V2 (VP2 SubSceneOverride) backends must satisfy.

V1 remains as-is. No migration is required in this spike.
This protocol exists to document the seam for future backend swapping.
"""
from typing import Protocol, runtime_checkable
from pose_ghost.core import SamplePlan, OnionSettings


@runtime_checkable
class RendererBackend(Protocol):
    """
    Abstract renderer backend for Pose Ghost ghost rendering.

    V1 Implementation: MeshSnapshotRenderer (DAG node duplication)
    V2 Implementation: VP2SubSceneOverride backend (direct VP2 draw)
    """

    def initialize(self, targets: list[str]) -> None:
        """
        Prepare the renderer for a set of target meshes.
        Called when targets change (scan, bypass toggle, etc.).
        """
        ...

    def update(self, sample_plan: SamplePlan, targets: list[str],
               settings: OnionSettings) -> None:
        """
        Full ghost update: capture mesh data at sample frames and render.
        Equivalent to V1 MeshSnapshotRenderer.render().
        """
        ...

    def apply_appearance_only(self, sample_plan: SamplePlan,
                               targets: list[str],
                               settings: OnionSettings) -> None:
        """
        Update visual appearance (color, opacity, visibility) without
        recapturing geometry. Equivalent to V1 apply_appearance_only().
        """
        ...

    def clear(self) -> None:
        """
        Remove all visible ghosts from the viewport.
        Equivalent to V1 MeshSnapshotRenderer.cleanup().
        """
        ...

    def teardown(self) -> None:
        """
        Full cleanup including any registered nodes, overrides, etc.
        Called on plugin unload or session end.
        """
        ...
