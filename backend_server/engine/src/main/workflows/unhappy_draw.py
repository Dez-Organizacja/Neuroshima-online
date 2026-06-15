from main.workflows.base import Workflow
from main.workflows.providers.unhappy_draw import UnhappyDrawProvider
from main.workflows.data import WorkflowConfig
from main.steps.config import WaitingStepConfig
from main.workflows.step_builders import build_end_step
from main.events.effects import (
    DiscardHandEffect,
    DrawTokensEffect,
    MaybePushUnhappyDrawEffect,
)
from main.events.data import Event
from main.state.context import ActionContext
from main.input.data import Button


class UnhappyDrawWorkflow(Workflow[UnhappyDrawProvider]):
    def __init__(self, config: WorkflowConfig):
        self.config: WorkflowConfig = config
        super().__init__(action_provider=UnhappyDrawProvider())

    def resolve_function(self, ctx: ActionContext) -> list[Event]:
        if ctx.workflow_data.button != Button.YES:
            return []

        return [
            DiscardHandEffect(),
            DrawTokensEffect(hand_limit=ctx.player.hand.MAX_LIMIT),
            MaybePushUnhappyDrawEffect(faction=self.config.faction),
        ]

    def _build_steps(self):
        return [
            WaitingStepConfig(
                message="Do you want to use the unhappy draw rule?",
            ),
            build_end_step(self.resolve_function),
        ]
