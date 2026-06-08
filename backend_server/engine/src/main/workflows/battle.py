from main.workflows.base import Workflow
from main.workflows.providers.base import WorkflowActionProvider
from main.workflows.data import WorkflowConfig, WorkflowName
from main.steps.config import InitStepConfig
from main.workflows.step_builders import build_end_step

class BattleWorkflow(Workflow):
    MAX_INITIATIVE : int = 7
    def __init__(self, config : WorkflowConfig):
        super().__init__()
        self.factions = config.factions
        
    def build_initiative_step(self, initiative):
        return InitStepConfig(
            wf_name=WorkflowName.INITIATIVE,
            wf_config=WorkflowConfig(
                initiative=initiative,
                factions=self.factions
            )
        )
    
    def _build_steps(self):
        return [
            self.build_initiative_step(i)
            for i in range(self.MAX_INITIATIVE, -1, -1)
        ] + [build_end_step()]