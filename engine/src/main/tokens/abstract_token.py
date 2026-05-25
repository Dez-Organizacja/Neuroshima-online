from abc import ABC, abstractmethod
from main.tokens.data import Ability, TokenType
from dataclasses import dataclass, field

@dataclass
class Token(ABC):
    name         : str
    fraction     : str
    type         : TokenType = field(default_factory=TokenType, init=False)
    ability_used : bool = False
    ability      : Ability = Ability.NO_ABILITY


    def get_ability(self) -> Ability:
        return self.ability