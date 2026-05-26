from main.state.contex import ActionContext

class BattleRules:
    
    @staticmethod 
    def can_start(ctx : ActionContext):
        return ctx.player.hand.size != 3