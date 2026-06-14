from main.state.contex import ActionContext
from main.utils.variable import Phase

class BattleRules:
    
    @staticmethod 
    def can_start(ctx : ActionContext):
        return ctx.state.phase != Phase.ENDGAME