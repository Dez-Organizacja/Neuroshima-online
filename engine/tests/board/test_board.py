import pytest

from main.board.board import Board
from main.tokens.board_token import BoardToken
from main.tokens.data import *

class TestBoard:
    def test_board1(self):
        board = Board()
        token = BoardToken("bloker", "moloch")
        board.import_board([
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, token.to_json(), None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
        ])

        assert board.get_token((2, 2)).name == "bloker"
        assert board.get_token((2, 2)).HP == 3

        assert board.get_token((2, 2)).DAMAGE == 0

        board.deal_damage((2, 2), 0, 1)
        assert board.get_token((2, 2)).DAMAGE == 1

        board.rotate_token((2, 2), 1)

        board.deal_damage((2, 2), 0, 1)
        assert board.get_token((2, 2)).DAMAGE == 2

        assert board.get_token((2, 2)).ARMOR == [1]
        assert board.get_token((2, 2)).get_attacks(0) == {}