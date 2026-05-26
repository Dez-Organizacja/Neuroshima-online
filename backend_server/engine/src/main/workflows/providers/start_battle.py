from main.workflows.providers.base import WorkflowActionProvider
from main.rules.battle import BattleRules
from main.state.contex import ActionContext
from main.input.data import Bottom

class StartBattleProvider(WorkflowActionProvider):
    def __int__(self):
        self.rules = BattleRules()

    def get_available_buttons(self, ctx : ActionContext):
        buttons = [Bottom.DISCARD, Bottom.CANCEL]
        if self.rules.can_start(ctx):
            buttons.append(Bottom.USE)
        return buttons