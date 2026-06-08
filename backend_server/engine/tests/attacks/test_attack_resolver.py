# from main.attacks.resolver import AttackResolver
# from main.attacks.targeting.data import TargetingType
# from main.attacks.data import TargetedAttackIntent, DirectedAttackIntent, AttackIntent
# from main.events.effects import DamageEffect
# from main.board.board import Board

# def get_board():
#     board = Board()
#     board.put_token(pos=(4, 2), name="dzialkogausa", faction="moloch")
#     board.put_token(pos=(3, 3), name="zabojca", faction="borgo")
#     board.put_token(pos=(2, 4), name="bloker", faction="moloch")
#     board.get_token((2, 4)).set_rotation(3)
#     board.put_token(pos=(1, 5), name="lowca", faction="moloch")
#     board.put_token(pos=(0, 6), name="mutek", faction="borgo")
#     return board

# def execute(
#         board : Board, 
#         attack : AttackIntent, 
#         expected_damage : list[DamageEffect]
#     ):
#     damage = AttackResolver.resolve(attack, board)
#     assert damage == expected_damage


# def test_targeted():
#     attack = TargetedAttackIntent(
#         target_pos=(3, 3),
#         power=2,
#     )
#     exp_damage = [DamageEffect(pos=(3, 3), power=2)]
#     execute(get_board(), attack, exp_damage)

# def test_gauss():
#     attack = DirectedAttackIntent(
#         attaker_pos=(4, 2),
#         direction=0,
#         targeting=TargetingType.ALL_IN_LINE,
#     )
#     exp_damage = [
#         DamageEffect(pos=(0, 6), power=1),
#         DamageEffect(pos=(3, 3), power=1),
#     ]
#     execute(get_board(), attack, exp_damage)

# def test_shoot():
#     attack = DirectedAttackIntent(
#         attaker_pos=(3, 3),
#         direction=0,
#         targeting=TargetingType.FIRST_IN_LINE,
#         power=2
#     )

#     exp_damage = [DamageEffect(pos=(2, 4), power=1)]
#     execute(get_board(), attack, exp_damage)
