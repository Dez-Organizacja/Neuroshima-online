from main.utils.variable import Bottom
from main.actions.available.result import AvailableActionResult
from main.state.contex import ActionContext

class AvailableStructure:
    BOTTOM_KEY = "bottom"
    HAND_KEY = "hand"
    BOARD_KEY = "board"
    def __init__(self, hand, board, bottoms):
        self.hand = hand
        self.board = board
        self.bottoms = bottoms

    @classmethod
    def build(cls, ctx : ActionContext):
        hand = {
            fraction: [False for _ in range(player.hand.size)]
            for fraction, player in ctx.state.players.items()
        }
        board = {
            hex: False
            for hex in ctx.board.ALL_HEXES
        }
        bottoms = {
            bottom: False
            for bottom in Bottom
        }
        return cls(hand, board, bottoms)

    def to_dict(self):
        return {
            self.BOARD_KEY : self.board,
            self.BOTTOM_KEY : self.bottoms,
            self.HAND_KEY : self.hand
        }