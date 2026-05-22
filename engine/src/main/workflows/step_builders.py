from main.steps.config import (
    ResolveStepConfig,
    WaitingStepConfig, 
    SetStepConfig
)
from main.state.user_action import BoardAction
from main.workflows.data import WorkflowData
from typing import TypeVar, Generic, Callable
from main.workflows.providers.base import WorkflowActionProvider
from main.state.contex import ActionContext
from main.events.data import ActionResult

resolve_func_type = Callable[[ActionContext], ActionResult]
def build_end_step(resolve_function : resolve_func_type | None = None):
    return ResolveStepConfig(
        resolve_func=resolve_function,
        wf_finished=True
    )

P = TypeVar("P", bound=WorkflowActionProvider)

class BoardSelectionMixin(Generic[P]):
    action_provider : P
    def build_waiting_step(self, get_positions):
        av_actions_config = self.action_provider.build_av_actions_config(get_positions)
        return WaitingStepConfig(
            av_actions_config=av_actions_config,
            consume_action=True
        )
        
    def build_set_step(self, setter):
        return SetStepConfig(
            getter=BoardAction.get_pos,
            setter=setter
        )

    def build_input_steps(self, setter, get_positions = None):
        return [
            self.build_waiting_step(get_positions),
            self.build_set_step(setter)
        ]

    def build_source_steps(self):
        return self.build_input_steps(
            get_positions=self.action_provider.get_sources,
            setter=WorkflowData.set_unit_pos
        )

    def build_destination_steps(self):
        return self.build_input_steps(
            get_positions=self.action_provider.get_destinations,
            setter=WorkflowData.set_destination
        )
    
    def build_target_steps(self):
        return self.build_input_steps(
            get_positions=self.action_provider.get_available_targets,
            setter=WorkflowData.set_target_pos
        )