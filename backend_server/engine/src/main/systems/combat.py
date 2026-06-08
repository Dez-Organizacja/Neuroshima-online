from main.board.board import Board, Hex
from main.board.query import BoardQuery
from main.rules.predicates import (
    NOT,
    is_empty_at
    ,token_predicate
)
from main.attacks.data import AttackConfig, DirectedIntent

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