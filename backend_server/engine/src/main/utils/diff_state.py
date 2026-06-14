from main.utils.diff import Diff
from main.state.game_state import GameState
from main.state.serialization import Serializator
from main.board.board import Board

class DiffState:
    KEYS = [
        "active_faction",
        "players",
        "phase",
    ]
    def __init__(self, a : GameState, b : GameState):
        # print("COMPERING STATES")
        self.compare_keys(a, b, self.KEYS)
        self.compare_workflow_instance(a, b)
        self.compare_board(a.board, b.board)

    @staticmethod
    def diff(a, b):
        Diff.compare(Serializator.auto_to_dict(a), Serializator.auto_to_dict(b))

    def compare_attr(self, attr : str, a, b):
        try:
            x = getattr(a, attr)
            y = getattr(b, attr)
        except Exception:
            raise ValueError(f"object don't have attribute named {attr}")
        
        self.diff(x, y)

    def compare_board(self, a : Board, b : Board):
        # print("COMPARE BOARDS")
        # a.print_board()
        # print("##########################")
        # b.print_board()
        tiles_a = a.get_tiles()
        tiles_b = b.get_tiles()
        assert len(tiles_a) == len(tiles_b)

        for x, y in zip(tiles_a, tiles_b):
            self.diff(x.pos, y.pos)
            self.diff(
                a.get_tile_view(x),
                b.get_tile_view(y)
            )


    def compare_workflow_instance(self, a : GameState, b : GameState):
        keys = ["name", "current_step_index"]
        x = a.workflow_stack[-1]
        y = b.workflow_stack[-1]
        self.compare_keys(x, y, keys)

    def compare_keys(self, a, b, keys : list[str]):
        for key in keys:
            # print(f"KEY {key} compared")
            self.diff(getattr(a, key), getattr(b, key))

    @classmethod
    def compare(cls, a : GameState, b : GameState):
        cls(a, b)