from main.rules.ability.base import AbilityRules
from main.board.board import Board, Hex
from main.board.query import BoardQuery
from main.rules.predicates import (
    is_empty_at,
    NOT,
    is_ally,
    predicate_maker,
)
from main.tokens.board_token import BoardToken
from main.rules.faction_manager import FactionManager

class HealRules:
    @staticmethod
    def needs_heal(unit : BoardToken) -> bool:
        return len(unit.wounds) > 0

    @staticmethod
    def is_healer(unit : BoardToken) -> bool:
        return len(unit.get_heal_directions()) > 0

    @staticmethod
    def can_heal(healer : BoardToken, target : BoardToken) -> bool:
        expected_relation = healer.state.relations.real_boost_target
        real_relation = FactionManager.get_relation(healer.faction, target.faction)
        return expected_relation == real_relation

    @staticmethod
    def in_range(healer_pos : Hex, target_pos : Hex, board : Board) -> bool:
        directions = board.get_token(healer_pos).get_heal_directions()
        return any(
            board.go(healer_pos, direction) == target_pos
            for direction in directions
        )

    @classmethod
    def get_targets(cls, board : Board, faction : str) -> list[Hex]:
        candidates = BoardQuery([
            NOT(is_empty_at),
            is_ally(faction),
            predicate_maker(cls.needs_heal),
        ]).apply(board)

        return [
            pos 
            for pos in candidates 
            if len(cls.get_healers(board, pos)) > 0
        ]

    @classmethod
    def get_possible_healers(cls, board : Board):
        return BoardQuery([
            NOT(is_empty_at),
            NOT(predicate_maker(cls.needs_heal)),
            predicate_maker(cls.is_healer)
        ]).apply(board)


    @classmethod
    def get_healers(cls, board : Board, target_pos) -> list[Hex]:
        candidates = cls.get_possible_healers(board)
        target = board.get_token(target_pos)
        return [
            pos 
            for pos in candidates 
            if cls.can_heal(board.get_token(pos), target)
            and cls.in_range(pos, target_pos, board)
        ]

    @classmethod
    def get_non_healers_targets(cls, board : Board, faction : str) -> list[Hex]:
        return [
            pos
            for pos in cls.get_targets(board, faction)
            if not cls.is_healer(board.get_token(pos))
        ]

    @classmethod
    def is_finished(cls, board : Board, faction : str) -> bool:
        return len(cls.get_targets(board, faction)) == 0


    @classmethod
    def can_end(cls, board : Board, faction : str) -> bool:
        mandatory_targets = cls.get_non_healers_targets(board, faction)
        return len(mandatory_targets) == 0