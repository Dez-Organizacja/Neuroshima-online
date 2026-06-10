from main.events.effects import DamageEffect, DestroyEffect, Effect
from main.attacks.data import (
    AttackIntent,
    DirectedIntent,
    TargetedIntent,
    AttackConfig,   
)
from main.rules.combat import CombatRules
from main.board.board import Board, Hex
from main.attacks.targeting.factory import TargetingFactory

class TargetedResolver:
    def __init__(self, board : Board):
        self.board = board
    
    @staticmethod
    def reverse_direction(direction : int):
        return (direction + 3) % 6

    def reduce_damage(self, attack : TargetedIntent):
        if attack.blockable and attack.from_direction is not None:
            unit = self.board.get_token(attack.target_pos)
            if unit is None:
                return 0
            if self.reverse_direction(attack.from_direction) in unit.get_armor():
                return max(attack.power - 1, 0)

        return attack.power
    
    def resolve(self, attack : TargetedIntent) -> list[Effect]:
        unit = self.board.get_token(attack.target_pos)
        if unit is None:
            return []

        if attack.destroy:
            return [DestroyEffect(attack.target_pos)]

        power = self.reduce_damage(attack)
        if power <= 0:
            return []

        return [DamageEffect(pos=attack.target_pos, damage=power)]

class DirectedResolver:
    @classmethod
    def resolve(cls, attack : DirectedIntent, board : Board) -> list[TargetedIntent]:
        strategy = TargetingFactory.create(attack.attack_type)
        targets = strategy.get_targets(
            board=board,
            attacker_pos=attack.attaker_pos,
            direction=attack.direction,
        )

        return [
            TargetedIntent(
                target_pos=t,
                power=attack.power,
                blockable=strategy.blockable,
                from_direction=attack.direction,
            )
            for t in targets
            if CombatRules.is_valid_attack(attack, t, board)
        ]
    
class AttackResolver:
    @classmethod
    def resolve(cls, attack, board):
        match attack:
            case DirectedIntent():
                expanded = DirectedResolver.resolve(attack, board)

            case TargetedIntent():
                expanded = [attack]

        result = []
        resolver = TargetedResolver(board)

        for t in expanded:
            result.extend(resolver.resolve(t))

        return result
