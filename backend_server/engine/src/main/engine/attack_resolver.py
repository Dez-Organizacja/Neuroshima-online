# from main.events.effects import DamageEffect
# from main.events.data import (
#     AttackIntent,
#     DirectedAttackIntent,
#     TargetedAttackIntent
# )
# from main.state.context import ActionContext
# from main.board.board import Hex
# from main.attacks.targeting.factory import TargetingFactory

# class AttackResolver:

#     @staticmethod
#     def reduce_damage(
#         ctx : ActionContext, 
#         targets : list[Hex], 
#         direction : int, 
#         power : int
#     ) -> int:
#         return [
#             (pos, ctx.board.get_token(pos).reduce_damage(power, direction))
#             for pos in targets
#         ]

#     @staticmethod
#     def to_tuple_list(targets : list[Hex], power : int):
#         return [
#             (pos, power)
#             for pos in targets
#         ]

#     @staticmethod
#     def convert_to_damage(attacks : list[tuple[Hex, int]]):
#         return [
#             DamageEffect(pos=target, power=power)
#             for target, power in attacks
#         ]

#     @classmethod
#     def handle_targeted_attack(cls, attack : AttackIntent, ctx : ActionContext):
#         attacks = cls.to_tuple_list(
#             targets=[attack.target_pos], 
#             power=attack.power,
#         )
#         return cls.convert_to_damage(attacks)
    
#     @classmethod
#     def handle_directed_attack(cls, attack : AttackIntent, ctx : ActionContext):
#         targeting_rules = TargetingFactory.create(attack.targeting)
#         targets = targeting_rules.get_targets(
#             ctx=ctx,
#             attacker_pos=attack.attaker_pos,
#             direction=attack.direction,
#         )
#         if targeting_rules.blockable:
#             attacks = cls.reduce_damage(
#                 ctx=ctx, 
#                 targets=targets,
#                 direction=attack.direction,
#                 power=attack.power
#             )
#         else:
#             attacks = cls.to_tuple_list(targets, attack.power)
        
#         return cls.convert_to_damage(attacks)

#     @classmethod
#     def resolve(cls, attack : AttackIntent, ctx: ActionContext):
#         match attack:
#             case TargetedAttackIntent():
#                 return cls.handle_targeted_attack(attack, ctx)
#             case DirectedAttackIntent():
#                 return cls.handle_directed_attack(attack, ctx)
                