from main.state.contex import ActionContext
from main.input.data import Bottom
from main.workflows.providers.base import WorkflowActionProvider
from main.rules.ability.movement import PushRules, MoveRules

positions = list[tuple[int, int]]

class MoveProvider(WorkflowActionProvider):
    def __init__(self):
        super().__init__()
        self.rules = MoveRules()

    def get_available_sources(self, ctx : ActionContext) -> positions:
        return self.rules.get_sources(ctx)

    def get_available_destinations(self, ctx : ActionContext) -> positions:
        return self.rules.get_destinations(ctx, ctx.workflow_data.unit_pos)
    
    def get_available_bottoms(self, ctx : ActionContext):
        idx = ctx.workflow_instance.current_step_index
        result = []
        if not ctx.workflow_data.unit_pos: # odzrucanie przed wybraniem jednostki
            result = [Bottom.DISCARD]
        if not ctx.workflow_data.destination: # cancel przed wybraniem celu
            result.append(Bottom.CANCEL)
        return result

    def get_available_positions(self, ctx):
        if not ctx.workflow_data.unit_pos:
            return self.get_available_sources
        
        return self.get_available_destinations
        


class PushProvider(WorkflowActionProvider):
    def __init__(self):
        super().__init__()
        self.rules = PushRules()
    
    def get_available_sources(self, ctx : ActionContext):
        return self.rules.get_sources(ctx)
    
    def get_available_targets(self, ctx : ActionContext):
        return self.rules.get_targets(ctx=ctx, pusher_pos=ctx.workflow_data.unit_pos)

    def get_available_destinations(self, ctx : ActionContext):
        return self.rules.get_destinations(
            ctx=ctx,
            pusher_pos=ctx.workflow_data.unit_pos,
            target_pos=ctx.workflow_data.target_pos
        )

    def get_available_bottoms(self, ctx : ActionContext):
        idx = ctx.workflow_instance.current_step_index
        result = []
        if not ctx.workflow_data.unit_pos: 
            # mozna zdiscardowac przed wybraniem swojej jednostki(zrodła)
            result = [Bottom.DISCARD]
        if not ctx.workflow_data.target_pos: 
            # mozna cancelowac przed wybraniem celu (jednostki wroga)
            result.append(Bottom.CANCEL)
        return result
    
    def get_available_positions(self, ctx):
        if not ctx.workflow_data.unit_pos:
            return self.get_available_sources
        if not ctx.workflow_data.target_pos:
            return self.get_available_targets
        return self.get_available_destinations
    
class RotateProvider(WorkflowActionProvider):
    def get_available_positions(self, ctx : ActionContext):
        return [ctx.workflow_data.unit_pos]