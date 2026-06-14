from main.workflows.base import Workflow
from main.workflows.providers.base import WorkflowActionProvider
from main.workflows.data import WorkflowConfig, WorkflowName

class BattleWorkflow(Workflow[WorkflowActionProvider]):
    MAX_INITIATIVE : int = 7
    def __init__(self, config : WorkflowConfig):
        super().__init__()
        self.factions = config.factions
        
    def build_initiative_step(self, initiative):
        return self.build_push_workflow_step(
            name=WorkflowName.INITIATIVE,
            config=WorkflowConfig(
                initiative=initiative,
                factions=self.factions
            )
        )


    def _build_steps(self):
        initiatives = [
            self.build_initiative_step(i)
            for i in range(self.MAX_INITIATIVE, -1, -1)
        ]
        return initiatives + [
            self.build_end_game_check_step(),
            self.build_end_step()
        ]