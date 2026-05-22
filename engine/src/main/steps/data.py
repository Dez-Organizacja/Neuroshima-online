from dataclasses import dataclass
from enum import Enum
from main.events.data import ExecutionResult
from main.events.workflow import WorkflowEvent

@dataclass
class StepResult:
    execution_result    : ExecutionResult
    advance             : bool = True

class StepName(Enum):
    WAITING = "waiting"
    INPUT = "input"
    INIT = "init_workflow"
    RESOLVE = "resolve"
    SET = "set"
    CHECK_END_TURN = "check_end_turn"
