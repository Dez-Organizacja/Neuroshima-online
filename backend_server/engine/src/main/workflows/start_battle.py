from main.workflows.base import Workflow
from main.state.contex import ActionContext
from main.workflows.providers.start_battle import StartBattleProvider
from main.steps.config import WaitingStepConfig, ResolveStepConfig
from main.events.data import ExecutionResult
from main.events.flow import StartBattleEvent, EndTurnEvent
from main.input.action_handlers import ActionHandler

class StartBattleWorkflow(Workflow[StartBattleProvider]):
    def __init__(self):
        super().__init__(StartBattleProvider())

    def build_waiting_step(self):
        return WaitingStepConfig(
            action_handler=ActionHandler(),
            consume_action=True
        )

    def build_end_step(self):
        return ResolveStepConfig(
            resolve_func = self.resolve_func,
            wf_finished=False, #bo start battle konczy ture
        )

    @staticmethod
    def resolve_func(ctx : ActionContext):
        return ExecutionResult(
            flow_events=[StartBattleEvent()]
        )



    def _build_steps(self):
        return [
            self.build_waiting_step(),
            self.build_end_step()
        ]