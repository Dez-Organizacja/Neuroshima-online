from main.attacks.data import DirectedIntent
from main.board.board import Board
from main.board.data import Hex
from main.board.query import BoardQuery
from main.rules.predicates import (
    NOT,
    is_empty_at,
    token_predicate
)
from main.tokens.board_token import BoardToken
from main.systems.clever_initiative import CleverInitiative

class CombatRules:
    @staticmethod
    def is_valid_attack(
            attack : DirectedIntent, 
            target_pos : Hex, 
            board : Board
        ) -> bool:
        attacker = board.get_token(attack.attacker_pos)
        target = board.get_token(target_pos)
        return not attacker.is_HQ or not target.is_HQ
    
    @staticmethod
    def can_activate(unit : BoardToken, initiative : int) -> bool:
        return (
            not unit.wired
            and CleverInitiative.can_activate(unit.state, initiative)
        )

    # @staticmethod
    # def get_activating_positions(board : Board, initiative : int) -> list[Hex]:
    #     return BoardQuery([
    #         NOT(is_empty_at),
    #         token_predicate(lambda t : t.can_activate(initiative)),
    #     ]).apply(board)
    
    