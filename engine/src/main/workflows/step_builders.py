from main.steps.config import ResolveStepConfig
from main.actions.available.config import AvActionsConfig
from main.steps.config import WaitingStepConfig, SetStepConfig
from main.state.user_action import BoardAction
from main.workflows.data import WorkflowData

def build_end_step():
    return ResolveStepConfig(wf_finished=True)

class BoardSelectionMixin:
    def build_waiting_step(self, get_positions):
        av_actions_config = self.rules.build_av_actions_config(get_positions)
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
            get_positions=self.rules.get_sources,
            setter=WorkflowData.set_unit_pos
        )

    def build_destination_steps(self):
        return self.build_input_steps(
            get_positions=self.rules.get_destinations,
            setter=WorkflowData.set_destination
        )
    
    def build_target_steps(self):
        return self.build_input_steps(
            get_positions=self.rules.get_available_targets,
            setter=WorkflowData.set_target_pos
        )