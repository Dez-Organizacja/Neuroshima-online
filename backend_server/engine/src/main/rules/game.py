from main.utils.variable import *

class GameRules():
    def is_hand_full(self, hand):
        return hand.is_full()

    def is_hq_not_wired(self, ctx):
        return not ctx.board.is_wired(ctx, ctx.board.get_hq_pos(ctx.faction))

    @staticmethod
    def get_enemy(ctx, my_fraction):
        for faction in ctx.state.factions:
            if(faction != my_fraction):
                return faction