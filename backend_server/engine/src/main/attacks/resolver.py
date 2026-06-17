from main.events.effects import DamageEffect, DestroyEffect, Effect
from main.systems.animations import AnimationSystem
from main.attacks.data import (
    DirectedIntent,
    TargetedIntent,
    AttackResult,
    TargetResoltion,
    AttackLog,
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

    def reduce_damage(self, attack : TargetedIntent) -> int:
        # print("damage reducing")
        # print(f"blockable {attack.blockable}")
        if attack.blockable and attack.from_direction is not None:
            # print("blacable and directed")
            unit = self.board.get_token(attack.target_pos)
            if self.reverse_direction(attack.from_direction) in unit.get_armor():
                return max(attack.power - 1, 0)

        return attack.power
    
    def resolve(self, attack : TargetedIntent) -> TargetResoltion:
        resolution = TargetResoltion(target_pos=attack.target_pos)
        if attack.destroy:
            resolution.effects.append(DestroyEffect(attack.target_pos))
            return resolution

        # print(f"attack {attack}")
        power = self.reduce_damage(attack)
        # print(f"new power {power}")
        if power > 0:
            resolution.effects.append(
                DamageEffect(pos=attack.target_pos, damage=power)
            )
        return resolution


class DirectedResolver:
    @staticmethod
    def get_targets(attack : DirectedIntent, board : Board) -> list[Hex]:
        strategy = TargetingFactory.create(attack.properties.targeting_type)
        return strategy.get_targets(
            board=board,
            attacker_pos=attack.attacker_pos,
            direction=attack.direction,
        )

    @classmethod
    def resolve(cls, attack : DirectedIntent, board : Board) -> list[TargetedIntent]:
        # print(f"RESOLVE DIRECTED")
        # print(f"from {attack.attaker_pos}")
        # print(f"properties: {attack.properties}")
        # print(f"")

        return [
            TargetedIntent(
                target_pos=t,
                attacker_pos=attack.attacker_pos,
                power=attack.power,
                blockable=attack.properties.blockable,
                from_direction=attack.direction,
            )
            for t in cls.get_targets(attack, board)
            if CombatRules.is_valid_attack(attack, t, board)
        ]
    
class AttackResolver:
    @classmethod
    def resolve(cls, attack, board) -> AttackResult:
        # print(f"RESOLVING ATTACK")
        # print(f"from {attack.}")
        expanded = []
        log = AttackLog()

        match attack:
            case DirectedIntent():
                log.attacker_pos = attack.attacker_pos
                expanded = DirectedResolver.resolve(attack, board)

            case TargetedIntent():
                expanded = [attack]

            # print(f"targeted to {t.target_pos} of power {t.power}")

        result = AttackResult()
        resolver = TargetedResolver(board)

        for t in expanded:
            resolution = resolver.resolve(t)
            result.result.extend(resolution.effects)
            log.resolved_targets.append(resolution)
        
        result.animations.extend(AnimationSystem.get_attacks_animations(log))

        return result
