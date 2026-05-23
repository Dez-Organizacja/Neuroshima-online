from main.workflows.base import Workflow
from main.workflows.data import GameConfig, WorkflowName, TurnConfig
from main.workflows.providers.base import WorkflowActionProvider
from main.steps.config import InitStepConfig, RepeatStepConfig

class GameWorkflow(Workflow[WorkflowActionProvider]):
    def __init__(self, config : GameConfig):
        self.config : GameWorkflow = config
        super().__init__(action_provider = WorkflowActionProvider())

    def build_player_turn_step(self, fraction : str):
        return InitStepConfig(wf_config=TurnConfig(fraction))
    
    def build_repeat_step(self):
        return RepeatStepConfig()
    
    def build_steps(self):
        steps = [
            self.build_player_turn_step(fraction)
            for fraction in self.fractions
        ]
        steps.append(self.build_repeat_step())
        return steps
