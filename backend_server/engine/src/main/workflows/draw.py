from main.workflows.base import Workflow
from main.workflows.data import WorkflowConfig
from main.state.context import ActionContext
from main.events.effects import DrawTokensEffect, DiscardAllEffect, DiscardTokenEffect
from main.events.flow import TriggerEndGameSequenceEvent
from main.events.workflow import GoToStep
from main.rules.turn import TurnRules
from main.workflows.providers.draw import DrawProvider

class DrawWorkflow(Workflow[DrawProvider]):
    def __init__(self, config : WorkflowConfig):
        super().__init__(DrawProvider())
        self.hand_limit = config.hand_limit
    
    def draw_tokens(self, ctx : ActionContext):
        return [DrawTokensEffect(hand_limit=self.hand_limit)]

    @staticmethod
    def can_skip_discard_all(ctx : ActionContext):
        return not TurnRules.is_unhappy_draw(ctx.player.hand, ctx.faction)

    @staticmethod
    def resolve_discard_all(ctx : ActionContext):
        if ctx.workflow_data.decision:
            return [DiscardAllEffect(), GoToStep(index=0)]

    @staticmethod
    def resolve_discard_phase(ctx : ActionContext):
        result = [TriggerEndGameSequenceEvent()]
        if ctx.workflow_data.slot is not None:
            result.insert(0, DiscardTokenEffect(ctx.workflow_data.slot))
        return result

    def _build_steps(self):
        return [
            self.build_resolve_step(
                self.draw_tokens,
                self.clear_wf_data,
            ),
            self.build_input_step(
                can_skip=self.can_skip_discard_all,
                message="Choose whether to redraw your hand.",
            ),
            self.build_resolve_step(self.resolve_discard_all),
            self.build_input_step(
                can_skip=TurnRules.can_skip_discarding_phase,
                message="Select a token to discard.",
                snapshot=True,
            ),
            self.build_resolve_step(self.resolve_discard_phase),
            self.build_end_step(),
        ]
