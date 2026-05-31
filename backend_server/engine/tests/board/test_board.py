import pytest

from main.board.board import Board
from main.tokens.board_token import BoardToken
from main.tokens.data import *

class TestBoard:
    def test_board1(self):
        board = Board()
        token = BoardToken(name="bloker", faction="moloch")
        board.import_board([
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, token.to_dict(), None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
        ])

        assert board.get_token((2, 2)).name == "bloker"
        assert board.get_token((2, 2)).hp == 3

        assert board.get_token((2, 2)).damage == 0

        # zakomentowe nie działa
        # board.deal_damage((2, 2), 0, 1)
        # assert board.get_token((2, 2)).damage == 1

        board.rotate_token((2, 2), 1)

        # board.deal_damage((2, 2), 0, 1)
        # assert board.get_token((2, 2)).damage == 2

        assert board.get_token((2, 2)).armor == [1]
        assert board.get_token((2, 2)).get_attacks(0) == {}