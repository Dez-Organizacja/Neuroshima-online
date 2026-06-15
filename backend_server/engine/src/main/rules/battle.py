from main.state.context import ActionContext
from main.utils.variable import Phase

class BattleRules:
    
    @staticmethod 
    def can_start(ctx : ActionContext):
        return ctx.state.phase != Phase.ENDGAME
    
    @staticmethod
    def should_start(ctx : ActionContext) -> bool:
        return ctx.board.is_full()