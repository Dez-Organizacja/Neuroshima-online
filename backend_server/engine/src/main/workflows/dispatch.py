from abc import ABC, abstractmethod
from main.events.data import Event
from main.events.effects import DiscardTokenEffect, MarkAbilityUsedEffect

from main.steps.config import InitStepConfig
from main.state.contex import ActionContext

from main.tokens.base import Token
from main.tokens.data import Ability, TokenType
from main.tokens.token_factory import TokenFactory

from main.workflows.providers.base import WorkflowActionProvider
from main.workflows.base import Workflow
from main.workflows.data import(
    WorkflowName, 
    ABILITY_WORKFLOW_REGISTRY, 
)
from main.workflows.step_builders import build_end_step

class DispatchActionWorkflow(Workflow[WorkflowActionProvider], ABC):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    @abstractmethod
    def resolve_function(ctx : ActionContext) -> list[Event]:
        pass

    @staticmethod
    @abstractmethod
    def get_active_token(ctx) -> Token:
        pass
    
    @staticmethod
    def get_workflow_for_ability(ability : Ability):
        return ABILITY_WORKFLOW_REGISTRY[ability]

    def dispatch_function(self, ctx : ActionContext) -> WorkflowName:
        token = self.get_active_token(ctx)
        ability = token.get_ability()
        return self.get_workflow_for_ability(ability)
    
    def build_dispatch_step(self):
        return InitStepConfig(
            decision_func=self.dispatch_function,
            as_child=True
        )
    
    def _build_steps(self):
        return [
            self.build_dispatch_step(),
            build_end_step(self.resolve_function)   
        ]

class HandWorkflow(DispatchActionWorkflow):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_active_token(ctx : ActionContext) -> Token:
        # print("get active token")
        name = ctx.player.hand.get(ctx.workflow_data.slot)
        # print(f"name {name}")
        return TokenFactory.create(name, ctx.faction)

    def dispatch_function(self, ctx : ActionContext) -> WorkflowName:
        # print("dispatch function")
        # print(f"ability {self.get_active_token(ctx).get_ability()}")
        token = self.get_active_token(ctx)
        if token.type == TokenType.BOARD:
            return WorkflowName.PLACE

        ability = token.get_ability()
        # print(f"token {token}")
        # print(f"ability {ability}")
        if ability == Ability.NO_ABILITY:
            return WorkflowName.PLACE
        
        return self.get_workflow_for_ability(ability)

    @staticmethod
    def resolve_function(ctx : ActionContext) -> list[Event]:
        return [DiscardTokenEffect(ctx.workflow_data.slot)]
    
class BoardWorkflow(DispatchActionWorkflow):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_active_token(ctx : ActionContext):
        return ctx.board.get_token(ctx.workflow_data.unit_pos)

    @staticmethod
    def resolve_function(ctx : ActionContext) -> list[Event]:
        pos = ctx.workflow_data.unit_pos

        if ctx.board.get_token(pos) is None:
            pos = ctx.workflow_data.destination

        token = ctx.board.get_token(pos)
        if token is None:
            raise ValueError("nie mozna oznaczyc uzycia abilki bez jednostki na planszy")

        return [MarkAbilityUsedEffect(pos)]
