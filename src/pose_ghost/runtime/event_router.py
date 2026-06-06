from dataclasses import dataclass

@dataclass
class TimeChangeEvent:
    frame: float

@dataclass
class KeyEditEvent:
    timestamp: float = 0.0

@dataclass
class PlaybackStartedEvent:
    pass

@dataclass
class PlaybackStoppedEvent:
    pass

@dataclass
class SettingsChangedEvent:
    pass

@dataclass
class ForceRebuildEvent:
    pass

@dataclass
class EnableStateChangedEvent:
    enabled: bool

@dataclass
class HeavyRigModeEvent:
    enabled: bool

class EventRouter:
    """
    Placeholder router if a full publish/subscribe mechanism is needed.
    Currently, the controller handles events directly.
    """
    pass