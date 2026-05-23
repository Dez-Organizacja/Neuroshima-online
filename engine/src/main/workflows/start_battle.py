from main.workflows.base import Workflow
from main.state.contex import ActionContext
from main.workflows.providers.start_battle import StartBattleProvider
from main.steps.config import WaitingStepConfig, ResolveStepConfig
from main.events.data import ExecutionResult
from main.events.flow import StartBattleEvent, EndTurnEvent
from main.workflows.step_builders import build_end_step
from main.input.action_handlers import ActionHandler

class StartBattleWorkflow(Workflow[StartBattleProvider]):
    def __int__(self):
        super().__init__(action_provider=StartBattleProvider())

    def build_waiting_step(self):
        return WaitingStepConfig(
            action_handler=ActionHandler(),
            consume_action=True
        )
    
    @staticmethod
    def resolve_func(ctx : ActionContext):
        return ExecutionResult(flow_events=[
            StartBattleEvent(),
            EndTurnEvent()
        ])

    def build_steps(self):
        return [
            self.build_waiting_step(),
            build_end_step(self.resolve_func)
        ]