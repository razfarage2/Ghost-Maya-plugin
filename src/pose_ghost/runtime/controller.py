from contextlib import contextmanager
from typing import Optional

from pose_ghost.core import OnionSettings, RelativeFrameSampler, GhostState, SamplePlan
from .update_queue import UpdateQueue
from .event_router import (
    TimeChangeEvent, KeyEditEvent, PlaybackStartedEvent,
    PlaybackStoppedEvent, SettingsChangedEvent, ForceRebuildEvent, EnableStateChangedEvent
)

class Controller:
    def __init__(self, update_queue: UpdateQueue):
        self._update_queue = update_queue
        self._settings = OnionSettings()
        self._enabled = True
        self._current_frame = 0.0
        self._is_playing = False
        self._key_dirty = False
        self._internal_time_change_active = False
        
        self._last_state: Optional[GhostState] = None
        self._target_signature = "default"  # Placeholder until target scanning is wired
        
    @contextmanager
    def internal_time_change(self):
        self._internal_time_change_active = True
        try:
            yield
        finally:
            self._internal_time_change_active = False

    def handle_event(self, event):
        if not self._enabled and not isinstance(event, EnableStateChangedEvent):
            return

        if isinstance(event, TimeChangeEvent):
            if self._internal_time_change_active:
                return
            self._current_frame = event.frame
            if not self._is_playing:
                self._evaluate_and_enqueue()

        elif isinstance(event, KeyEditEvent):
            self._key_dirty = True
            if not self._is_playing:
                self._evaluate_and_enqueue()

        elif isinstance(event, PlaybackStartedEvent):
            self._is_playing = True

        elif isinstance(event, PlaybackStoppedEvent):
            self._is_playing = False
            self._evaluate_and_enqueue()

        elif isinstance(event, SettingsChangedEvent):
            # Assume self._settings was updated externally or passed in
            if not self._is_playing:
                self._evaluate_and_enqueue()

        elif isinstance(event, ForceRebuildEvent):
            if not self._is_playing:
                self._force_enqueue()

        elif isinstance(event, EnableStateChangedEvent):
            self._enabled = event.enabled
            if self._enabled and not self._is_playing:
                self._evaluate_and_enqueue()
            elif not self._enabled:
                # Could enqueue a clear request if needed, or rely on renderer
                self._update_queue.enqueue({"action": "clear"})

    def update_settings(self, new_settings: OnionSettings):
        self._settings = new_settings
        self.handle_event(SettingsChangedEvent())

    def update_target_signature(self, signature: str):
        self._target_signature = signature
        self.handle_event(SettingsChangedEvent())

    def _evaluate_and_enqueue(self):
        plan = RelativeFrameSampler.generate_plan(self._current_frame, self._settings)
        
        rebuild_needed = False
        if self._key_dirty:
            rebuild_needed = True
            self._key_dirty = False
        elif self._last_state is None:
            rebuild_needed = True
        elif self._last_state.requires_rebuild(plan, self._settings, self._target_signature):
            rebuild_needed = True
            
        if rebuild_needed:
            self._last_state = GhostState(
                sample_plan=plan,
                settings=self._settings, # Note: Should really deepcopy if settings mutate, but dataclass is fine if we replace it.
                target_signature=self._target_signature
            )
            self._update_queue.enqueue({
                "action": "rebuild",
                "state": self._last_state
            })

    def _force_enqueue(self):
        plan = RelativeFrameSampler.generate_plan(self._current_frame, self._settings)
        self._last_state = GhostState(
            sample_plan=plan,
            settings=self._settings,
            target_signature=self._target_signature
        )
        self._key_dirty = False
        self._update_queue.enqueue({
            "action": "rebuild",
            "state": self._last_state
        })