from main.input.data import ActionType, Button
from typing import Callable
from main.state.context import ActionContext
from main.events.data import Event
from main.events.flow import EndTurnEvent, DeleteAbove
from main.events.effects import ClearWorkflowDataEffect, DiscardTokenEffect
from main.events.history import UndoEffect
from main.events.workflow import GoToStep, PushWorkflow
from main.workflows.data import WorkflowName, WorkflowData, WorkflowConfig
from main.input.data import(
    BoardAction, 
    UserAction, 
    RotationAction,
    HandAction,
    ButtonAction
)

button_handler = Callable[[ActionContext, ButtonAction], list[Event]]
BUTTON_DISPATCH = {}
def button_register(button : Button):
    def wrapper(func : button_handler):
        BUTTON_DISPATCH[button] = func
        return func
    return wrapper

class ButtonHandler:
    @classmethod
    def handle(cls, ctx : ActionContext, action : ButtonAction) -> list[Event]:
        handler = BUTTON_DISPATCH.get(action.name, None)
        if handler:
            return handler(ctx) or []
        
        return []

    @staticmethod
    def can_handle(ctx : ActionContext, action : UserAction) -> bool:
        return (
            action.type == ActionType.BUTTON 
            and action.name in BUTTON_DISPATCH.keys()
        )

    @staticmethod
    @button_register(Button.END_TURN)
    def handle_end_turn(ctx : ActionContext) -> list[Event]:
        if ctx.player.hand.size > 0:
            return [PushWorkflow(WorkflowName.END_TURN_CONFIRM)]
        return [EndTurnEvent()]


    @staticmethod
    @button_register(Button.CANCEL)
    def handle_cancel(ctx : ActionContext) -> list[Event]:
        # if not ctx.state.can_undo(ctx.decision_faction):
        #     if ctx.workflow_instance.name in {
        #         WorkflowName.TURN,
        #         WorkflowName.HEADQUARTER_TURN,
        #     }:
        #         return [GoToStep(ctx.workflow_instance.current_step_index)]

        #     return [
        #         DeleteAbove(name=WorkflowName.TURN),
        #         ClearWorkflowDataEffect()
        #     ]
        return [UndoEffect()]
    
    @staticmethod
    @button_register(Button.DISCARD)
    def handle_discard(ctx : ActionContext) -> list[Event]:
        return [
            DiscardTokenEffect(ctx.workflow_data.slot),
            DeleteAbove(WorkflowName.TURN)
        ]


position_setter = Callable[[WorkflowData, BoardAction], None]
class ActionHandler:
    def __init__(self, setter = None):
        self.setter : position_setter = setter or WorkflowData.set_unit_pos
        self.dispatch = {}
        self._build_dispatch()

    # def no_setter(self, workflow_data : WorkflowData, value) -> None:
    #     pass

    def _build_dispatch(self):
        self.dispatch[ActionType.BOARD] = self.handle_board
        self.dispatch[ActionType.HAND] = self.handle_hand
        self.dispatch[ActionType.ROTATE] = self.handle_rotation
        self.dispatch[ActionType.BUTTON] = self.handle_button
        
    def handle_board(self, ctx : ActionContext, action : BoardAction):
        self.setter(ctx.workflow_data, action.pos)
        ctx.state.last_clicked_hex.set_board(action.pos)

    @staticmethod
    def handle_rotation(ctx : ActionContext, action : RotationAction) -> None:
        ctx.workflow_data.rotation = action.rotation

    @staticmethod
    def handle_hand(ctx : ActionContext, action : HandAction) -> None:
        ctx.workflow_data.slot = action.slot
        ctx.state.last_clicked_hex.set_hand(action.slot)

    @staticmethod
    def handle_button(ctx : ActionContext, action : ButtonAction) -> None:
        ctx.workflow_data.button = action.name 

    def handle(self, ctx : ActionContext, action : UserAction) -> None:
        # if self.allowed_action_types is not None:
        #     is_allowed_button = action.type is ActionType.BUTTON and self.allow_buttons
        #     if not is_allowed_button and action.type not in self.allowed_action_types:
        #         raise ValueError(f"akcja {action.type} nie jest dozwolona w aktualnym kroku")
        ctx.workflow_data.type = action.type
        # print(f"HANDLING ACTION {action}")

        self.dispatch[action.type](ctx, action)
