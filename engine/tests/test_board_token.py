import pytest

from main.tokens.board_token import BoardToken
from main.tokens.properties import Properties
from main.tokens.data import *
from main.utils.variable import *


class TestBoardToken:
    def test_properties1(self):
        prop = Properties("bloker", "moloch")

        expected = {
            "TYPE": TokenType.BOARD,
            "UNIT_COUNT": 2,
            "HP": 3,
            "ARMOR": [0],
        }

        assert prop.__dict__ == expected

    def test_properties2(self):
        prop = Properties("sztab", "borgo")

        expected = {
            "TYPE": TokenType.BOARD,
            "UNIT_COUNT": 1,
            "HP": 20,
            "ATTACKS": {
                Attack.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]]},
            "BOOSTS": {
                Boost.INITIATIVE: [0, 1, 2, 3, 4, 5]
            },
            "BOOST_TARGET": "own",
            "INITIATIVE": [0],
        }

        assert prop.__dict__ == expected

    def test_board_token_properties1(self):
        token = BoardToken({TokenKey.NAME: "bloker", TokenKey.FRACTION: "moloch", TokenKey.ROTATION: 0, TokenKey.DAMAGE: 0})

        assert token.name == "bloker"

        expected = {
            "TYPE": TokenType.BOARD,
            "UNIT_COUNT": 2,
            "HP": 3,
            "ARMOR": [0],
        }

        assert token.properties.__dict__ == expected

        assert token.get_property(TokenStats.HP) == 3

        token.set_property(TokenStats.HP, 5)
        assert token.get_property(TokenStats.HP) == 5

        assert token.has_property(TokenStats.ARMOR) == True
        assert token.has_property(TokenStats.WIRE) == False

        assert token.get_attacks(0) == {}

    def test_board_token_properties2(self):
        token = BoardToken({TokenKey.NAME: "sztab", TokenKey.FRACTION: "borgo", TokenKey.ROTATION: 0, TokenKey.DAMAGE: 0})

        assert token.name == "sztab"

        expected = {
            "TYPE": TokenType.BOARD,
            "UNIT_COUNT": 1,
            "HP": 20,
            "ATTACKS": {
                Attack.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]]},
            "BOOSTS": {
                Boost.INITIATIVE: [0, 1, 2, 3, 4, 5]
            },
            "BOOST_TARGET": "own",
            "INITIATIVE": [0],
        }

        assert token.properties.__dict__ == expected

        assert token.get_property(TokenStats.HP) == 20

        token.set_property(TokenStats.HP, 5)
        assert token.get_property(TokenStats.HP) == 5

        assert token.has_property(TokenStats.BOOSTS) == True
        assert token.has_property(TokenStats.ARMOR) == False

        assert token.get_attacks(1) == {}
        assert token.get_attacks(0) == {
            Attack.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]]
        }

        assert token.get_boosts() == {
            Boost.INITIATIVE: [0, 1, 2, 3, 4, 5]
        }