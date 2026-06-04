import json

from main.utils.variable import Boost, Attack
from main.tokens.data import TokenKey, TokenType, TokenStats, TokenRelation, Ability

wlasciwosci = {
    ############## wojownicy
    "mutek": {
        TokenKey.TYPE: TokenType.BOARD,
        TokenKey.UNIT_COUNT: 6,
        TokenStats.HP: 1,
        TokenStats.ATTACKS: {
            Attack.MELEE: [[0, 1], [1, 1], [5, 1]],
        },
        TokenStats.INITIATIVE: [2]
    },
    "nozownik": {
        TokenKey.TYPE: TokenType.BOARD,
        TokenKey.UNIT_COUNT: 4,
        TokenStats.HP: 1,
        TokenStats.ATTACKS: {
            Attack.MELEE: [[4, 1], [5, 1]],
        },
        TokenStats.INITIATIVE: [3]
    },
    "sieciarz": {
        TokenKey.TYPE: TokenType.BOARD,
        TokenKey.UNIT_COUNT: 2,
        TokenStats.HP: 1,
        TokenStats.ATTACKS: {
            Attack.MELEE: [[2, 3]],
        },
        TokenStats.WIRE : [2],
        TokenStats.INITIATIVE: [1]
    },
    "supermutant": {
        TokenKey.TYPE: TokenType.BOARD,
        TokenKey.UNIT_COUNT: 1,
        TokenStats.HP: 2,
        TokenStats.ATTACKS: {
            Attack.MELEE: [[0, 2], [1, 1], [5, 1]],
        },
        TokenStats.ARMOR: [0, 1, 5],
        TokenStats.INITIATIVE: [2]
    },
    "silacz": {
        TokenKey.TYPE: TokenType.BOARD,
        TokenKey.UNIT_COUNT: 2,
        TokenStats.HP: 1,
        TokenStats.ATTACKS: {
            Attack.MELEE: [[0, 2]],
        },
        TokenStats.INITIATIVE: [2]
    },
    "zabojca": {
        TokenKey.TYPE: TokenType.BOARD,
        TokenKey.UNIT_COUNT: 2,
        TokenStats.HP: 1,
        TokenStats.ATTACKS: {
            Attack.SHOOT: [[5, 1]],
        },
        "abilitki" : ["mobilność"],
        TokenStats.INITIATIVE: [3]
    },
    ############## sztab
    "sztab": {
        TokenKey.TYPE: TokenType.BOARD,
        TokenKey.UNIT_COUNT: 1,
        TokenStats.HP: 20,
        TokenStats.ATTACKS: {
            Attack.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
        },
        TokenStats.BOOSTS: {
            Boost.INITIATIVE: [0, 1, 2, 3, 4, 5]
        },
        TokenStats.BOOST_TARGET: TokenRelation.OWN,
        TokenStats.INITIATIVE: [0]
    },

    ############## moduły
    "medyk": {
        TokenKey.TYPE: TokenType.BOARD,
        TokenKey.UNIT_COUNT: 1,
        TokenStats.HP: 1,
        TokenStats.BOOSTS: {
            Boost.HEAL: [0, 1, 5]
        },
        TokenStats.BOOST_TARGET: TokenRelation.OWN
    },
    "oficer": {
        TokenKey.TYPE: TokenType.BOARD,
        TokenKey.UNIT_COUNT: 2,
        TokenStats.HP: 1,
        TokenStats.BOOSTS: {
            Boost.MELEE: [0, 1, 5]
        },
        TokenStats.BOOST_TARGET: TokenRelation.OWN
    },
    "superoficer": {
        TokenKey.TYPE: TokenType.BOARD,
        TokenKey.UNIT_COUNT: 1,
        TokenStats.HP: 2,
        TokenStats.BOOSTS: {
            Boost.MELEE: [0, 1, 5]
        },
        TokenStats.BOOST_TARGET: TokenRelation.OWN
    },
    "zwiadowca": {
        TokenKey.TYPE: TokenType.BOARD,
        TokenKey.UNIT_COUNT: 2,
        TokenStats.HP: 1,
        TokenStats.BOOSTS: {
            Boost.INITIATIVE: [0, 1, 5]
        },
        TokenStats.BOOST_TARGET: TokenRelation.OWN
    },

    ############# natychmiastowe
    "bitwa": {
        TokenKey.ABILITY: Ability.BATTLE,
        TokenKey.TYPE: TokenType.INSTANT,
        TokenKey.UNIT_COUNT: 6,
    },
    "ruch": {
        TokenKey.ABILITY: Ability.MOVE,
        TokenKey.TYPE: TokenType.INSTANT,
        TokenKey.UNIT_COUNT: 4,
    },
    "granat": {
        TokenKey.ABILITY: Ability.GRENADE,
        TokenKey.TYPE: TokenType.INSTANT,
        TokenKey.UNIT_COUNT: 1,
    }
}
