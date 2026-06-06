from .onion_settings import OnionSettings
from .display_mode import DisplayMode
from .onion_sample import OnionSample
from .sample_plan import SamplePlan
from .opacity_falloff import OpacityFalloff

class RelativeFrameSampler:
    @staticmethod
    def generate_plan(current_frame: float, settings: OnionSettings) -> SamplePlan:
        plan = SamplePlan()
        
        # Previous Samples
        if settings.display_mode in (DisplayMode.BOTH, DisplayMode.PREVIOUS):
            for i in range(1, settings.previous_count + 1):
                frame = current_frame - (i * settings.frame_step)
                
                if settings.clamp_to_playback_range:
                    if frame < settings.playback_min_frame:
                        continue
                        
                opacity = OpacityFalloff.calculate_opacity(
                    index=i,
                    base_opacity=settings.base_opacity,
                    fade_strength=settings.fade_strength,
                    enabled=settings.opacity_falloff_enabled
                )
                
                plan.previous_samples.append(
                    OnionSample(frame=frame, side="previous", index=i, opacity=opacity)
                )
                
        # Next Samples
        if settings.display_mode in (DisplayMode.BOTH, DisplayMode.NEXT):
            for i in range(1, settings.next_count + 1):
                frame = current_frame + (i * settings.frame_step)
                
                if settings.clamp_to_playback_range:
                    if frame > settings.playback_max_frame:
                        continue
                        
                opacity = OpacityFalloff.calculate_opacity(
                    index=i,
                    base_opacity=settings.base_opacity,
                    fade_strength=settings.fade_strength,
                    enabled=settings.opacity_falloff_enabled
                )
                
                plan.next_samples.append(
                    OnionSample(frame=frame, side="next", index=i, opacity=opacity)
                )
                
        return plan