from abc import ABC, abstractmethod
from typing import TypeVar

from main.workflows.step_builders import BoardSelectionMixin
from main.workflows.base import Workflow
from main.workflows.providers.target import (
    TargetProvider,
    SniperProvider,
    BombProvider,
    GrenadeProvider
)
from main.workflows.data import WorkflowName, WorkflowConfig
from main.state.contex import ActionContext

from main.events.data import Event
from main.attacks.data import TargetedIntent
from main.events.effects import DestroyEffect, EnqueueAttacksEffect
from main.events.workflow import PushWorkflow
from main.events.data import Effect
from main.board.query import BoardQuery
import main.rules.predicates as pr


P = TypeVar("P", bound=TargetProvider)

class TargetWorkflow(BoardSelectionMixin, Workflow[P], ABC):
    def __init__(self, action_provider : P):
        super().__init__(action_provider)

    @staticmethod
    @abstractmethod
    def resolve_func(ctx : ActionContext) -> list[Event]:
        pass

    def resolve_attacks(
            self,
            attack_intents : list[TargetedIntent], 
            factions : list[str]
        ) -> list[Effect]:
        return [
            EnqueueAttacksEffect(attack_intents),
            PushWorkflow(
                name=WorkflowName.DAMAGE_RESOLVE, 
                config=WorkflowConfig(factions=factions)
            )
        ]

    def _build_steps(self):
        return [
            self.build_target_step(),
            self.build_resolve_step(self.resolve_func),
            self.build_end_step(),
        ]
            # build_resolve_step(self.resolve_func),
            # build_end_step()
    
class SniperWorkflow(TargetWorkflow[SniperProvider]):
    def __init__(self):
        super().__init__(SniperProvider())

    @staticmethod
    def resolve_func(ctx : ActionContext):
        return [
            EnqueueAttacksEffect(
                [TargetedIntent(target_pos=ctx.workflow_data.target_pos)]
            ),
            PushWorkflow(
                name=WorkflowName.DAMAGE_RESOLVE, 
                config=WorkflowConfig(factions=ctx.state.factions)
            )
        ]
    
class GranadeWorkflow(TargetWorkflow):
    def __init__(self):
        super().__init__(action_provider=GrenadeProvider())

    @staticmethod
    def resolve_func(ctx : ActionContext):
        return [DestroyEffect(ctx.workflow_data.target_pos)]
    
class BombWorkflow(TargetWorkflow):
    def __init__(self):
        super().__init__(action_provider=BombProvider())
    
    def resolve_func(self, ctx : ActionContext) -> list[Effect]:
        pos = ctx.workflow_data.target_pos
        # print(f"BOMB AT {pos}")
        positions = BoardQuery([
            pr.adjacent_to(pos),
            pr.NOT(pr.is_empty_at),
            pr.NOT(pr.token_predicate(lambda t : t.is_HQ))
        ]).apply(ctx.board)

        if not pr.is_empty_at(ctx.board, pos):
            if not ctx.board.get_token(pos).is_HQ:
                positions.append(pos)

        return self.resolve_attacks(
            attack_intents=[
                TargetedIntent(target_pos=pos)
                for pos in positions
            ],
            factions=ctx.state.factions
        )