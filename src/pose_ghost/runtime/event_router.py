from dataclasses import dataclass

@dataclass
class TimeChangeEvent:
    frame: float

@dataclass
class KeyEditEvent:
    pass

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

class EventRouter:
    """
    Placeholder router if a full publish/subscribe mechanism is needed.
    Currently, the controller handles events directly.
    """
    pass