from enum import Enum

class DisplayMode(str, Enum):
    BOTH = "both"
    PREVIOUS = "previous"
    NEXT = "next"

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in cls._value2member_map_