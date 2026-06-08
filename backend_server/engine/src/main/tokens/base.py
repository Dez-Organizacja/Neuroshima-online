from main.tokens.data import Ability, BattleAbility
from main.tokens.config import TokenConfigId, BoardTokenConfig
# from main.tokens.state import 
from dataclasses import dataclass
from main.tokens.registry import TokenConfigRegistry

@dataclass
class Token:
    config_id : TokenConfigId

    @property
    def config(self) -> BoardTokenConfig:
        return TokenConfigRegistry.get(*self.config_id.to_tuple())
    
    @property
    def name(self):
        return self.config_id.name
    
    @property
    def faction(self):
        return self.config_id.faction

    @property
    def type(self):
        return self.config.type

    @property
    def has_battle_ability(self):
        return self.config.has_battle_ability
    
    @property
    def has_ability(self):
        return self.config.has_ability

    def get_ability(self) -> Ability | None:
        # print(f"get ability of token {self}")
        return self.config.get_ability()

    def get_battle_ability(self) -> BattleAbility | None:
        return self.config.get_battle_ability()