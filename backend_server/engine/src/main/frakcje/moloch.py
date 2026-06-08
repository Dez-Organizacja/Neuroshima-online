from main.frakcje.builder import token, melee, shoot, gauss
from main.frakcje.base import Faction
from main.tokens.data import BattleAbility, Boost

unit = Faction("moloch")
units = [
    unit.HQ(boost=Boost.SHOOT).build(),

    unit.board(name="bloker", unit_count=2)
    .hp(3)
    .directions_of(armor=[0])
    .build(),

    unit.board(name="cyborg", unit_count=2)
    .hp(1)
    .attacks(shoot(directions=[0]))
    .initiatives([3])
    .build(),

    unit.board(name="dzialkogaussa", unit_count=1)
    .hp(2)
    .attacks(gauss(directions=[4]))
    .initiatives([1])
    .build(),

    unit.board(name="klaun", unit_count=1)
    .hp(2)
    .attacks(melee(directions=[0, 5]))
    .initiatives([2])
    .battle_ability(BattleAbility.EXPLOSIN)
    .build(),

    unit.board(name="lowca", unit_count=2)
    .hp(1)
    .attacks(melee(directions=[0, 1, 3, 5]))
    .initiatives([3])
    .build(),

    unit.board(name="sieciarz", unit_count=1)
    .hp(1)
    .directions_of(wire=[0, 5])
    .build(),   

    unit.board(name="medyk", unit_count=2)
    .hp(1)
    .boosts(types=[Boost.HEAL], directions=[0, 2, 4])
    .build(),
]
# wlasciwosci = {
#     ############## wojownicy
#     "bloker": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 2,
#         TokenStats.HP: 3,
#         TokenStats.ARMOR: [0]
#     },
#     "hybryda": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 2,
#         TokenStats.HP: 1,
#         TokenStats.ATTACKS : {
#             Attack.SHOOT: [[0, 1]],
#         },
#         TokenStats.INITIATIVE: [3]
#     },
#     "dzialkogaussa": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 2,
#         TokenStats.ATTACKS : {
#             Attack.GAUSS: [[4, 1]],
#         },
#         TokenStats.INITIATIVE: [1]
#     },
#     "juggernaut": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 2,
#         TokenStats.ATTACKS : {
#             Attack.SHOOT : [[1, 1]],
#             Attack.MELEE: [[0, 2]],
#         },
#         TokenStats.ARMOR: [0, 2, 4],
#         TokenStats.INITIATIVE: [1]
#     },
#     "klaun": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 2,
#         TokenStats.ATTACKS : {
#             Attack.MELEE: [[0, 1], [5, 1]],
#         },
#         TokenStats.INITIATIVE: [2],
#         TokenStats.ABILITIES : {
#             AbilityType.BATTLE_ABILITY : BattleAbility.EXPLOSIN
#         }
#     },
#     "lowca": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 2,
#         TokenStats.HP: 1,
#         TokenStats.ATTACKS : {
#             Attack.MELEE: [[0, 1], [1, 1], [3, 1], [5, 1]],
#         },
#         TokenStats.INITIATIVE: [3]
#     },
#     "obronca": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 2,
#         TokenStats.ATTACKS : {
#             Attack.SHOOT: [[0, 1], [1, 1], [5, 1]],
#         },
#         TokenStats.INITIATIVE: [1]
#     },
#     "opancerzonylowca": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 2,
#         TokenStats.HP: 2,
#         TokenStats.ATTACKS : {
#             Attack.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
#         },
#         TokenStats.ARMOR: [0, 5],
#         TokenStats.INITIATIVE: [2]
#     },
#     "opancerzonywartownik": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 1,
#         TokenStats.ATTACKS : {
#             Attack.SHOOT: [[0, 1], [5, 1]],
#         },
#         TokenStats.INITIATIVE: [2]
#     },
#     "szerszen": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 1,
#         TokenStats.ATTACKS : {
#             Attack.MELEE: [[0, 2]],
#         },
#         TokenStats.INITIATIVE: [2]
#     },
#     "sieciarz": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 1,
#         TokenStats.WIRE: [0, 5]
#     },
#     "szturmowiec": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 2,
#         TokenStats.ATTACKS : {
#             Attack.SHOOT: [[0, 1]],
#         },
#         TokenStats.INITIATIVE: [1, 2]
#     },
#     "wartownik": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 1,
#         TokenStats.ARMOR: [0],
#         TokenStats.ATTACKS : {
#             Attack.SHOOT: [[1, 1], [5, 1]],
#         },
#         TokenStats.INITIATIVE: [2]
#     },
#     "sztab": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 20,
#         TokenStats.ATTACKS : {
#             Attack.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
#         },
#         TokenStats.BOOSTS: {
#             Boost.SHOOT: [0, 1, 2, 3, 4, 5],
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN,
#         TokenStats.INITIATIVE: [0],
#     },

#     ############## moduły
#     "oficer": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 1,
#         TokenStats.BOOSTS: {
#             Boost.SHOOT: [1, 3, 5],
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN
#     },
#     "zwiadowca": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 1,
#         TokenStats.BOOSTS: {
#              Boost.INITIATIVE: [0, 2, 4]
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN
#     },
#     "matka": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 1,
#         TokenStats.BOOSTS: {
#             Boost.NEW_INITIATIVE: [0]
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN
#     },
#     "medyk": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 2,
#         TokenStats.HP: 1,
#         TokenStats.BOOSTS: {
#             Boost.HEAL: [0, 2, 4]
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN
#     },
#     "mozg": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 1,
#         TokenStats.BOOSTS: {
#             Boost.SHOOT: [0, 2, 4],
#             Boost.MELEE: [0, 2, 4]
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN
#     },
#     ############# natychmiastowe
#     "bitwa": {
#         TokenStats.ABILITIES : {
#             AbilityType.ABILITY : Ability.BATTLE
#         },
#         TokenKey.TYPE : TokenType.INSTANT,
#         TokenKey.UNIT_COUNT : 4,
#     },
#     "ruch": {
#         TokenStats.ABILITIES : {
#             AbilityType.ABILITY : Ability.MOVE
#         },
#         TokenKey.TYPE : TokenType.INSTANT,
#         TokenKey.UNIT_COUNT : 1,
#     },
#     "odepchniecie": {
#         TokenStats.ABILITIES : {
#             AbilityType.ABILITY : Ability.PUSH
#         },
#         TokenKey.TYPE : TokenType.INSTANT,
#         TokenKey.UNIT_COUNT : 5,
#     },
#     "bomba": {
#         TokenStats.ABILITIES : {
#             AbilityType.ABILITY : Ability.PUSH
#         },
#         TokenKey.TYPE : TokenType.INSTANT,
#         TokenKey.UNIT_COUNT : 1,
#     }
# }
