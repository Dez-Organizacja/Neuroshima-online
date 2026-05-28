from main.input.data import ActionType, Button
from typing import Callable
from main.state.contex import ActionContext
from main.events.data import ExecutionResult
from main.events.flow import EndTurnEvent, DeleteAbove
from main.events.effects import ClearWorkflowDataEffect, DiscardTokenEffect
from main.workflows.data import WorkflowName, WorkflowData
from main.input.data import(
    BoardAction, 
    UserAction, 
    RotationAction,
    HandAction,
    ButtonAction
)

button_handler = Callable[[ActionContext], ExecutionResult]
Button_DISPATCH = {}
def button_register(button : Button):
    def wrapper(func : button_handler):
        Button_DISPATCH[button] = func
        return func
    return wrapper

class ButtonHandler:
    @classmethod
    def handle(cls, ctx : ActionContext, action : ButtonAction) -> ExecutionResult:
        return cls.DISPATCH[action.name](ctx)

    @staticmethod
    @button_register(Button.END_TURN)
    def handle_end_turn(ctx : ActionContext) -> ExecutionResult:
        return ExecutionResult(flow_events=[EndTurnEvent()])


    @staticmethod
    @button_register(Button.CANCEL)
    def handle_cancel(ctx : ActionContext) -> ExecutionResult:
        return ExecutionResult(
            workflow_effects=[DeleteAbove(name=WorkflowName.TURN)],
            effects=[ClearWorkflowDataEffect()]
        )
    
    @staticmethod
    @button_register(Button.DISCARD)
    def handle_discard(ctx : ActionContext) -> ExecutionResult:
        return ExecutionResult(
            effects=[DiscardTokenEffect(ctx.workflow_data.slot)],
            workflow_effects=[DeleteAbove(WorkflowName.TURN)]
        )
    
    @staticmethod
    @button_register(Button.USE)
    def handle_use(ctx : ActionContext) -> ExecutionResult:
        return ExecutionResult()

position_setter = Callable[[WorkflowData, BoardAction], None]
class ActionHandler:
    def __init__(self, setter = None):
        self.button_handler = ButtonHandler
        self.setter : position_setter = setter or self.no_setter
        self.dispatch = {}
        self._build_dispatch()

    def no_setter(self, action : BoardAction) -> None:
        pass

    def _build_dispatch(self):
        self.dispatch[ActionType.BOARD] = self.handle_board
        self.dispatch[ActionType.HAND] = self.handle_hand
        self.dispatch[ActionType.ROTATE] = self.handle_rotation
        
    def handle_board(self, ctx : ActionContext, action : BoardAction):
        self.setter(ctx.workflow_data, action.pos)

    @staticmethod
    def handle_rotation(ctx : ActionContext, action : RotationAction) -> None:
        ctx.workflow_data.rotation = action.rotation

    @staticmethod
    def handle_hand(ctx : ActionContext, action : HandAction) -> None:
        ctx.workflow_data.slot = action.slot

    def handle(self, ctx : ActionContext, action : UserAction) -> ExecutionResult:
        if action.type == ActionType.BUTTON:
            return self.button_handler.handle(ctx, action)
        
        ctx.workflow_data.type = action.type
        self.dispatch[action.type](ctx, action)
        return ExecutionResult()