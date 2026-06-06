from dataclasses import dataclass
from .display_mode import DisplayMode

@dataclass
class OnionSettings:
    previous_count: int = 3
    next_count: int = 3
    frame_step: int = 1
    clamp_to_playback_range: bool = True
    playback_min_frame: float = 0.0
    playback_max_frame: float = 100.0
    display_mode: DisplayMode = DisplayMode.BOTH
    base_opacity: float = 0.10
    opacity_falloff_enabled: bool = True
    fade_strength: float = 0.35
    sampling_mode: str = "relative_frames"

    def __post_init__(self):
        # Normalize and validate
        self.previous_count = max(0, self.previous_count)
        self.next_count = max(0, self.next_count)
        self.frame_step = max(1, self.frame_step)
        
        self.base_opacity = max(0.0, min(1.0, self.base_opacity))
        self.fade_strength = max(0.0, min(1.0, self.fade_strength))

        if not isinstance(self.display_mode, DisplayMode):
            if DisplayMode.is_valid(self.display_mode):
                self.display_mode = DisplayMode(self.display_mode)
            else:
                raise ValueError(f"Invalid display mode: {self.display_mode}")