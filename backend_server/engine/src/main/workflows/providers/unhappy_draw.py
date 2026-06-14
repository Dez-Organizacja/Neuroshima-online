from main.workflows.providers.base import WorkflowActionProvider
from main.state.contex import ActionContext
from main.input.data import Button
from main.view.data import StepUIState, UIMode


class UnhappyDrawProvider(WorkflowActionProvider):
    def get_available_buttons(self, ctx: ActionContext):
        return [Button.YES, Button.NO, Button.CANCEL]

    def get_ui_state(self, ctx: ActionContext):
        return StepUIState(
            faction=ctx.faction,
            mode=UIMode.DECISION,
        )
