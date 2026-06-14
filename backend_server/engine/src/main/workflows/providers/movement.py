from main.state.contex import ActionContext
from main.input.data import Button
from main.workflows.providers.base import WorkflowActionProvider
from main.rules.ability.movement import PushRules, MoveRules
from main.view.data import StepUIState, UIMode
from main.rules.game import GameRules

positions = list[tuple[int, int]]

class MoveProvider(WorkflowActionProvider):
    def __init__(self):
        super().__init__()
        self.rules = MoveRules()

    def get_available_sources(self, ctx : ActionContext) -> positions:
        return self.rules.get_sources(ctx)

    def get_available_destinations(self, ctx : ActionContext) -> positions:
        return self.rules.get_destinations(ctx, ctx.workflow_data.unit_pos)
    
    def get_available_buttons(self, ctx : ActionContext):
        result = []
        if not ctx.workflow_data.unit_pos: # odzrucanie przed wybraniem jednostki
            result = [Button.DISCARD]
        if not ctx.workflow_data.destination: # cancel przed wybraniem celu
            result.append(Button.CANCEL)
        return result

    def get_available_positions(self, ctx : ActionContext) -> list[tuple[int, int]]:
        if not ctx.workflow_data.unit_pos:
            return self.get_available_sources(ctx)
        
        if not ctx.workflow_data.destination:
            return self.get_available_destinations(ctx)
    
        return []
        


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

    def get_available_buttons(self, ctx : ActionContext):
        result = []
        if not ctx.workflow_data.unit_pos: 
            # mozna zdiscardowac przed wybraniem swojej jednostki(zrodła)
            result = [Button.DISCARD]
        if not ctx.workflow_data.target_pos: 
            # mozna cancelowac przed wybraniem celu (jednostki wroga)
            result.append(Button.CANCEL)
        return result
    
    def get_available_positions(self, ctx):
        if not ctx.workflow_data.unit_pos:
            return self.get_available_sources(ctx)
        
        if not ctx.workflow_data.target_pos:
            return self.get_available_targets(ctx)
        
        if not ctx.workflow_data.destination:
            return self.get_available_destinations(ctx)
        
        return []
    
    def get_ui_state(self, ctx):
        if ctx.workflow_data.target_pos and ctx.workflow_data.destination is None:
            return StepUIState(
                faction=GameRules.get_enemy(ctx.state.factions, ctx.faction)
            )
        
        return super().get_ui_state(ctx)
    
class RotateProvider(WorkflowActionProvider):
    def get_available_positions(self, ctx : ActionContext):
        if ctx.workflow_data.unit_pos is None:
            return []
        return [ctx.workflow_data.unit_pos]
    
    def get_ui_state(self, ctx):
        return StepUIState(faction=ctx.faction, mode=UIMode.ROTATION)
