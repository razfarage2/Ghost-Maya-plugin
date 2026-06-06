from dataclasses import dataclass, field
from typing import List
from .onion_sample import OnionSample

@dataclass
class SamplePlan:
    previous_samples: List[OnionSample] = field(default_factory=list)
    next_samples: List[OnionSample] = field(default_factory=list)

    def all_samples(self) -> List[OnionSample]:
        return self.previous_samples + self.next_samples

    def is_empty(self) -> bool:
        return len(self.previous_samples) == 0 and len(self.next_samples) == 0

    def frame_signature(self) -> str:
        prev_frames = [s.frame for s in self.previous_samples]
        next_frames = [s.frame for s in self.next_samples]
        return f"prev:{prev_frames}|next:{next_frames}"