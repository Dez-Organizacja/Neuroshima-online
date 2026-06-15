from main.workflows.base import Workflow
from main.workflows.providers.end_turn_confirm import EndTurnConfirmProvider
from main.steps.config import WaitingStepConfig, ResolveStepConfig
from main.events.effects import ClearWorkflowDataEffect
from main.events.flow import EndTurnEvent
from main.events.workflow import PopWorkflow
from main.events.data import Event
from main.state.context import ActionContext


class EndTurnConfirmWorkflow(Workflow[EndTurnConfirmProvider]):
    def __init__(self):
        super().__init__(action_provider=EndTurnConfirmProvider())

    def resolve_function(self, ctx: ActionContext) -> list[Event]:
        if ctx.workflow_data.decision:
            return [
                ClearWorkflowDataEffect(),
                EndTurnEvent(),
            ]

        return [
            ClearWorkflowDataEffect(),
            PopWorkflow(),
        ]

    def _build_steps(self):
        return [
            WaitingStepConfig(
                message="Do you want to end turn? You have unused tokens on your hand.",
            ),
            ResolveStepConfig(resolve_func=self.resolve_function),
        ]
