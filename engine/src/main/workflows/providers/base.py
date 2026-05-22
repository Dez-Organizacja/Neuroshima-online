from main.state.contex import ActionContext
from main.actions.available.config import AvActionsConfig, PositionsGetter

class WorkflowActionProvider():
    def get_available_tokens(self, ctx : ActionContext):
        return {}
    
    def get_available_bottoms(self, ctx : ActionContext):
        return []
    
    def get_available_positions(self, ctx : ActionContext):
        return []

    def build_av_actions_config(self, 
            get_positions : PositionsGetter | None = None
        ):
        if get_positions is None:
            get_positions =  self.get_available_positions
        
        return AvActionsConfig(
            get_bottoms=self.get_available_bottoms,
            get_tokens=self.get_available_tokens,
            get_positions=get_positions
        )