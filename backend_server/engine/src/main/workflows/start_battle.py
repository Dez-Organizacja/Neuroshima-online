from main.workflows.base import Workflow
from main.workflows.providers.start_battle import StartBattleProvider
from main.workflows.data import WorkflowName

from main.events.data import Event
from main.events.flow import EndTurnEvent
from main.events.workflow import PushWorkflow, PopWorkflow

from main.state.contex import ActionContext
from main.steps.config import WaitingStepConfig, ResolveStepConfig

class StartBattleWorkflow(Workflow[StartBattleProvider]):
    def __init__(self):
        super().__init__(StartBattleProvider())

    def build_waiting_step(self):
        return WaitingStepConfig()
    
    def build_end_turn_step(self) -> list[Event]:
        return ResolveStepConfig(
            resolve_func=lambda ctx : [EndTurnEvent()] 
        ) 

    @staticmethod
    def resolve_func(ctx : ActionContext) -> list[Event]:
        return [
            PopWorkflow(),
            PushWorkflow(name=WorkflowName.BATTLE)
        ]

    def build_end_step(self):
        return ResolveStepConfig(resolve_func=self.resolve_func)
        # nie ma wf finished = true bo resolve func popuje (zeby móc pushnąć BattleWorkflow)


    def _build_steps(self):
        return [
            self.build_waiting_step(),
            self.build_end_turn_step(),
            self.build_end_step()
        ]