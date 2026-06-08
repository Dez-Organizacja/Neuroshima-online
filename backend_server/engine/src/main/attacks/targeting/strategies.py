from main.attacks.targeting.base import TargetingStrategy
from main.attacks.targeting.factory import TargetingFactory
from main.attacks.data import AttackType
from main.board.query import BoardQuery
from main.board.board import Hex, Board
from main.rules.predicates import adjacent_to, in_line_to, is_enemy_of
from typing import ClassVar

@TargetingFactory.register(AttackType.MELEE)
class AdjacentDirection(TargetingStrategy):
    @staticmethod
    def get_targets(
        board : Board, 
        attacker_pos : Hex, 
        direction : int
    ) -> list[Hex]:
        return BoardQuery([
            adjacent_to(attacker_pos),
            in_line_to(attacker_pos, direction),
            is_enemy_of(board.get_token(attacker_pos))
        ]).apply(board)

@TargetingFactory.register(AttackType.SHOOT)
class FirstInLine(TargetingStrategy):
    IS_BLOCKALBE : ClassVar[bool] = True
    @staticmethod
    def get_targets(
        board : Board, 
        attacker_pos : Hex, 
        direction : int
    ) -> list[Hex]:
        attacker = board.get_token(attacker_pos)
        pos = attacker_pos
        while(board.on_board(pos) and not is_enemy_of(attacker)(board, pos)):
            pos = board.go(pos, direction)

        if is_enemy_of(attacker)(board, pos):
            return [pos]

        return []
    
@TargetingFactory.register(AttackType.GAUSS)
class AllEnemiesInLine(TargetingStrategy):
    @staticmethod
    def get_targets(
        board : Board, 
        attacker_pos : Hex, 
        direction : int
    ) -> list[Hex]:
        return BoardQuery([
            in_line_to(attacker_pos, direction),
            is_enemy_of(board.get_token(attacker_pos))
        ]).apply(board)
