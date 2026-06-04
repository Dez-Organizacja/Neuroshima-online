import json

from main.utils.variable import Boost, Attack
from main.tokens.data import TokenKey, TokenType, TokenStats, TokenRelation, Ability

wlasciwosci = {
    ############## wojownicy
    "biegacz": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 2,
        TokenStats.HP: 1,
        TokenStats.ATTACKS : {
            Attack.SHOOT: [[5, 1]],
        },
        TokenKey.ABILITY : Ability.MOVE,
        TokenStats.INITIATIVE: [2]
    },
    "ckm": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 1,
        TokenStats.ATTACKS : {
            Attack.SHOOT: [[0, 1]],
        },
        TokenStats.INITIATIVE: [2, 1]
    },
    "komandos": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 5,
        TokenStats.HP: 1,
        TokenStats.ATTACKS : {
            Attack.SHOOT: [[2, 1]],
        },
        TokenStats.INITIATIVE: [3]
    },
    "likwidator": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 2,
        TokenStats.HP: 1,
        TokenStats.ATTACKS : {
            Attack.SHOOT: [[4, 2]],
        },
        TokenStats.INITIATIVE: [2]
    },
    "pancerzwspomagany": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 1,
        TokenStats.ATTACKS : {
            Attack.SHOOT: [[5, 1]],
            Attack.MELEE: [[0, 2]],
        },
        TokenStats.INITIATIVE: [3, 2],
        "ability": "ruch",
    },
    "silacz": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 1,
        TokenStats.ATTACKS : {
            Attack.MELEE: [[0, 2]],
        },
        TokenStats.INITIATIVE: [3]
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
        TokenStats.BOOST_TARGET: TokenRelation.OWN,
        TokenStats.INITIATIVE: [0],
    },

    ############## moduły
    "centrumrospoznania": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 1
    },
    "dywersant": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 1,
        TokenStats.BOOSTS: {
            Boost.MINUS_INITIATIVE: [0, 1, 2, 3, 4, 5],
        },
    },
    "medyk": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 2,
        TokenStats.HP: 1,
        TokenStats.BOOSTS: {
            Boost.HEAL: [0, 1, 5],
        },
        TokenStats.BOOST_TARGET: TokenRelation.OWN
    },
    "oficer": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 1,
        TokenStats.BOOSTS: {
            Boost.SHOOT: [0, 1, 2, 3, 4, 5],
        },
        TokenStats.BOOST_TARGET: TokenRelation.OWN
    },
    "skoper": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 1,
        TokenStats.BOOSTS: {
            Boost.STEAL_BOOST: [0, 1, 2, 3, 4, 5],
        },
        TokenStats.BOOST_TARGET: TokenRelation.ENEMY
    },
    "zwiadowca": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 2,
        TokenStats.HP: 1,
        TokenStats.BOOSTS: {
            Boost.INITIATIVE: [0, 2, 4],
        },
    },
    ############# natychmiastowe
    "bitwa": {
        TokenKey.ABILITY : Ability.BATTLE,
        TokenKey.TYPE : TokenType.INSTANT,
        TokenKey.UNIT_COUNT : 6,
    },
    "ruch": {
        TokenKey.ABILITY : Ability.MOVE,
        TokenKey.TYPE : TokenType.INSTANT,
        TokenKey.UNIT_COUNT : 7,
    },
    "snajper": {
        TokenKey.ABILITY : Ability.SNIPER,
        TokenKey.TYPE : TokenType.INSTANT,
        TokenKey.UNIT_COUNT : 1,
    }
}