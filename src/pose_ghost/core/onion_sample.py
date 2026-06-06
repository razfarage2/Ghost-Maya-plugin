from dataclasses import dataclass

@dataclass
class OnionSample:
    frame: float
    side: str  # "previous" or "next"
    index: int  # 1 = nearest, 2 = farther
    opacity: float