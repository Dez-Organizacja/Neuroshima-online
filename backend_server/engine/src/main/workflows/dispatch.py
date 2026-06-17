from abc import ABC, abstractmethod
from main.events.data import Event, OnClickData
from main.events.effects import DiscardTokenEffect
from main.events.workflow import PushWorkflow, PopWorkflow, SetActionHook

from main.state.context import ActionContext

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

    # @abstractmethod
    # def resolve_function(self, ctx : ActionContext) -> list[Event]:
    #     pass

    def resolve_function(self, ctx : ActionContext) -> PushWorkflow:
        print("RESOLVE FUNTION")
        on_click = self.on_click_effects(ctx)
        result = []
        if on_click is not None:
            result.append(
                SetActionHook(effects=on_click, name=ctx.workflow_instance.name)
            )
        result.append(PushWorkflow(name=self.dispatch_function(ctx)))

        return result

    # def next_workflow_push_effect(self, ctx : ActionContext) -> PushWorkflow:
    #     # print("NEXT WORKFLOW PUSH EFFECT")
    #     return PushWorkflow(name=self.dispatch_function(ctx))

    # def set_action_hook(self, ctx : ActionContext) -> SetActionHook:
    #     return SetActionHook(effects=self.on_click_effects(ctx))

    def _build_steps(self):
        return [
            self.build_resolve_step(
                self.resolve_function,
                # self.next_workflow_push_effect,
                # self.set_action_hook,
            ),
            self.build_end_step(),   
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

    # def resolve_function(self, ctx : ActionContext) -> list[Event]:
    #     # print("HAND RESOLVE FUNCTION")
    #     if ctx.workflow_data.button == Button.DISCARD:
    #         # print("REOSLVE DISCARD")
    #         return [
    #             DiscardTokenEffect(slot=ctx.workflow_data.slot),
    #             PopWorkflow(),
    #         ]
        
    #     return [self.next_workflow_push_effect(ctx)]
        

    def dispatch_function(self, ctx : ActionContext) -> WorkflowName:
        # print("DISPATCH FUNCTION")
        token = self.get_active_token(ctx)
        if self.is_board_token(token):
            return WorkflowName.PLACE

        ability = token.get_ability()
        if ability == Ability.NO_ABILITY:
            return WorkflowName.PLACE
        
        return self.get_workflow_for_ability(ability)


    def on_click_effects(self, ctx : ActionContext) -> OnClickData | None:
        print("HAND ON CLICK")
        # return OnClickData(discard_slot=ctx.workflow_data.slot)
        # result = OnClickData()
        if not self.is_board_token(self.get_active_token(ctx)):
            return OnClickData(discard_slot=ctx.workflow_data.slot) 
        return None
        

class BoardWorkflow(DispatchActionWorkflow):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_active_token(ctx : ActionContext):
        # print("get active token")
        # print(f"workflow data {ctx.workflow_data}")
        return ctx.board.get_token(ctx.workflow_data.unit_pos)

    @staticmethod
    def on_click_effects(ctx : ActionContext) -> OnClickData:
        return OnClickData(mark_activated_pos=ctx.workflow_data.unit_pos)
    
    def dispatch_function(self, ctx : ActionContext):
        token = self.get_active_token(ctx)
        ability = token.get_ability()
        return self.get_workflow_for_ability(ability)
    
    # def resolve_function(self, ctx):
    #     return [self.next_workflow_push_effect(ctx)]