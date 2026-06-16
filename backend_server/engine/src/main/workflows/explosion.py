from main.workflows.base import Workflow
from main.workflows.data import WorkflowConfig
from main.workflows.providers.expolsion import ExplasionProvider

from main.state.context import ActionContext
from main.attacks.data import TargetedIntent
from main.attacks.provider import AttackProvider

from main.events.effects import EnqueueAttacksEffect
from main.events.flow import ChangeActiveFactionEvent
from main.board.query import BoardQuery
from main.rules.predicates import NOT, is_empty_at, adjacent_to


class ExpolsionWorkflow(Workflow):
    def __init__(self, config : WorkflowConfig):
        super().__init__(action_provider=ExplasionProvider(config.pos))
        self.pos = config.pos

        # def resolve_func(ctx : ActionContext):
        # return ResolveStepConfig(resolve_func=resolve_func)

    def set_faction(self, ctx : ActionContext):
        return [ChangeActiveFactionEvent(ctx.board.get_token(self.pos).faction)]

    # def build_decision_step(self):
    #     return WaitingStepConfig()

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
        return EnqueueAttacksEffect(attacks)

    def resolve_func(self, ctx : ActionContext):
        result = []
        if ctx.workflow_data.decision:
            result.append(self.resolve_explosion(ctx))
        else:
            attacks = AttackProvider.get_attack_intents(
                unit=ctx.board.get_token(self.pos),
                pos=self.pos
            )
            result.append(EnqueueAttacksEffect(attacks))
        result.append(ChangeActiveFactionEvent())

        return result

    def _build_steps(self):
        return [
            self.build_resolve_step(
                self.clear_wf_data,
                self.set_faction,
            ),
            self.build_input_step(message="Do you want to use explosion ability?"),
            self.build_resolve_step(self.resolve_func),
            self.build_end_step()
        ]
