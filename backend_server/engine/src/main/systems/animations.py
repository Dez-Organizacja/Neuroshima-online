from main.events.animations import (
    Animation,
    WoundAnimation,
    AttackAnimation,
    DestroyAnimation,
)
from main.board.board import Hex
from main.attacks.data import AttackLog, TargetResoltion
from main.events.effects import Effect, DamageEffect, DestroyEffect

class AnimationSystem:
    @staticmethod
    def add_wounds_animation(effect : DamageEffect) -> list[Animation]:
        if effect.damage > 0:
            return [WoundAnimation(effect.pos, effect.damage)]
        return []

    @staticmethod
    def add_destroy_animation(effect : DestroyEffect) -> list[Animation]:
        return [DestroyAnimation(effect.pos)]

    @classmethod
    def form_effect_animations(cls, effect : Effect) -> list[Animation]:
        match effect:
            case DamageEffect():
                return cls.add_wounds_animation(effect)
            case DestroyEffect():
                return cls.add_destroy_animation(effect)
            
        raise ValueError(f"effect {effect} not matched")

    @staticmethod
    def attack_animation(
        attacker_pos : tuple[int, int], 
        resolution : TargetResoltion
    ) -> list[Animation]:
        if attacker_pos is not None:
            return [AttackAnimation(attacker_pos, resolution.target_pos)]
        return []

    @classmethod
    def get_attacks_animations(
        cls, log : AttackLog
    ) -> list[Animation]:
        result = []
        for resolution in log.resolved_targets:
            result.extend(cls.attack_animation(log.attacker_pos, resolution))

            for effect in resolution.effects:
                result.extend(cls.form_effect_animations(effect))

        return result