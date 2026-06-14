from main.workflows.base import WorkflowActionProvider
from main.state.contex import ActionContext
from main.input.data import Button

class DrawProvider(WorkflowActionProvider):
    def get_available_buttons(self, ctx : ActionContext):
        if ctx.workflow_instance.current_step_index == 1:
            return [Button.YES, Button.NO]
        
        return []
    
    def get_available_tokens(self, ctx : ActionContext):
        if ctx.workflow_instance.current_step_index == 3:
            return self.all_tokens(ctx)
        
        return []