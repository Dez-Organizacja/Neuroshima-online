from main.board.board import Board, Hex

class BoardQuery():
    def __init__(self, predicates=None):
        self.predicates = predicates or []

    def matches(self, board : Board, pos) -> bool:
        # print(f"matching check of {pos}")
        return all(p(board, pos) for p in self.predicates)

    def apply(self, board : Board) -> list[Hex]:
        return [
            pos for pos in board.ALL_HEXES
            if self.matches(board, pos)
        ]