from dataclasses import dataclass
from typing import Optional
from .sample_plan import SamplePlan
from .onion_settings import OnionSettings

@dataclass
class GhostState:
    sample_plan: SamplePlan
    settings: OnionSettings
    target_signature: str

    def requires_rebuild(self, new_plan: SamplePlan, new_settings: OnionSettings, new_target_signature: str) -> bool:
        if self.target_signature != new_target_signature:
            return True
            
        if self.sample_plan.frame_signature() != new_plan.frame_signature():
            return True
            
        if self.settings.display_mode != new_settings.display_mode:
            return True
            
        if self.settings.base_opacity != new_settings.base_opacity:
            return True
            
        if self.settings.opacity_falloff_enabled != new_settings.opacity_falloff_enabled:
            return True
            
        if self.settings.fade_strength != new_settings.fade_strength:
            return True
            
        return False