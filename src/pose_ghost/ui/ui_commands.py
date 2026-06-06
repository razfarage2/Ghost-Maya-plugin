# src/pose_ghost/ui/ui_commands.py
from typing import Protocol, Optional
from pose_ghost.core import OnionSettings, DisplayMode

class UiCommandsProtocol(Protocol):
    def pick_target_root(self) -> str: ...
    def scan_target_root(self, path: str): ...
    def pick_rig_root(self) -> str: ...
    def scan_rig_root(self, path: str): ...
    
    def set_sampling_settings(self, settings: OnionSettings): ...
    def set_display_mode(self, mode: DisplayMode): ...
    def set_appearance_settings(self, settings: OnionSettings): ...
    
    def set_object_bypass(self, object_id: str, bypassed: bool): ...
    def set_ghost_source_mode(self, mode: str, proxy_root: Optional[str] = None): ...
    
    def enable(self): ...
    def disable(self): ...
    def clear_ghosts(self): ...
    def force_rebuild(self): ...
    def save_profile(self): ...

class FakeUiCommands:
    """A fake implementation for testing UI components without Maya."""
    def __init__(self):
        self.calls = []

    def _record(self, name, *args, **kwargs):
        self.calls.append({"method": name, "args": args, "kwargs": kwargs})

    def pick_target_root(self) -> str:
        self._record("pick_target_root")
        return "Fake|Root|Path"
        
    def scan_target_root(self, path: str):
        self._record("scan_target_root", path)
        
    def pick_rig_root(self) -> str:
        self._record("pick_rig_root")
        return "Fake|Rig|Path"
        
    def scan_rig_root(self, path: str):
        self._record("scan_rig_root", path)
        
    def set_sampling_settings(self, settings: OnionSettings):
        self._record("set_sampling_settings", settings)
        
    def set_display_mode(self, mode: DisplayMode):
        self._record("set_display_mode", mode)
        
    def set_appearance_settings(self, settings: OnionSettings):
        self._record("set_appearance_settings", settings)
        
    def set_object_bypass(self, object_id: str, bypassed: bool):
        self._record("set_object_bypass", object_id, bypassed)
        
    def set_ghost_source_mode(self, mode: str, proxy_root: Optional[str] = None):
        self._record("set_ghost_source_mode", mode, proxy_root)
        
    def enable(self):
        self._record("enable")
        
    def disable(self):
        self._record("disable")
        
    def clear_ghosts(self):
        self._record("clear_ghosts")
        
    def force_rebuild(self):
        self._record("force_rebuild")
        
    def save_profile(self):
        self._record("save_profile")
