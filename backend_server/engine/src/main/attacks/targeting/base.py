from abc import ABC, abstractmethod
from main.board.board import Board
from main.board.data import Hex

class TargetingStrategy(ABC):
    @staticmethod
    @abstractmethod
    def get_targets(
        board : Board, 
        attacker_pos : Hex, 
        direction : int
    ) -> list[Hex]:
        pass