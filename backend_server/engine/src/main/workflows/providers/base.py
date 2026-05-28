from main.state.contex import ActionContext
from main.view.data import StepUIState

class WorkflowActionProvider():
    def get_available_tokens(self, ctx : ActionContext):
        return []
    
    def get_available_buttons(self, ctx : ActionContext):
        return []
    
    def get_available_positions(self, ctx : ActionContext):
        return []
    
    def get_ui_state(self, ctx : ActionContext) -> StepUIState:
        return StepUIState(ctx.faction)