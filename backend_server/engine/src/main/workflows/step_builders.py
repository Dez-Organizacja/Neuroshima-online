from main.steps.config import (
    ResolveStepConfig,
    WaitingStepConfig, 
    SetStepConfig
)
from main.input.data import BoardAction
from main.workflows.data import WorkflowData
from typing import TypeVar, Generic, Callable
from main.workflows.providers.base import WorkflowActionProvider
from main.state.contex import ActionContext
from main.events.data import ExecutionResult
from main.input.action_handlers import ActionHandler

resolve_func_type = Callable[[ActionContext], ExecutionResult]
def build_end_step(resolve_function : resolve_func_type | None = None):
    step = ResolveStepConfig(wf_finished=True)
    if resolve_function:
        step.resolve_func=resolve_function
    return step

P = TypeVar("P", bound=WorkflowActionProvider)

class BoardSelectionMixin(Generic[P]):
    action_provider : P

    def build_input_step(self, setter):
        return WaitingStepConfig(
            action_handler=ActionHandler(setter),
            consume_action=True
        )

    def build_source_step(self):
        return self.build_input_step(WorkflowData.set_unit_pos)

    def build_destination_step(self):
        return self.build_input_step(WorkflowData.set_destination)
    
    def build_target_step(self):
        return self.build_input_step(WorkflowData.set_target_pos)