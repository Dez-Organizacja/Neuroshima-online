from dataclasses import dataclass
from main.workflows.data import WorkflowData
from main.actions.exeute_actions.action_result import ActionResult

@dataclass
class StepResult:
    push_workflow       : WorkflowData | None = None
    pop_workflow        : bool = False
    replace_workflow    : WorkflowData | None = None
    action_result       : ActionResult = ActionResult()
    input_consumed      : bool = False