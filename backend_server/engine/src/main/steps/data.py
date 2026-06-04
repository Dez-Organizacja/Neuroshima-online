from dataclasses import dataclass, field
from enum import Enum
from main.events.data import Event

@dataclass
class StepResult:
    execution_result    : list[Event] = field(default_factory=list) 
    advance             : bool = True

class StepName(Enum):
    WAITING = "waiting"
    INPUT = "input"
    INIT = "init_workflow"
    RESOLVE = "resolve"
    SET = "set"
    REPEAT = "repeat"