import pytest

from main.tokens.board_token import BoardToken
from main.tokens.data import *
from main.utils.variable import *

class TestBoardToken:
    def test_board_token1(self):
        token = BoardToken(name="bloker", fraction="moloch")

        assert token.name == "bloker"
        assert token.HP == 3

        # token.HP = 5
        # assert token.HP == 5

        assert token.ARMOR == [0]
        assert token.WIRED == False

        assert token.get_attacks(0) == {}

    def test_board_token2(self):
        token = BoardToken(name="sztab", fraction="moloch")

        assert token.name == "sztab"
        assert token.HP == 20

        # token.HP = 15
        # assert token.HP == 15

        print(token.get_boosts())

        assert token.get_boosts() == {
            Boost.SHOOT: [0, 1, 2, 3, 4, 5],
        }
        assert token.ARMOR == []
        assert token.WIRED == False

        assert token.get_attacks(1) == {}
        assert token.get_attacks(0) == {
            Attack.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]]
        }

    def test_board_token3(self):
        token = BoardToken(name="juggernaut", fraction="moloch")

        assert token.name == "juggernaut"
        assert token.HP == 2

        token.rotate(3)

        assert token.ARMOR == [3, 5, 1]
        assert token.get_attacks(1) == {
            Attack.SHOOT: [[4, 1]],
            Attack.MELEE: [[3, 2]],
        }

    def test_board_token4(self):
        token = BoardToken.from_dict({"name": "juggernaut", "fraction": "moloch", "ROTATION": 1, "DAMAGE": 3})

        assert token.name == "juggernaut"
        assert token.HP == 2

        assert token.DAMAGE == 3    

        token.rotate(2)

        assert token.ARMOR == [3, 5, 1]
        assert token.get_attacks(1) == {
            Attack.SHOOT: [[4, 1]],
            Attack.MELEE: [[3, 2]],
    }
        
    def test_save_load(self):
        token = BoardToken(name="klaun", fraction="moloch")
        data = token.to_dict()
        # print(data)
        # token : BoardToken = Serializator.from_dict_dataclass(BoardToken, data)
        # print(token.to_dict())
        token = BoardToken.from_dict(data)
        # assert False
        assert data == token.to_dict()