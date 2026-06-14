from main.board.board import Board, Hex
from main.board.query import BoardQuery
from main.rules.predicates import (
    NOT,
    is_empty_at,
)
from main.events.data import Effect
from main.events.workflow import PushWorkflow
from main.events.effects import (
    ResolveUnitsDamageEffect, 
    ClearPendingAttacksEffect, 
    MarkActivatedUnitsEffect,
    EnqueueAttacksEffect
)

from main.attacks.provider import AttackProvider
from main.attacks.data import AttackIntent
from main.attacks.resolver import AttackResolver

from main.rules.combat import CombatRules
from main.tokens.board_token import BoardToken

from main.workflows.data import BATTLE_ABILITY_WORKFLOW_REGISTRY, WorkflowConfig

from typing import Protocol

class HasBoard(Protocol):
    board : Board

class HasPendingAttacks(Protocol):
    pending_attacks : list[AttackIntent]

class HasCombatCtx(HasBoard, HasPendingAttacks, Protocol):
    pass

class CombatSystem:
    @staticmethod
    def get_non_empty_positions(ctx : HasBoard):
        return BoardQuery([NOT(is_empty_at)]).apply(ctx.board)

    @staticmethod
    def resolve_unit_attack_declarations(unit : BoardToken, pos : Hex) -> Effect:
        if unit.has_battle_ability:
            ability = unit.get_battle_ability()
            wf_name = BATTLE_ABILITY_WORKFLOW_REGISTRY[ability]
            return PushWorkflow(name=wf_name, config=WorkflowConfig(pos=pos))

        # print(f"attacks {AttackProvider.get_attack_intents(unit, pos)}")
        return EnqueueAttacksEffect(AttackProvider.get_attack_intents(unit, pos))

    @classmethod
    def resolve_attack_declaration(cls, ctx : HasBoard, initiative : int) -> list[Effect]:
        positions = cls.get_non_empty_positions(ctx)
        effects = [
            MarkActivatedUnitsEffect(
                positions=positions,
                initiative=initiative    
            )
        ]
        for pos in positions:
            unit = ctx.board.get_token(pos)
            if CombatRules.can_activate(unit, initiative):
                # print(f"ACTIVATING UNIT {unit.get_view()} AT {pos}")
                effects.append(cls.resolve_unit_attack_declarations(unit, pos))

        return effects

    @classmethod
    def resolve_combat_damage(cls, ctx : HasBoard) -> list[Effect]:
        return [
            ResolveUnitsDamageEffect(
                positions=cls.get_non_empty_positions(ctx)
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