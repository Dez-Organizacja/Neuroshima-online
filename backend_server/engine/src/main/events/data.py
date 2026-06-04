from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar
from enum import Enum

@dataclass
class Event(ABC):
    recompute_passive: ClassVar[bool] = False

    @abstractmethod
    def apply(self, ctx):
        pass

@dataclass
class Effect(Event, ABC):
    pass

@dataclass
class FlowEvent(Event, ABC):
    pass

@dataclass
class WorkflowEvent(Event, ABC):
    pass

class TargetingType(Enum):
    FIRST_IN_LINE = "first_in_line"
    ALL_IN_LINE = "all_in_line"
    ADJACENT_DIRECTION = "adjacent_direction"

@dataclass
class TargetedAttackIntent:
    target_pos : tuple[int, int]
    power : int = 1

@dataclass
class DirectedAttackIntent:
    attaker_pos : tuple[int, int]
    direction : int
    targeting : TargetingType
    power : int = 1

AttackIntent = TargetedAttackIntent | DirectedAttackIntent