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

    # @staticmethod
    # def get_target_faction(unit : BoardToken):


    # def get_targets(self, board : Board, healer_pos : Hex):
    #     # print(f"possible getting targets for {healer_pos}")
    #     healer = board.get_token(healer_pos)
    #     to_target_relation = healer.state.relations.real_boost_target
    #     heal_directions = healer.get_heal_directions()
    #     candidates = [
    #         board.go(healer_pos, direction)
    #         for direction in heal_directions
    #     ]
    #     # print(f"candidates {candidates}")
    #     possible_targets = set(
    #         BoardQuery([
    #             NOT(is_empty_at),
    #             of_relation_to(to_target_relation, healer),
    #             predicate_maker(self.needs_heal),
    #         ]).apply(board)
    #     )
    #     # print(f"posible targets {possible_targets}")
    #     return [pos for pos in candidates if pos in possible_targets]

    # def non_healers_targets(self, board : Board, healer_pos : Hex) -> list[Hex]:
    #     return [
    #         pos
    #         for pos in self.get_targets(board, healer_pos)
    #         if not self.is_healer(board.get_token(pos))
    #     ]

    # def get_candidate_sources(self, board : Board, target_faction : str) -> list[Hex]:
    #     positions = BoardQuery([
    #         NOT(is_empty_at),
    #         token_predicate(lambda t : not t.wired),
    #         predicate_maker(self.is_healer),
    #         NOT(predicate_maker(self.needs_heal))
    #     ]).apply(board)

    #     return [pos for pos in positions if ]


    # def get_sources(self, board : Board, faction : str):
    #     # print(f"getting heal sources for faction {faction}")

    #     # print(f"candidates {self.get_candidate_sources(board, faction)}")  
    #     return [
    #         pos 
    #         for pos in self.get_candidate_sources(board, faction) 
    #         if any(self.get_targets(board, pos))
    #     ]
    
    # def is_finished(self, board : Board, faction : str) -> bool:
    #     # sources = self.get_sources(board, faction)
    #     # print(f"sources {sources}")
    #     return not self.get_sources(board, faction)
    #     # true jezeli nie 

    # def can_end(self, board : Board, faction : str) -> bool:
    #     for source in self.get_candidate_sources(board, faction):
    #         if self.non_healers_targets(board, source):
    #             return False
    #     return True