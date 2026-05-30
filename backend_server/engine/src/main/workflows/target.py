from abc import ABC, abstractmethod
from main.events.data import ExecutionResult
from main.workflows.base import Workflow
from main.workflows.providers.target import (
    TargetProvider,
    SniperProvider,
    BombProvider,
    GrenadeProvider
)
from main.state.contex import ActionContext
from main.steps.config import ResolveStepConfig
from main.events.effects import(
    DamageEffect, 
    DamageProfile, 
    DestroyEffect
)
from main.board.board_query import BoardQuery
import main.rules.predicates as pr
from main.workflows.step_builders import BoardSelectionMixin, build_end_step
from typing import TypeVar
from main.tokens.board_token import BoardToken

P = TypeVar("P", bound=TargetProvider)

class TargetWorkflow(BoardSelectionMixin[P], Workflow[P], ABC):
    def __init__(self, action_provider : P):
        super().__init__(action_provider)

    @staticmethod
    @abstractmethod
    def resolve_func(ctx : ActionContext) -> ExecutionResult:
        pass

    def build_end_step(self):
        return ResolveStepConfig(
            resolve_func = self.resolve_func,
            wf_finished=True
        )

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
        return ExecutionResult(
            effects=[
                DamageEffect(pos = ctx.workflow_data.target_pos)
            ]
        )
    
class GranadeWorkflow(TargetWorkflow):
    def __init__(self):
        super().__init__(action_provider=GrenadeProvider())

    @staticmethod
    def resolve_func(ctx : ActionContext):
        return ExecutionResult(
            effects=[DestroyEffect(ctx.workflow_data.target_pos)]
        )
    
class BombWorkflow(TargetWorkflow):
    def __init__(self):
        super().__init__(action_provider=BombProvider())
    
    @staticmethod
    def resolve_func(ctx : ActionContext):
        pos = ctx.workflow_data.target_pos
        positions = BoardQuery([
            pr.adjacent_to(pos),
            pr.NOT(pr.is_empty_at),
            pr.NOT(pr.token_predicate(BoardToken.is_HQ))
        ]).apply(ctx)

        print(f"postitions {positions}")

        if not pr.is_empty_at(ctx, pos):
            positions.append(pos)

        return ExecutionResult(
            effects=[
                DamageEffect(pos)
                for pos in positions       
            ]
        )