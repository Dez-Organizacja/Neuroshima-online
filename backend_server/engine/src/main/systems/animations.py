from main.events.animations import (
    Animation,
    WoundAnimation,
    AttackAnimation,
)
from main.board.board import Hex
from main.events.effects import DamageEffect

class AnimationSystem:
    @staticmethod
    def get_attacks(
        attacker_pos : Hex, effects : list[DamageEffect]
    ) -> list[Animation]:
        result = []
        for effect in effects:
            result.extend([
                AttackAnimation(attacker=attacker_pos, target=effect.pos),
                WoundAnimation(target=effect.pos, wounds=effect.damage)
            ])
        return result