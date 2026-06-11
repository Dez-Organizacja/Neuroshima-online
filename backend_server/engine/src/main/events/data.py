from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

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


@dataclass
class OnClickData:
    discard_slot : int | None = None
    mark_activated_pos : tuple[int, int] | None = None