from enum import Enum


class EventType(str, Enum):
    SEATED = "SEATED"
    CAPACITY = "CAPACITY"