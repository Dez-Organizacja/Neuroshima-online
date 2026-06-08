import pytest

from main.tokens.board_token import BoardToken
from main.tokens.token_factory import TokenFactory
from main.tokens.data import *
from main.state.serialization import Serializator
from main.attacks.data import AttackType

class TestBoardToken:
    def test_board_token1(self):
        token = TokenFactory.create("bloker", "moloch")

        assert token.name == "bloker"
        assert token.config.hp == 3

        # token.hp = 5
        # assert token.hp == 5

        assert token.config.armor == [0]
        assert token.wired is False

        assert token.get_attacks() == []

    # def test_board_token2(self):
    #     token = BoardToken(name="sztab", faction="moloch")

    #     assert token.name == "sztab"
    #     assert token.hp == 20

    #     # token.hp = 15
    #     # assert token.hp == 15

    #     print(token.get_boosts())

    #     assert token.get_boosts() == {
    #         Boost.SHOOT: [0, 1, 2, 3, 4, 5],
    #     }
    #     assert token.armor == []
    #     assert token.wired is False

    #     assert token.get_attacks(1) == {}
    #     assert token.get_attacks(0) == {
    #         AttackType.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]]
    #     }

    # def test_board_token3(self):
    #     token = BoardToken(name="juggernaut", faction="moloch")

    #     assert token.name == "juggernaut"
    #     assert token.hp == 2

    #     token.rotate(3)

    #     assert token.armor == [3, 5, 1]
    #     assert token.get_attacks(1) == {
    #         AttackType.SHOOT: [[4, 1]],
    #         AttackType.MELEE: [[3, 2]],
    #     }

    # def test_board_token4(self):
    #     token = BoardToken.from_dict({"name": "juggernaut", "faction": "moloch", "rotation": 1, "damage": 3})

    #     assert token.name == "juggernaut"
    #     assert token.hp == 2

    #     assert token.damage == 3

    #     token.rotate(2)

    #     assert token.armor == [3, 5, 1]
    #     assert token.get_attacks(1) == {
    #         AttackType.SHOOT: [[4, 1]],
    #         AttackType.MELEE: [[3, 2]],
    #     }
        
    def test_save_load(self):
        token = TokenFactory.create("klaun", "moloch")
        data = token.to_dict()
        print(data)
        # token : BoardToken = Serializator.from_dict_dataclass(BoardToken, data)
        # print(token.to_dict())
        token = BoardToken.from_dict(data)
        # assert False
        assert data == token.to_dict()

    # def test_constructor_keeps_clever_initiative_state(self):
    #     data = {
    #         "name": "klaun",
    #         "faction": "moloch",
    #         "clever_initiative": {
    #             "initiative": [[2, True, True], [1, False, False]],
    #             "is_blocked_to_0": False,
    #             "iniciative_boosts": 0,
    #             "num_of_new": 1,
    #         },
    #     }

    #     token = BoardToken(**data)

    #     assert token.clever_initiative.export_state() == data["clever_initiative"]

    # def test_serializator_keeps_clever_initiative_state(self):
    #     data = {
    #         "name": "klaun",
    #         "faction": "moloch",
    #         "clever_initiative": {
    #             "initiative": [[2, True, True], [1, False, False]],
    #             "is_blocked_to_0": False,
    #             "iniciative_boosts": 0,
    #             "num_of_new": 1,
    #         },
    #     }

    #     token = Serializator.from_dict_dataclass(BoardToken, data)

        # assert token.to_dict()["clever_initiative"] == {
        #     "initiative": [2, 1],
        #     "is_used": [True, False],
        #     "is_basic": [True, False],
        #     "num_of_old": 1,
        # }
    #     assert token.clever_initiative.export_state() == data["clever_initiative"]

    def test_board_get_ability(self):
        token = TokenFactory.create(name="pancerzwspomagany", faction="posterunek")

        assert token.get_ability() == Ability.MOVE
