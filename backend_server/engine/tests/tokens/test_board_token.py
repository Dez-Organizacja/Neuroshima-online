import pytest

from main.tokens.board_token import BoardToken
from main.tokens.data import *
from main.utils.variable import *

class TestBoardToken:
    def test_board_token1(self):
        token = BoardToken(name="bloker", faction="moloch")

        assert token.name == "bloker"
        assert token.hp == 3

        # token.hp = 5
        # assert token.hp == 5

        assert token.armor == [0]
        assert token.wired is False

        assert token.get_attacks(0) == {}

    def test_board_token2(self):
        token = BoardToken(name="sztab", faction="moloch")

        assert token.name == "sztab"
        assert token.hp == 20

        # token.hp = 15
        # assert token.hp == 15

        print(token.get_boosts())

        assert token.get_boosts() == {
            Boost.SHOOT: [0, 1, 2, 3, 4, 5],
        }
        assert token.armor == []
        assert token.wired is False

        assert token.get_attacks(1) == {}
        assert token.get_attacks(0) == {
            Attack.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]]
        }

    def test_board_token3(self):
        token = BoardToken(name="juggernaut", faction="moloch")

        assert token.name == "juggernaut"
        assert token.hp == 2

        token.rotate(3)

        assert token.armor == [3, 5, 1]
        assert token.get_attacks(1) == {
            Attack.SHOOT: [[4, 1]],
            Attack.MELEE: [[3, 2]],
        }

    def test_board_token4(self):
        token = BoardToken.from_dict({"name": "juggernaut", "faction": "moloch", "rotation": 1, "damage": 3})

        assert token.name == "juggernaut"
        assert token.hp == 2

        assert token.damage == 3

        token.rotate(2)

        assert token.armor == [3, 5, 1]
        assert token.get_attacks(1) == {
            Attack.SHOOT: [[4, 1]],
            Attack.MELEE: [[3, 2]],
        }
        
    def test_save_load(self):
        token = BoardToken(name="klaun", faction="moloch")
        data = token.to_dict()
        # print(data)
        # token : BoardToken = Serializator.from_dict_dataclass(BoardToken, data)
        # print(token.to_dict())
        token = BoardToken.from_dict(data)
        # assert False
        assert data == token.to_dict()

    # def test_board_get_ability(self):
    #     token = BoardToken(name="biegacz", faction="posterunek")
    #     # print(token)
    #     print(TokenKey.ABILITY.name)
    #     assert TokenKey.ABILITY.name.isidentifier()
    #     assert hasattr(token, TokenKey.ABILITY.name) 
    #     assert token.get_ability() == Ability.MOVE
