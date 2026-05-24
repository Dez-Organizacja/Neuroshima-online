from main.actions.available.data import AvailableStructure
from main.state.contex import ActionContext
from main.input.data import Bottom

class AvailableActionsBuilder:
    @staticmethod
    def build_hand(ctx : ActionContext):
        return {
            fraction: [False for _ in range(player.hand.size)]
            for fraction, player in ctx.state.players.items()
        }
    
    def build_board(ctx : ActionContext):
        return [[False] * ctx.board.length for i in range(ctx.board.width)]                

    def build_bottoms(ctx : ActionContext):
        return {
            bottom: False
            for bottom in Bottom
        }

    def build(self, ctx : ActionContext):
        return AvailableStructure(
            hand=self.build_hand(ctx),
            board=self.build_board(ctx),
            bottoms=self.build_bottoms(ctx)
        )