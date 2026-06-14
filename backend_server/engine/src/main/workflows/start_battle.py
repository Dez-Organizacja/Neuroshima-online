from main.workflows.base import Workflow
from main.workflows.providers.start_battle import StartBattleProvider

from main.events.data import Event
from main.events.flow import StartBattleEvent

from main.state.contex import ActionContext

class StartBattleWorkflow(Workflow[StartBattleProvider]):
    def __init__(self):
        super().__init__(StartBattleProvider())

    # def build_waiting_step(self):
    #     return WaitingStepConfig()

    @staticmethod
    def resolve_func(ctx : ActionContext) -> list[Event]:
        return [StartBattleEvent()]

 
    def _build_steps(self):
        return [
            self.build_input_step(),
            self.build_resolve_step(self.resolve_func),
            #nie ma end workflow step bo start battle -> end turn wywala ze stacka
        ]
            # self.build_waiting_step(),
            # build_resolve_step(self.resolve_func) 
            # #nie popujemy bo start battle wszystko czyści