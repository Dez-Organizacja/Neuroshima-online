import pytest

from main.board.board import Board
from main.tokens.board_token import BoardToken
from main.tokens.data import *

class TestBoard:
    def test_board1(self):
        board = Board()
        board.put_token(pos=(2, 2), name="bloker", faction="moloch")

        assert board.get_token((2, 2)).name == "bloker"
        assert board.get_token((2, 2)).config.hp == 3

        assert board.get_token((2, 2)).state.damage == 0

        board.get_token((2, 2)).set_rotation(1)
        assert board.get_token((2, 2)).get_attacks() == []