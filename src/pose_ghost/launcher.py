# src/pose_ghost/launcher.py
import maya.cmds as cmds
from pose_ghost.runtime import CompositionRoot
from pose_ghost.maya_adapters.event_bridge import MayaEventBridge
from pose_ghost.maya_adapters.object_bypass_store import ObjectBypassStore
from pose_ghost.maya_adapters.mesh_snapshot_renderer import MeshSnapshotRenderer
from pose_ghost.maya_adapters.target_scanner import TargetScanner
from pose_ghost.maya_adapters.scene_profile_store import SceneProfileStore
from pose_ghost.ui.ui_commands import UiCommandsProtocol
from pose_ghost.ui.object_list_model import ObjectListModel, TargetRowData
from pose_ghost.ui.pose_ghost_panel import PoseGhostPanel
from pose_ghost.ui.qt_compat import QT_AVAILABLE
from pose_ghost.core import OnionSettings, DisplayMode

class MayaUiCommandsAdapter(UiCommandsProtocol):
    def __init__(self, controller, bypass_store, ui_model):
        self.controller = controller
        self.bypass_store = bypass_store
        self.ui_model = ui_model
        self.current_targets = []
        
    def pick_target_root(self) -> str:
        selection = cmds.ls(selection=True, long=True)
        if selection:
            return selection[0]
        return ""

    def scan_target_root(self, path: str):
        if not cmds.objExists(path):
            return
        
        targets = TargetScanner.scan_target_root(path)
        
        rows = []
        for t in targets:
            short_name = t.split('|')[-1]
            rows.append(TargetRowData(
                object_id=t,
                display_name=short_name,
                node_path=t,
                bypassed=t in self.bypass_store._bypassed_ids,
                source_mode="original"
            ))
        self.ui_model.set_rows(rows)
        self.current_targets = targets
        self.controller.update_target_signature(f"root_{path}")

    def pick_rig_root(self) -> str:
        selection = cmds.ls(selection=True, long=True)
        if selection:
            return selection[0]
        return ""

    def scan_rig_root(self, path: str):
        pass

    def set_sampling_settings(self, settings: OnionSettings):
        current = self.controller._settings
        current.previous_count = settings.previous_count
        current.next_count = settings.next_count
        current.frame_step = settings.frame_step
        current.clamp_to_playback_range = settings.clamp_to_playback_range
        self.controller.update_settings(current)

    def set_display_mode(self, mode: DisplayMode):
        current = self.controller._settings
        current.display_mode = mode
        self.controller.update_settings(current)

    def set_appearance_settings(self, settings: OnionSettings):
        current = self.controller._settings
        current.base_opacity = settings.base_opacity
        current.opacity_falloff_enabled = settings.opacity_falloff_enabled
        current.fade_strength = settings.fade_strength
        self.controller.update_settings(current)

    def set_object_bypass(self, object_id: str, bypassed: bool):
        if bypassed:
            self.bypass_store.mark_bypassed(object_id)
        else:
            self.bypass_store.unmark_bypassed(object_id)
        
        self.ui_model.set_bypass(object_id, bypassed)
        self.controller.update_target_signature(f"bypassed_{object_id}_{bypassed}")

    def set_ghost_source_mode(self, mode: str, proxy_root=None):
        pass
        
    def enable(self):
        from pose_ghost.runtime.event_router import EnableStateChangedEvent
        self.controller.handle_event(EnableStateChangedEvent(True))

    def disable(self):
        from pose_ghost.runtime.event_router import EnableStateChangedEvent
        self.controller.handle_event(EnableStateChangedEvent(False))

    def clear_ghosts(self):
        self.controller._update_queue.enqueue({"action": "clear"})

    def force_rebuild(self):
        from pose_ghost.runtime.event_router import ForceRebuildEvent
        self.controller.handle_event(ForceRebuildEvent())

    def save_profile(self):
        SceneProfileStore.save_profile({"target_root": "saved_from_ui"})

from pose_ghost.ui.pose_ghost_panel import PoseGhostPanel
from pose_ghost.ui.qt_compat import QT_AVAILABLE

class PoseGhostApp:
    def __init__(self):
        self.root = CompositionRoot()
        self.bridge = MayaEventBridge(self.root.controller, self.root.registry)
        self.bypass_store = ObjectBypassStore()
        self.ui_model = ObjectListModel()
        
        self.ui_adapter = MayaUiCommandsAdapter(self.root.controller, self.bypass_store, self.ui_model)
        self.panel = PoseGhostPanel(self.ui_adapter)
        
        self.widget = None
        self._initialized = False

    def initialize(self):
        if self._initialized:
            return
        self.bridge.register_all()
        self._setup_idle_drain()
        self._initialized = True

    def _setup_idle_drain(self):
        import maya.cmds as cmds
        if cmds.about(batch=True):
            return
        
        # We need to drain the queue automatically in an interactive session.
        import maya.api.OpenMaya as om
        
        def _on_idle(clientData=None):
            req = self.root.queue.drain_latest()
            if req:
                with self.root.controller.internal_time_change():
                    if req["action"] == "rebuild":
                        state = req["state"]
                        targets = getattr(self.ui_adapter, 'current_targets', [])
                        active_targets = self.bypass_store.filter_targets(targets)
                        MeshSnapshotRenderer.render(state.sample_plan, active_targets)
                    elif req["action"] == "clear":
                        MeshSnapshotRenderer.cleanup()

        self._idle_cb = om.MEventMessage.addEventCallback("idle", _on_idle)
        self.root.registry.register("idle_drain", lambda cb: om.MMessage.removeCallback(self._idle_cb))

    def show(self):
        self.initialize()
        
        import maya.cmds as cmds
        if cmds.about(batch=True):
            print("[Pose Ghost] Running in batch mode. Skipping UI.")
            return

        if not QT_AVAILABLE:
            print("[Pose Ghost] Qt not available. Running in headless mode.")
            return

        # Simple show for now. Maya docking is more complex, just show as floating window.
        if not self.widget:
            self.widget = self.panel.build_ui()
            self.widget.setWindowTitle("Pose Ghost")
        
        self.widget.show()
        self.widget.raise_()

    def close(self):
        if self.widget:
            self.widget.close()

    def cleanup(self, clear_ghosts=False):
        if clear_ghosts:
            MeshSnapshotRenderer.cleanup()
        self.root.lifecycle.shutdown()
        self._initialized = False

    def unload(self, clear_ghosts=False):
        self.close()
        self.cleanup(clear_ghosts)

# Global singleton
_APP_INSTANCE = None

def get_app():
    global _APP_INSTANCE
    if _APP_INSTANCE is None:
        _APP_INSTANCE = PoseGhostApp()
    return _APP_INSTANCE

def show():
    get_app().show()

def close():
    if _APP_INSTANCE:
        _APP_INSTANCE.close()

def unload(clear_ghosts=False):
    global _APP_INSTANCE
    if _APP_INSTANCE:
        _APP_INSTANCE.unload(clear_ghosts)
        _APP_INSTANCE = None

def cleanup(clear_ghosts=False):
    if _APP_INSTANCE:
        _APP_INSTANCE.cleanup(clear_ghosts)
