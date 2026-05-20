from abc import ABC, abstractmethod
from main.events.effects import DiscardActiveTokenEffect, MarkAbilityUsedEffect
from main.workflows.base import Workflow
from main.steps.config import InitStepConfig, ResolveStepConfig
from main.state.contex import ActionContext
from main.workflows.data import WorkflowName
from main.actions.execute.result import ActionResult
from main.workflows.data import ABILITY_WORKFLOW_REGISTRY
from main.tokens.abstract_token import Token

class DispatchActionWorkflow(Workflow, ABC):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    @abstractmethod
    def resolve_function(ctx : ActionContext) -> ActionResult:
        pass

    @staticmethod
    @abstractmethod
    def get_active_token(ctx) -> Token:
        pass
    
    @staticmethod
    def dispatch_function(ctx : ActionContext) -> WorkflowName:
        token = DispatchActionWorkflow.get_active_token(ctx)
        ability = token.get_ability()
        return ABILITY_WORKFLOW_REGISTRY[ability]

    def build_dispatch_step(self):
        return InitStepConfig(
            decision_func=self.dispatch_function,
            as_child=True
        )

    def build_end_step(self):
        return ResolveStepConfig(
            resolve_func=self.resolve_function,
            wf_finished=True
        )
    
    def build_steps(self):
        return [
            self.build_dispatch_step(),
            self.build_end_step()   
        ]

class HandWorkflow(DispatchActionWorkflow):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_active_token(ctx : ActionContext):
        return ctx.player.hand.get_token(ctx.workflow_data.slot)

    @staticmethod
    def resolve_function(ctx : ActionContext):
        return ActionResult(
            effects=[DiscardActiveTokenEffect()]
        )
    
class BoardWorkflow(DispatchActionWorkflow):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_active_token(ctx : ActionContext):
        return ctx.board.get_tile(ctx.workflow_data.unit_pos)

    @staticmethod
    def resolve_function(ctx : ActionContext):
        return ActionResult(
            effects=[MarkAbilityUsedEffect()]
        )