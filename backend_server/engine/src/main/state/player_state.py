from main.tokens.hand import Hand
from main.tokens.pile import Pile
from dataclasses import dataclass, field

@dataclass
class PlayerState:
    hand : Hand = field(default_factory=Hand)
    pile : Pile = field(default_factory=Pile)

    move_range : int = 1
    moves_used : int = 0

    def reset_boosts(self):
        self.move_range = 1

    def reset_execution(self):
        self.moves_used = 0

    @property
    def has_moves(self):
        return self.move_range > self.moves_used