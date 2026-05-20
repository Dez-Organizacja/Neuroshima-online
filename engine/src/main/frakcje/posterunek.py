import json

from main.utils.variable import Boost, Attack
from main.tokens.data import TokenKey, TokenType, TokenStats, Ability

wlasciwosci = {
    ############## wojownicy
    "biegacz": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 2137, # nwm ile
        TokenStats.HP: 1,
        TokenStats.ATTACKS : {
            Attack.SHOOT: [[5, 1]],
        },
        # i tu jeszcze mobilnosc
        TokenStats.INITIATIVE: [2]
    },
    "ckm": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 2137, # nwm ile
        TokenStats.HP: 1,
        TokenStats.ATTACKS : {
            Attack.SHOOT: [[0, 1]],
        },
        TokenStats.INITIATIVE: [2, 1]
    },
    "sztab": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 20,
        TokenStats.ATTACKS : {
            Attack.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
        },
        TokenStats.BOOSTS: {
            Boost.NEW_INITIATIVE: [0, 1, 2, 3, 4, 5],
        },
        TokenStats.BOOST_TARGET: "own",
        TokenStats.INITIATIVE: [0],
    },

    ############## moduły
    "skoper": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 1,
        TokenStats.BOOSTS: {
            Boost.STEAL_BOOST: [0, 1, 2, 3, 4, 5],
        },
        TokenStats.BOOST_TARGET: "enemy"
    },

    ############# natychmiastowe
    # Ability.BITWA: {
    #     TokenKey.TYPE : TokenType.INSTANT,
    #     TokenKey.UNIT_COUNT : 4,
    # },
    # Ability.MOVE: {
    #     TokenKey.TYPE : TokenType.INSTANT,
    #     TokenKey.UNIT_COUNT : 1,
    # },
    # Ability.PUSH: {
    #     TokenKey.TYPE : TokenType.INSTANT,
    #     TokenKey.UNIT_COUNT : 5,
    # },
    # Ability.BOMB: {
    #     TokenKey.TYPE : TokenType.INSTANT,
    #     TokenKey.UNIT_COUNT : 1,
    # }
}