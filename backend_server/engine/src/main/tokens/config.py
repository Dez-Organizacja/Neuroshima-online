from __future__ import annotations

from dataclasses import dataclass, field
from main.tokens.data import Ability, BattleAbility, TokenType, TokenRelation, Boost
from main.attacks.config import AttackConfig

@dataclass 
class Abilities:
    ability             : Ability | None = None
    battle_ability      : BattleAbility | None = None

@dataclass
class TokenConfigId:
    name        : str
    faction     : str
    def to_tuple(self):
        return (self.faction, self.name)

@dataclass
class TokenConfig:
    faction     : str
    name        : str
    type        : TokenType
    unit_count  : int
    
    abilities   : Abilities = field(default_factory=Abilities)

    @property
    def has_ability(self):
        return self.abilities.ability is not None
    
    @property
    def has_battle_ability(self):
        return self.abilities.battle_ability is not None
    
    def get_ability(self) -> Ability | None:
        return self.abilities.ability

    def get_battle_ability(self) -> BattleAbility | None:
        return self.abilities.battle_ability
    
@dataclass
class BoostInstance:
    directions : list[int]

@dataclass  
class BoardTokenConfig(TokenConfig):
    hp              : int = 0

    armor           : list[int] = field(default_factory=list)
    wire            : list[int] = field(default_factory=list)
    initiative      : list[int] = field(default_factory=list)

    attacks         : list[AttackConfig] = field(default_factory=list)
    
    boosts          : dict[Boost, BoostInstance] = field(default_factory=dict)
    
    boost_target    : TokenRelation = TokenRelation.OWN

    @classmethod
    def from_base(cls: type[BoardTokenConfig], base: TokenConfig) -> BoardTokenConfig:
        return cls(
            faction=base.faction,
            name=base.name,
            type=base.type,
            unit_count=base.unit_count,
        )
