from main.frakcje.builder import token, melee, shoot, gauss
from main.frakcje.base import Faction
from main.tokens.data import BattleAbility, Boost, Ability

unit = Faction("borgo")

units = [
    unit.HQ(boost=Boost.INITIATIVE).build(),
    unit.board("mutek", unit_count=6)
    .hp(1)
    .attacks(melee(directions=[0, 1, 5]))
    .initiatives([2])
    .build(),

    unit.board("sieciarz", unit_count=2)
    .hp(1)
    .attacks(melee(directions=[2], power=3))
    .directions_of(wire=[2])
    .initiatives([1])
    .build(),

    unit.board("zabojca", unit_count=2)
    .hp(1)
    .attacks(shoot(directions=[5]))
    .initiatives([3])
    .ability(Ability.MOVE)
    .build(),
]
# wlasciwosci = {
#     ############## wojownicy
#     "mutek": {
#         TokenKey.TYPE: TokenType.BOARD,
#         TokenKey.UNIT_COUNT: 6,
#         TokenStats.HP: 1,
#         TokenStats.ATTACKS: {
#             Attack.MELEE: [[0, 1], [1, 1], [5, 1]],
#         },
#         TokenStats.INITIATIVE: [2]
#     },
#     "nozownik": {
#         TokenKey.TYPE: TokenType.BOARD,
#         TokenKey.UNIT_COUNT: 4,
#         TokenStats.HP: 1,
#         TokenStats.ATTACKS: {
#             Attack.MELEE: [[4, 1], [5, 1]],
#         },
#         TokenStats.INITIATIVE: [3]
#     },
#     "sieciarz": {
#         TokenKey.TYPE: TokenType.BOARD,
#         TokenKey.UNIT_COUNT: 2,
#         TokenStats.HP: 1,
#         TokenStats.ATTACKS: {
#             Attack.MELEE: [[2, 3]],
#         },
#         TokenStats.WIRE : [2],
#         TokenStats.INITIATIVE: [1]
#     },
#     "super-mutant": {
#         TokenKey.TYPE: TokenType.BOARD,
#         TokenKey.UNIT_COUNT: 1,
#         TokenStats.HP: 2,
#         TokenStats.ATTACKS: {
#             Attack.MELEE: [[0, 2], [1, 1], [5, 1]],
#         },
#         TokenStats.ARMOR: [0, 1, 5],
#         TokenStats.INITIATIVE: [2]
#     },
#     "silacz": {
#         TokenKey.TYPE: TokenType.BOARD,
#         TokenKey.UNIT_COUNT: 2,
#         TokenStats.HP: 1,
#         TokenStats.ATTACKS: {
#             Attack.MELEE: [[0, 2]],
#         },
#         TokenStats.INITIATIVE: [2]
#     },
#     "zabojca": {
#         TokenKey.TYPE: TokenType.BOARD,
#         TokenKey.UNIT_COUNT: 2,
#         TokenStats.HP: 1,
#         TokenStats.ATTACKS: {
#             Attack.SHOOT: [[5, 1]],
#         },
#         TokenStats.ABILITIES : {
#             AbilityType.ABILITY : Ability.MOVE
#         },
#         TokenStats.INITIATIVE: [3]
#     },
#     ############## sztab
#     "sztab": {
#         TokenKey.TYPE: TokenType.BOARD,
#         TokenKey.UNIT_COUNT: 1,
#         TokenStats.HP: 20,
#         TokenStats.ATTACKS: {
#             Attack.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
#         },
#         TokenStats.BOOSTS: {
#             Boost.INITIATIVE: [0, 1, 2, 3, 4, 5]
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN,
#         TokenStats.INITIATIVE: [0]
#     },

#     ############## moduły
#     "medyk": {
#         TokenKey.TYPE: TokenType.BOARD,
#         TokenKey.UNIT_COUNT: 1,
#         TokenStats.HP: 1,
#         TokenStats.BOOSTS: {
#             Boost.HEAL: [0, 1, 5]
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN
#     },
#     "oficer": {
#         TokenKey.TYPE: TokenType.BOARD,
#         TokenKey.UNIT_COUNT: 2,
#         TokenStats.HP: 1,
#         TokenStats.BOOSTS: {
#             Boost.MELEE: [0, 1, 5]
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN
#     },
#     "super-oficer": {
#         TokenKey.TYPE: TokenType.BOARD,
#         TokenKey.UNIT_COUNT: 1,
#         TokenStats.HP: 2,
#         TokenStats.BOOSTS: {
#             Boost.MELEE: [0, 1, 5]
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN
#     },
#     "zwiadowca": {
#         TokenKey.TYPE: TokenType.BOARD,
#         TokenKey.UNIT_COUNT: 2,
#         TokenStats.HP: 1,
#         TokenStats.BOOSTS: {
#             Boost.INITIATIVE: [0, 1, 5]
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN
#     },

#     ############# natychmiastowe
#     "bitwa": {
#         TokenStats.ABILITIES : {
#             AbilityType.ABILITY : Ability.BATTLE
#         },
#         TokenKey.TYPE: TokenType.INSTANT,
#         TokenKey.UNIT_COUNT: 6,
#     },
#     "ruch": {
#         TokenStats.ABILITIES : {
#             AbilityType.ABILITY : Ability.MOVE
#         },
#         TokenKey.TYPE: TokenType.INSTANT,
#         TokenKey.UNIT_COUNT: 4,
#     },
#     "granat": {
#         TokenStats.ABILITIES : {
#             AbilityType.ABILITY : Ability.GRENADE
#         },
#         TokenKey.TYPE: TokenType.INSTANT,
#         TokenKey.UNIT_COUNT: 1,
#     }
# }
