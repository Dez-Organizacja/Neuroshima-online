from main.tokens.hand import Hand
from main.tokens.pile import Pile
from dataclasses import dataclass, field

@dataclass
class PlayerState:
    hand : Hand = field(default_factory=Hand)
    pile : Pile = field(default_factory=Pile)