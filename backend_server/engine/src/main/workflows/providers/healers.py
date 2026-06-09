from main.workflows.providers.base import WorkflowActionProvider
from main.state.contex import ActionContext
from main.input.data import Button
from main.rules.ability.heal import HealRules

class HealersProvider(WorkflowActionProvider):
    def __init__(self):
        self.rules = HealRules()
        
    def get_available_buttons(self, ctx : ActionContext) -> list[Button]:
        if ctx.workflow_data.unit_pos:
            return [Button.CANCEL]

        return []

    
    def get_available_positions(self, ctx : ActionContext) -> list[tuple[int, int]]:

        if not ctx.workflow_data.unit_pos:
            return self.rules.get_sources(ctx, ctx.faction)
        
        if not ctx.workflow_data.target_pos:
            return self.rules.get_targets(ctx, ctx.workflow_data.unit_pos)
        
        return []