from abc import ABC, abstractmethod
from typing import ClassVar
from main.board.board import Hex, Board


class TargetingStrategy(ABC):
    IS_BLOCKALBE : ClassVar[bool] = False
    @staticmethod
    @abstractmethod
    def get_targets(
        board : Board, 
        attacker_pos : Hex, 
        direction : int
    ) -> list[Hex]:
        pass

    @property
    def blockable(self):
        return self.IS_BLOCKALBE