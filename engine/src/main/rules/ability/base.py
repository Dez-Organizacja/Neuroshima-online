from abc import ABC
from typing import TypeVar, Generic

R = TypeVar("R", bound=AbilityRules)

class AbilityRules(ABC, Generic[R]):
    def __int__(self, rules : R):
        self.rules = rules