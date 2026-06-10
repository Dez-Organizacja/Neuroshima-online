from main.workflows.base import Workflow
from main.workflows.providers.start_battle import StartBattleProvider
from main.workflows.data import WorkflowName
from main.workflows.step_builders import build_resolve_step

from main.events.data import Event
from main.events.flow import StartBattleEvent

from main.state.contex import ActionContext
from main.steps.config import WaitingStepConfig, ResolveStepConfig

class StartBattleWorkflow(Workflow[StartBattleProvider]):
    def __init__(self):
        super().__init__(StartBattleProvider())

    def build_waiting_step(self):
        return WaitingStepConfig()

    @staticmethod
    def resolve_func(ctx : ActionContext) -> list[Event]:
        return [StartBattleEvent()]

 
    def _build_steps(self):
        return [
            self.build_waiting_step(),
            build_resolve_step(self.resolve_func) #nie popujemy bo start battle wszystko czyści
        ]