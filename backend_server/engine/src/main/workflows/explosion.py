from main.workflows.base import Workflow
from main.workflows.data import WorkflowConfig
from main.events.effects import ClearWorkflowDataEffect
from main.steps.config import WaitingStepConfig, ResolveStepConfig
from main.state.contex import ActionContext
from main.attacks.data import TargetedIntent
from main.events.effects import EnqueueAttacksEffect
from main.board.query import BoardQuery
from main.rules.predicates import NOT, is_empty_at, adjacent_to
from main.workflows.step_builders import build_end_step
from main.workflows.providers.expolsion import ExplasionProvider

class ExpolsionWorkflow(Workflow):
    def __init__(self, config : WorkflowConfig):
        super().__init__(action_provider=ExplasionProvider(config.pos))
        self.pos = config.pos

    def build_clean_step(self):
        def resolve_func(ctx : ActionContext):
            return [ClearWorkflowDataEffect()]
        ResolveStepConfig(resolve_func=resolve_func)

    def build_decision_step(self):
        return WaitingStepConfig()

    def resolve_explosion(self, ctx : ActionContext):
        targets = BoardQuery([
            NOT(is_empty_at),
            adjacent_to(self.pos)
        ]).apply(ctx.board)
        attacks = [
            TargetedIntent(pos)
            for pos in targets
        ]
        attacks.append(TargetedIntent(self.pos, destroy=True))
        return [EnqueueAttacksEffect(attacks)]

    def resolve_func(self, ctx : ActionContext):
        if ctx.workflow_data.decision:
            return self.resolve_explosion(ctx)
        else:
            token = ctx.board.get_token(self.pos)
            return [EnqueueAttacksEffect(token.get_attacks())]

    def _build_steps(self):
        return [
            self.build_clean_step(),
            self.build_decision_step(),
            build_end_step(self.resolve_func)
        ]