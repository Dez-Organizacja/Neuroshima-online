from main.workflows.providers.base import WorkflowActionProvider
from main.state.contex import ActionContext
from main.input.data import Button
from main.view.data import StepUIState, UIMode

class ExplasionProvider(WorkflowActionProvider):
    def __init__(self, pos : str):
        self.pos = pos

    def get_available_buttons(self, ctx : ActionContext):
        return [Button.YES, Button.NO]
    
    def get_ui_state(self, ctx : ActionContext):
        return StepUIState(
            faction=ctx.board.get_token(self.pos).faction,
            mode=UIMode.DECISION,
            message="użyć cechy eksplozji?"
        )