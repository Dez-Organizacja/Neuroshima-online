from main.workflows.base import Workflow
from main.workflows.data import WorkflowName, WorkflowConfig
from main.workflows.providers.base import WorkflowActionProvider
from main.steps.config import InitStepConfig, RepeatStepConfig

class GameWorkflow(Workflow[WorkflowActionProvider]):
    def __init__(self, config : WorkflowConfig):
        self.config : WorkflowConfig = config
        super().__init__()

    def build_player_turn_step(self, faction : str, hand_limit : int = 3):
        return InitStepConfig(
            wf_name=WorkflowName.TURN,
            wf_config=WorkflowConfig(faction=faction, hand_limit=hand_limit)
        )

    def build_headquarter_turn_step(self, faction : str):
        return InitStepConfig(
            wf_name=WorkflowName.HEADQUARTER_TURN,
            wf_config=WorkflowConfig(faction=faction)
        )
    
    def build_repeat_step(self):
        return RepeatStepConfig(repeat_from_index=2 * len(self.config.factions)) 
        # *2 poniewaz sa 2 frakcje -> 2 kroki na frakcje -> 4 tura to dopiero normalna tura
        # sztab1, sztab2, tura 1 zeton, tura 2 zetony, tura 3 zetony, ...,
    
    def _build_steps(self):
        headquarter_steps = [
            self.build_headquarter_turn_step(faction)
            for faction in self.config.factions
        ]
        opening_turn_steps = [
            self.build_player_turn_step(faction, hand_limit=min(index + 1, 3))
            for index, faction in enumerate(self.config.factions)
        ]
        turn_steps = [
            self.build_player_turn_step(faction)
            for faction in self.config.factions
        ]
        steps = headquarter_steps + opening_turn_steps + turn_steps
        steps.append(self.build_repeat_step())
        return steps
