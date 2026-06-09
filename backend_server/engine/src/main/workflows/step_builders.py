from main.steps.config import (
    ResolveStepConfig,
    WaitingStepConfig,
)
from main.input.data import ActionType
from main.workflows.data import WorkflowData
from main.state.contex import ActionContext
from main.events.data import Event
from main.input.action_handlers import ActionHandler
from typing import Callable

resolve_func_type = Callable[[ActionContext], list[Event]]
def build_end_step(resolve_function : resolve_func_type | None = None):
    step = ResolveStepConfig(wf_finished=True)
    if resolve_function:
        step.resolve_func=resolve_function
    return step

def build_resolve_step(resolve_function : resolve_func_type):
    return ResolveStepConfig(resolve_function)

class BoardSelectionMixin():
    def build_input_step(self, setter):
        return WaitingStepConfig(
            action_handler=ActionHandler(setter)
        )

    def build_source_step(self):
        return self.build_input_step(WorkflowData.set_unit_pos)

    def build_destination_step(self):
        return self.build_input_step(WorkflowData.set_destination)
    
    def build_target_step(self):
        return self.build_input_step(WorkflowData.set_target_pos)
