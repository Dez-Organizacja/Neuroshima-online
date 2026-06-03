from main.workflows.providers.base import WorkflowActionProvider
from main.rules.battle import BattleRules
from main.state.contex import ActionContext
from main.input.data import Button

class StartBattleProvider(WorkflowActionProvider):
    def __init__(self):
        self.rules = BattleRules()

    def get_available_buttons(self, ctx : ActionContext):
        buttons = [Button.DISCARD, Button.CANCEL]
        if self.rules.can_start(ctx):
            buttons.append(Button.USE)
        return buttons