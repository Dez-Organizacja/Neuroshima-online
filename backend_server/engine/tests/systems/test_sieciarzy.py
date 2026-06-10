from main.board.board import Board
from main.systems.sieciarze import Sieciarze
from main.tokens.token_factory import TokenFactory


def place(board: Board, pos: tuple[int, int], name: str, faction: str, rotation: int):
    token = TokenFactory.create(name, faction)
    token.set_rotation(rotation)
    board.import_token(pos, token)


def compute(board: Board) -> Sieciarze:
    sieciarze = Sieciarze(board)
    sieciarze.kwestia_sieciarzy()
    return sieciarze


class TestSieciarze:
    def test_wire_connections_use_rotated_directions(self):
        board = Board()

        place(board, (2, 4), "sieciarz", "moloch", rotation=1)
        place(board, (2, 6), "sieciarz", "testowa", rotation=0)
        place(board, (1, 5), "sieciarz", "testowa", rotation=0)

        sieciarze = compute(board)

        assert sieciarze.status_sieciarzy == {
            (2, 4): 1,
            (2, 6): 2,
            (1, 5): 2,
        }
        assert board.get_token((2, 4)).wired is False
        assert board.get_token((2, 6)).wired is True
        assert board.get_token((1, 5)).wired is True

    def test_wire_can_reach_non_wire_targets(self):
        board = Board()

        place(board, (2, 4), "sieciarz", "testowa", rotation=1)
        place(board, (2, 6), "sztab", "moloch", rotation=0)

        sieciarze = compute(board)

        assert sieciarze.status_sieciarzy == {
            (2, 4): 1,
        }
        assert board.get_token((2, 4)).wired is False
        assert board.get_token((2, 6)).wired is True

    def test_large_network_matches_expected_statuses(self):
        board = Board()

        place(board, (3, 3), "sieciarz", "testowa", rotation=5)
        place(board, (2, 2), "sieciarz", "moloch", rotation=0)
        place(board, (1, 3), "dwu-sieciarz", "testowa", rotation=1)
        place(board, (2, 4), "sieciarz", "moloch", rotation=3)
        place(board, (1, 5), "sztab", "moloch", rotation=0)
        place(board, (1, 7), "sieciarz", "testowa", rotation=2)
        place(board, (2, 8), "sieciarz", "moloch", rotation=1)
        place(board, (3, 7), "sieciarz", "testowa", rotation=3)
        place(board, (4, 6), "opancerzonywartownik", "moloch", rotation=2)

        sieciarze = compute(board)

        assert sieciarze.status_sieciarzy == {
            (1, 3): 1,
            (1, 7): 1,
            (2, 2): 1,
            (2, 4): 1,
            (2, 8): 2,
            (3, 3): 1,
            (3, 7): 1,
        }

        assert board.get_token((2, 8)).wired is True
        assert board.get_token((1, 3)).wired is False
        assert board.get_token((2, 4)).wired is False
        assert board.get_token((3, 3)).wired is False

    def test(self):
        board = Board()
        place(board, (2, 4), "sztab", "borgo", rotation=1)
        place(board, (3, 3), "sieciarz", "testowa", rotation=0)

        compute(board)

        assert board.get_token((2, 4)).wired is True
        assert board.get_token((3, 3)).wired is False
