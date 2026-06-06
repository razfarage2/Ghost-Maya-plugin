import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
from pose_ghost.runtime.controller import Controller
from pose_ghost.runtime.callback_registry import CallbackRegistry
from pose_ghost.runtime.event_router import (
    TimeChangeEvent, KeyEditEvent, PlaybackStartedEvent, PlaybackStoppedEvent
)

class MayaEventBridge:
    def __init__(self, controller: Controller, registry: CallbackRegistry):
        self.controller = controller
        self.registry = registry

    def register_all(self):
        # Time change
        cb_time = om.MDGMessage.addTimeChangeCallback(self._on_time_change)
        self.registry.register("time_change", lambda cb: om.MMessage.removeCallback(cb_time))

        # Keyframe edit
        cb_anim = oma.MAnimMessage.addAnimCurveEditedCallback(self._on_key_edit)
        self.registry.register("key_edit", lambda cb: om.MMessage.removeCallback(cb_anim))

        # Playback (using standard Maya commands/events or OpenMaya)
        # Conditionals for play state:
        cb_play_start = om.MConditionMessage.addConditionCallback("playingBack", self._on_playback_state)
        self.registry.register("play_state", lambda cb: om.MMessage.removeCallback(cb_play_start))

    def _on_time_change(self, time, clientData=None):
        import maya.cmds as cmds
        frame = time.value
        self.controller.handle_event(TimeChangeEvent(frame=frame))

    def _on_key_edit(self, nodes, clientData=None):
        self.controller.handle_event(KeyEditEvent())

    def _on_playback_state(self, state: bool, clientData=None):
        if state:
            self.controller.handle_event(PlaybackStartedEvent())
        else:
            self.controller.handle_event(PlaybackStoppedEvent())
