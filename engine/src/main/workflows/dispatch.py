from abc import ABC, abstractmethod
from main.events.data import ActionResult
from main.events.effects import DiscardActiveTokenEffect, MarkAbilityUsedEffect

from main.steps.config import InitStepConfig, SetStepConfig
from main.state.contex import ActionContext
from main.state.user_action import HandAction, BoardAction

from main.tokens.abstract_token import Token

from main.workflows.providers.base import WorkflowActionProvider
from main.workflows.base import Workflow
from main.workflows.data import(
    WorkflowName, 
    ABILITY_WORKFLOW_REGISTRY, 
    WorkflowData,
)
from main.workflows.step_builders import build_end_step
from main.utils.variable import Bottom

class DispatchActionWorkflow(Workflow[WorkflowActionProvider], ABC):
    def __init__(self):
        super().__init__(action_provider=WorkflowActionProvider())
    
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

    @abstractmethod
    def build_set_step(self):
        pass

    def build_dispatch_step(self):
        return InitStepConfig(
            decision_func=self.dispatch_function,
            as_child=True
        )
    
    def build_steps(self):
        return [
            self.build_set_step(),
            self.build_dispatch_step(),
            build_end_step(self.resolve_function)   
        ]

class HandWorkflow(DispatchActionWorkflow):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_active_token(ctx : ActionContext):
        return ctx.player.hand.get_token(ctx.workflow_data.slot)

    @staticmethod
    def resolve_function(ctx : ActionContext) -> ActionResult:
        return ActionResult(
            effects=[DiscardActiveTokenEffect()]
        )

    def build_set_step(self):
        return SetStepConfig(
            getter=HandAction.get_slot,
            setter=WorkflowData.set_slot
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
    
    def build_set_step(self):
        return SetStepConfig(
            getter=BoardAction.get_pos,
            setter=WorkflowData.set_unit_pos
        )