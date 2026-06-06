class OpacityFalloff:
    @staticmethod
    def calculate_opacity(index: int, base_opacity: float, fade_strength: float, enabled: bool) -> float:
        if not enabled:
            opacity = base_opacity
        else:
            opacity = base_opacity * (fade_strength ** (index - 1))
            
        # Clamp to 0.0 - 1.0
        return max(0.0, min(1.0, opacity))