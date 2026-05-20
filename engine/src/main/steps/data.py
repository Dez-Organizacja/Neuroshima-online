from dataclasses import dataclass
from enum import Enum
from main.actions.execute.result import ActionResult
from main.events.workflow import WorkflowEvent

@dataclass
class StepResult:
    workflow_effects    : list[WorkflowEvent]
    action_result       : ActionResult = ActionResult()
    input_consumed      : bool = False
    advance             : bool = True

class StepName(Enum):
    WAITING = "waiting"
    INPUT = "input"
    INIT = "init_workflow"
    RESOLVE = "resolve"
    SET = "set"
