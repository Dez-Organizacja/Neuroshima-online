from main.workflows.base import Workflow
from main.workflows.data import GameConfig, WorkflowName, TurnConfig
from main.workflows.providers.base import WorkflowActionProvider
from main.steps.config import InitStepConfig, RepeatStepConfig

class GameWorkflow(Workflow[WorkflowActionProvider]):
    def __init__(self, config : GameConfig):
        self.config : GameConfig = config
        super().__init__()

    def build_player_turn_step(self, faction : str):
        return InitStepConfig(
            wf_name=WorkflowName.TURN,
            wf_config=TurnConfig(faction)
        )
    
    def build_repeat_step(self):
        return RepeatStepConfig()
    
    def _build_steps(self):
        steps = [
            self.build_player_turn_step(faction)
            for faction in self.config.factions
        ]
        steps.append(self.build_repeat_step())
        return steps
