import json
from main.utils.variable import Boost, Attack
from main.tokens.data import TokenKey, TokenType, TokenStats, Ability

wlasciwosci = {
    ############## wojownicy
    "bloker": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 2,
        TokenStats.HP: 3,
        TokenStats.ARMOR: [0]
    },
    "hybryda": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 2,
        TokenStats.HP: 1,
        TokenStats.ATTACKS : {
            Attack.SHOOT: [[0, 1]],
        },
        TokenStats.INITIATIVE: [3]
    },
    "dzialkogaussa": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 2,
        TokenStats.ATTACKS : {
            Attack.GAUSS: [[4, 1]],
        },
        TokenStats.INITIATIVE: [1]
    },
    "juggernaut": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 2,
        TokenStats.ATTACKS : {
            Attack.SHOOT : [[1, 1]],
            Attack.MELEE: [[0, 2]],
        },
        TokenStats.ARMOR: [0, 2, 4],
        TokenStats.INITIATIVE: [1]
    },
    "klaun": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 2,
        TokenStats.ATTACKS : {
            Attack.MELEE: [[0, 1], [5, 1]],
        },
        TokenStats.INITIATIVE: [2]
    },
    "lowca": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 2,
        TokenStats.HP: 1,
        TokenStats.ATTACKS : {
            Attack.MELEE: [[0, 1], [1, 1], [3, 1], [5, 1]],
        },
        TokenStats.INITIATIVE: [3]
    },
    "obronca": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 2,
        TokenStats.ATTACKS : {
            Attack.SHOOT: [[0, 1], [1, 1], [5, 1]],
        },
        TokenStats.INITIATIVE: [1]
    },
    "opancerzonylowca": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 2,
        TokenStats.HP: 2,
        TokenStats.ATTACKS : {
            Attack.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
        },
        TokenStats.ARMOR: [0, 5],
        TokenStats.INITIATIVE: [2]
    },
    "opancerzonywartownik": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 1,
        TokenStats.ATTACKS : {
            Attack.SHOOT: [[0, 1], [5, 1]],
        },
        TokenStats.INITIATIVE: [2]
    },
    "szerszeń": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 1,
        TokenStats.ATTACKS : {
            Attack.MELEE: [[0, 2]],
        },
        TokenStats.INITIATIVE: [2]
    },
    "sieciarz": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 1,
        TokenStats.WIRE: [0, 5]
    },
    "szturmowiec": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 2,
        TokenStats.ATTACKS : {
            Attack.SHOOT: [[0, 1]],
        },
        TokenStats.INITIATIVE: [1, 2]
    },
    "wartownik": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 1,
        TokenStats.ARMOR: [0],
        TokenStats.ATTACKS : {
            Attack.SHOOT: [[1, 1], [5, 1]],
        },
        TokenStats.INITIATIVE: [2]
    },
    "sztab": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 20,
        TokenStats.ATTACKS : {
            Attack.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
        },
        TokenStats.BOOSTS: {
            Boost.SHOOT: [0, 1, 2, 3, 4, 5],
        },
        TokenStats.BOOST_TARGET: "own",
        TokenStats.INITIATIVE: [0],
    },

    ############## moduły
    "oficer": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 1,
        TokenStats.BOOSTS: {
            Boost.SHOOT: [1, 3, 5],
        },
        TokenStats.BOOST_TARGET: "own"
    },
    "zwiadowca": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 1,
        TokenStats.BOOSTS: {
             Boost.INITIATIVE: [0, 2, 4]
        },
        TokenStats.BOOST_TARGET: "own"
    },
    "matka": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 1,
        TokenStats.BOOSTS: {
            Boost.NEW_INITIATIVE: [0]
        },
        TokenStats.BOOST_TARGET: "own"
    },
    "medyk": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 2,
        TokenStats.HP: 1,
        TokenStats.BOOSTS: {
            Boost.HEAL: [0, 2, 4]
        },
        TokenStats.BOOST_TARGET: "own"
    },
    "mozg": {
        TokenKey.TYPE : TokenType.BOARD,
        TokenKey.UNIT_COUNT : 1,
        TokenStats.HP: 1,
        TokenStats.BOOSTS: {
            Boost.SHOOT: [0, 2, 4],
            Boost.MELEE: [0, 2, 4]
        },
        TokenStats.BOOST_TARGET: "own"
    },
    ############# natychmiastowe
    Ability.BITWA: {
        TokenKey.TYPE : TokenType.INSTANT,
        TokenKey.UNIT_COUNT : 4,
    },
    Ability.MOVE: {
        TokenKey.TYPE : TokenType.INSTANT,
        TokenKey.UNIT_COUNT : 1,
    },
    Ability.PUSH: {
        TokenKey.TYPE : TokenType.INSTANT,
        TokenKey.UNIT_COUNT : 5,
    },
    Ability.BOMB: {
        TokenKey.TYPE : TokenType.INSTANT,
        TokenKey.UNIT_COUNT : 1,
    }
}