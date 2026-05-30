from abc import ABC, abstractmethod
from main.tokens.data import Ability, TokenType
from dataclasses import dataclass, field

@dataclass
class Token(ABC):
    name         : str
    faction      : str
    ability_used : bool = False
    ABILITY      : Ability | None = None
    type         : TokenType = field(default_factory=TokenType, init=False)


    def get_ability(self) -> Ability | None:
        return self.ABILITY