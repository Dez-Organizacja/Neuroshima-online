from main.utils.variable import *

class GameRules():
    def __init__(self):
        pass
    #############################################################################
    #   bottom validation functions       
    #############################################################################
    def can_execute_use(self, ctx):
        if(ctx.ui_state != State.SELECTED_HAND):
            return False
        
        if(ctx.active_token.name != InstantType.BITWA):
            return True
        
        if(self.is_hand_full(ctx.state.player.hand)):
            return False
        
        return self.can_end_turn(ctx)
    
    def can_execute_discard(self, ctx):
        if(ctx.ui_state != State.SELECTED_HAND):
            return False
            
        return not self.is_token_hq(ctx.active_token)

   
    def can_use_bottom(self, ctx, bottom):
        if(bottom == Bottom.USE):
            return self.can_execute_use(ctx)
        
        if(bottom == Bottom.DISCARD):
            return self.can_execute_discard(ctx)
        
        if(bottom == Bottom.END_TURN):
            return self.can_end_turn(ctx)
        return True

    #############################################################################
    #   Other useful functions       
    #############################################################################
    def is_hand_full(self, hand):
        return hand.is_full()

    def is_hq_not_wired(self, ctx):
        return not ctx.board.is_wired(ctx, ctx.board.get_hq_pos(ctx.fraction))
    
    def is_token_hq(self, token):
        return token.name == BoardType.HQ

    def get_enemy(self, ctx, my_fraction):
        for fraction in ctx.state.fractions:
            if(fraction != my_fraction):
                return fraction