from main.rules.ability.base import AbilityRules
from main.board.board import Board, Hex
from main.board.query import BoardQuery
from main.rules.predicates import (
    token_predicate,
    is_empty_at,
    is_ally_of,
    is_ally,
    NOT,
    predicate_maker,
    of_relation_to,
)
from main.tokens.board_token import BoardToken

class HealRules(AbilityRules):
    @staticmethod
    def needs_heal(unit : BoardToken) -> bool:
        return len(unit.wounds) > 0

    @staticmethod
    def is_healer(unit : BoardToken) -> bool:
        return len(unit.get_heal_directions()) > 0

    def get_targets(self, board : Board, healer_pos : Hex):
        # print(f"possible getting targets for {healer_pos}")
        healer = board.get_token(healer_pos)
        to_target_relation = healer.state.relations.real_boost_target
        heal_directions = healer.get_heal_directions()
        candidates = [
            board.go(healer_pos, direction)
            for direction in heal_directions
        ]
        # print(f"candidates {candidates}")
        possible_targets = set(
            BoardQuery([
                NOT(is_empty_at),
                of_relation_to(to_target_relation, healer),
                predicate_maker(self.needs_heal),
            ]).apply(board)
        )
        # print(f"posible targets {possible_targets}")
        return [pos for pos in candidates if pos in possible_targets]

    def non_healers_targets(self, board : Board, healer_pos : Hex) -> list[Hex]:
        return [
            pos
            for pos in self.get_targets(board, healer_pos)
            if not self.is_healer(board.get_token(pos))
        ]

    def get_candidate_sources(self, board : Board, faction : str) -> list[Hex]:
        return BoardQuery([
            NOT(is_empty_at),
            is_ally(faction),
            token_predicate(lambda t : not t.wired),
            predicate_maker(self.is_healer),
            NOT(predicate_maker(self.needs_heal))
        ]).apply(board)


    def get_sources(self, board : Board, faction : str):
        # print(f"getting heal sources for faction {faction}")

        # print(f"candidates {self.get_candidate_sources(board, faction)}")  
        return [
            pos 
            for pos in self.get_candidate_sources(board, faction) 
            if any(self.get_targets(board, pos))
        ]
    
    def is_finished(self, board : Board, faction : str) -> bool:
        # sources = self.get_sources(board, faction)
        # print(f"sources {sources}")
        return not self.get_sources(board, faction)
        # true jezeli nie 

    def can_end(self, board : Board, faction : str) -> bool:
        for source in self.get_candidate_sources(board, faction):
            if self.non_healers_targets(board, source):
                return False
        return True