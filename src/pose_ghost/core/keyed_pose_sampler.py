from .sample_plan import SamplePlan
from .onion_settings import OnionSettings

class KeyedPoseSampler:
    """
    Placeholder/seam for future keyed-pose mode.
    V1 relies primarily on RelativeFrameSampler.
    """
    @staticmethod
    def generate_plan(current_frame: float, settings: OnionSettings) -> SamplePlan:
        raise NotImplementedError("Keyed pose sampling is a V2 feature.")