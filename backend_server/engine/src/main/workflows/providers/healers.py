from main.workflows.providers.base import WorkflowActionProvider
from main.state.context import ActionContext
from main.input.data import Button
from main.rules.ability.heal import HealRules

class HealersProvider(WorkflowActionProvider):
    def __init__(self):
        self.rules = HealRules()
        
    def get_available_buttons(self, ctx : ActionContext) -> list[Button]:
        if ctx.workflow_instance.current_step_index == 2:
            return [Button.CANCEL, Button.YES, Button.NO]
        if ctx.workflow_data.unit_pos:
            return [Button.CANCEL]

        return []

    
    def get_available_positions(self, ctx : ActionContext) -> list[tuple[int, int]]:
        if ctx.workflow_instance.current_step_index == 2:
            return []

        if not ctx.workflow_data.unit_pos:
            return self.rules.get_sources(ctx.board, ctx.faction)
        
        if not ctx.workflow_data.target_pos:
            return self.rules.get_targets(ctx.board, ctx.workflow_data.unit_pos)
        
        return []