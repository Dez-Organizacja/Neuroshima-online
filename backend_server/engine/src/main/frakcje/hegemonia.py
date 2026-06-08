# import json

# from main.utils.variable import Boost, Attack
# from main.tokens.data import TokenKey, TokenType, TokenStats, TokenRelation, Ability

# wlasciwosci = {
#     ############## wojownicy
#     "biegacz": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 3,
#         TokenStats.HP: 1,
#         TokenStats.ATTACKS : {
#             Attack.MELEE: [[5, 1]],
#         },
#         TokenKey.ABILITY : Ability.MOVE,
#         TokenStats.INITIATIVE: [2]
#     },
#     "bydlak": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 1,
#         TokenStats.ATTACKS : {
#             Attack.MELEE: [[0, 2], [1, 1], [5, 1]],
#         },
#         TokenStats.INITIATIVE: [2]
#     },
#     "ganger": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 4,
#         TokenStats.HP: 1,
#         TokenStats.ATTACKS : {
#             Attack.MELEE: [[5, 1]],
#         },
#         TokenStats.INITIATIVE: [3]
#     },
#     "gladiator": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 2,
#         TokenStats.ATTACKS : {
#             Attack.MELEE: [[0, 2], [1, 2], [5, 2]],
#         },
#         TokenStats.ARMOR: [0, 1, 5],
#         TokenStats.INITIATIVE: [1]
#     },
#     "sieciarz": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 2,
#         TokenStats.HP: 1,
#         TokenStats.WIRE : [1],
#     },
#     "straznik": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 2,
#         TokenStats.ATTACKS : {
#             Attack.MELEE: [[0, 1], [4, 1], [5, 1]],
#         },
#         TokenStats.INITIATIVE: [2]
#     },
#     "supersieciarz": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 1,
#         TokenStats.WIRE : [2, 4],
#         TokenStats.ATTACKS : {
#             Attack.MELEE: [[3, 1]]
#         },
#         TokenStats.INITIATIVE: [2]
#     },
#     "uniwersalnyzolnierz": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 3,
#         TokenStats.HP: 1,
#         TokenStats.ATTACKS : {
#             Attack.MELEE: [[5, 1]],
#             Attack.SHOOT: [[5, 1]],
#         },
#         TokenStats.INITIATIVE: [3]
#     },
#     "sztab": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 20,
#         TokenStats.ATTACKS : {
#             Attack.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
#         },
#         TokenStats.BOOSTS : {
#             Boost.MELEE: [0, 1, 2, 3, 4, 5],
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN,
#         TokenStats.INITIATIVE: [0]
#     },
#     ############## moduly
#     "boss": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 1,
#         TokenStats.BOOSTS : {
#             Boost.MELEE: [0, 5],
#             Boost.INITIATIVE: [0, 2],
#         },
#         TokenStats.INITIATIVE: [1],
#         TokenStats.BOOST_TARGET: TokenRelation.OWN
#     },
#     "kwatermistrz": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 1,
#         TokenStats.BOOSTS : {
#             Boost.MELEE_TO_SHOOT: [0],
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN
#     },
#     "oficer1": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 2,
#         TokenStats.HP: 1,
#         TokenStats.BOOSTS : {
#             Boost.MELEE: [0, 5],
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN,
#     },
#     "oficer2": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 1,
#         TokenStats.BOOSTS : {
#             Boost.MELEE: [0, 1, 5],
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN,
#     },
#     "transport": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 1,
#         TokenStats.BOOSTS : {
#             Boost.MOVE_ABILITY: [0, 1, 2, 3, 4, 5]
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN
#     },
#     "zwiadowca": {
#         TokenKey.TYPE : TokenType.BOARD,
#         TokenKey.UNIT_COUNT : 1,
#         TokenStats.HP: 1,
#         TokenStats.BOOSTS : {
#             Boost.INITIATIVE: [0, 1, 5],
#         },
#         TokenStats.BOOST_TARGET: TokenRelation.OWN,
#     },
#     ############# natychmiastowe
#     "bitwa": {
#         TokenKey.ABILITY : Ability.BATTLE,
#         TokenKey.TYPE : TokenType.INSTANT,
#         TokenKey.UNIT_COUNT : 5,
#     },
#     "ruch": {
#         TokenKey.ABILITY : Ability.MOVE,
#         TokenKey.TYPE : TokenType.INSTANT,
#         TokenKey.UNIT_COUNT : 3,
#     },
#     "odepchniecie": {
#         TokenKey.ABILITY : Ability.PUSH,
#         TokenKey.TYPE : TokenType.INSTANT,
#         TokenKey.UNIT_COUNT : 2,
#     },
#     "snajper": {
#         TokenKey.ABILITY : Ability.SNIPER,
#         TokenKey.TYPE : TokenType.INSTANT,
#         TokenKey.UNIT_COUNT : 1,
#     }
# }
