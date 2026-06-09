from main.board.board import Board, Hex
from main.board.query import BoardQuery
from main.rules.predicates import (
    NOT,
    is_empty_at
    ,token_predicate
)
from main.attacks.data import AttackConfig, DirectedIntent
from main.events.effects import ResolveUnitsDamageEffect, ClearPendingAttacksEffect
from main.events.data import Effect
from main.attacks.data import AttackIntent
from main.attacks.resolver import AttackResolver
from typing import Protocol

class HasBoard(Protocol):
    board : Board

class HasPendingAttacks(Protocol):
    pending_attacks : list[AttackIntent]

class HasCombatCtx(HasBoard, HasPendingAttacks, Protocol):
    pass

class CombatSystem:
    @staticmethod
    def get_activating_positions(board : Board, initiative : int) -> list[Hex]:
        return BoardQuery([
            NOT(is_empty_at),
            token_predicate(lambda t : t.can_activate(initiative)),
        ]).apply(board)
    
    @staticmethod
    def build_attack_intent(attack : AttackConfig, pos : Hex):
        return DirectedIntent(
            attaker_pos=pos,
            direction=attack.direction,
            attack_type=attack.attack_type,
            power=attack.power
        )
    
    @staticmethod
    def resolve_combat_damage(ctx : HasBoard) -> list[Effect]:
        return [
            ResolveUnitsDamageEffect(
                positions=BoardQuery([
                    NOT(is_empty_at)
                ]).apply(ctx.board)
            )
        ]
    
    @staticmethod
    def resolve_pending_attacks(ctx : HasCombatCtx) -> list[Effect]:
            effects = [
                effect
                for attack in ctx.pending_attacks
                for effect in AttackResolver.resolve(attack, ctx.board)
            ]
            effects.append(ClearPendingAttacksEffect())
            return effects