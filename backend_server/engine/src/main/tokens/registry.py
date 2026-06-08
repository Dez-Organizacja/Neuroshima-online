from main.tokens.config import TokenConfig
from typing import TypeVar
C = TypeVar("C", bound=TokenConfig)

class TokenConfigRegistry:
    _CONFIGS : dict[tuple[str, str], C] = {}

    @classmethod
    def registry(cls, config : C) -> None:
        cls._CONFIGS[(config.faction, config.name)] = config

    @classmethod
    def get(cls, faction : str, name : str) -> C:
        return cls._CONFIGS[(faction, name)]
    
    @classmethod
    def get_faction_units(cls, faction):
        return [
            name
            for (f, name) in cls._CONFIGS.keys()
            if f == faction
        ]