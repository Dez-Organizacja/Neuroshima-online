from abc import ABC, abstractmethod
from typing import TypeVar

from main.workflows.step_builders import BoardSelectionMixin, build_end_step
from main.workflows.base import Workflow
from main.workflows.providers.target import (
    TargetProvider,
    SniperProvider,
    BombProvider,
    GrenadeProvider
)
from main.state.contex import ActionContext

from main.events.data import Event
from main.attacks.data import TargetedIntent
from main.events.effects import DestroyEffect, EnqueueAttacksEffect
from main.events.flow import ResolvePendingAttacksEvent
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

    def _build_steps(self):
        return [
            self.build_target_step(),
            build_end_step(self.resolve_func)
        ]
    
class SniperWorkflow(TargetWorkflow[SniperProvider]):
    def __init__(self):
        super().__init__(SniperProvider())

    @staticmethod
    def resolve_func(ctx : ActionContext):
        return [
            EnqueueAttacksEffect(
                [TargetedIntent(target_pos=ctx.workflow_data.target_pos)]
            ),
            ResolvePendingAttacksEvent(),
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
    
    @staticmethod
    def resolve_func(ctx : ActionContext):
        pos = ctx.workflow_data.target_pos
        positions = BoardQuery([
            pr.adjacent_to(pos),
            pr.NOT(pr.is_empty_at),
            pr.NOT(pr.token_predicate(lambda t : t.is_HQ))
        ]).apply(ctx.board)

        print(f"postitions {positions}")

        if not pr.is_empty_at(ctx.board, pos):
            positions.append(pos)

        return [
            EnqueueAttacksEffect([
                TargetedIntent(target_pos=pos)
                for pos in positions
            ]),
            ResolvePendingAttacksEvent()
        ]