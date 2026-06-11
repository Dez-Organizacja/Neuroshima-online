from abc import ABC, abstractmethod
from main.events.data import Event, OnClickData
from main.events.effects import DiscardTokenEffect, MarkAbilityUsedEffect
from main.events.workflow import PushWorkflow, PopWorkflow

from main.steps.config import WaitingStepConfig
from main.state.contex import ActionContext

from main.tokens.base import Token
from main.tokens.data import Ability, TokenType
from main.tokens.token_factory import TokenFactory

from main.workflows.providers.base import WorkflowActionProvider
from main.workflows.base import Workflow
from main.workflows.data import(
    WorkflowName,
    WorkflowConfig, 
    ABILITY_WORKFLOW_REGISTRY, 
)
from main.workflows.step_builders import build_end_step, build_resolve_step
from main.input.data import Button

class DispatchActionWorkflow(Workflow[WorkflowActionProvider], ABC):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    @abstractmethod
    def get_active_token(ctx) -> Token:
        pass
    
    @staticmethod
    def get_workflow_for_ability(ability : Ability):
        return ABILITY_WORKFLOW_REGISTRY[ability]
    
    @staticmethod
    @abstractmethod
    def on_click_effects(ctx : ActionContext) -> OnClickData:
        pass
    
    @abstractmethod
    def dispatch_function(self, ctx : ActionContext) -> WorkflowName:
        pass

    @abstractmethod
    def resolve_function(self, ctx : ActionContext) -> list[Event]:
        pass

    def next_workflow_push_effect(self, ctx : ActionContext) -> PushWorkflow:
        return PushWorkflow(
            name=self.dispatch_function(ctx),
            config=WorkflowConfig(on_click=self.on_click_effects(ctx))
        )

    def _build_steps(self):
        return [
            build_resolve_step(self.resolve_function),
            build_end_step(),   
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

    @staticmethod
    def is_board_token(token : Token) -> bool:
        return token.type == TokenType.BOARD

    def resolve_function(self, ctx : ActionContext) -> list[Event]:
        print("HAND RESOLVE FUNCTION")
        if ctx.workflow_data.button == Button.DISCARD:
            return [
                DiscardTokenEffect(slot=ctx.workflow_data.slot),
                PopWorkflow(),
            ]
        
        else:
            return [self.next_workflow_push_effect(ctx)]

    def dispatch_function(self, ctx : ActionContext) -> WorkflowName:
        token = self.get_active_token(ctx)
        if self.is_board_token(token):
            return WorkflowName.PLACE

        ability = token.get_ability()
        if ability == Ability.NO_ABILITY:
            return WorkflowName.PLACE
        
        return self.get_workflow_for_ability(ability)


    def on_click_effects(self, ctx : ActionContext) -> OnClickData:
        result = OnClickData()
        if not self.is_board_token(self.get_active_token(ctx)):
            result.discard_slot = ctx.workflow_data.slot 
        return result
        

class BoardWorkflow(DispatchActionWorkflow):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_active_token(ctx : ActionContext):
        return ctx.board.get_token(ctx.workflow_data.unit_pos)

    @staticmethod
    def on_click_effects(ctx : ActionContext) -> OnClickData:
        return OnClickData(mark_activated_pos=ctx.workflow_data.unit_pos)
    
    def dispatch_function(self, ctx : ActionContext):
        token = self.get_active_token(ctx)
        ability = token.get_ability()
        return self.get_workflow_for_ability(ability)
    
    def resolve_function(self, ctx):
        return [self.next_workflow_push_effect(ctx)]