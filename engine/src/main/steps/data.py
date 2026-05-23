from dataclasses import dataclass, field
from enum import Enum
from main.events.data import ExecutionResult

@dataclass
class StepResult:
    execution_result    : ExecutionResult = field(default_factory=ExecutionResult) 
    advance             : bool = True
    input_consumed      : bool = False

class StepName(Enum):
    WAITING = "waiting"
    INPUT = "input"
    INIT = "init_workflow"
    RESOLVE = "resolve"
    SET = "set"
    REPEAT = "repeat"

