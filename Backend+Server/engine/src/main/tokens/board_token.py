from dataclasses import dataclass, field
from copy import deepcopy
from enum import Enum

import main.frakcje.wszystkie_frakcje as allfractions
from main.tokens.data import Ability
from main.tokens.abstract_token import Token as AbstractToken
from main.tokens.data import TokenKey, TokenStats, TokenType, TokenRelation
from main.utils.variable import Attack, Boost
from main.state.serialization import Serializator

@dataclass
class BoardToken(AbstractToken):
    # name: str | dict = "default"
    type: TokenType = field(default=TokenType.BOARD, init=False)

    ROTATION: int = 0
    DAMAGE: int = 0
    WIRED: bool = False
    HP: int = 0
    ARMOR: list[int] = field(default_factory=list)
    UNIT_COUNT: int | None = None
    ATTACKS: dict = field(default_factory=dict)
    WIRE: list[int] = field(default_factory=list)
    BOOSTS: dict = field(default_factory=dict)
    BOOST_TARGET: TokenRelation | None = None

    INITIATIVE: list[int] = field(default_factory=list)


    def __post_init__(self):
        # if isinstance(self.name, dict):
        #     data = self.name
        #     self.name = data.get("name", "default")
        #     self.fraction = data.get("fraction", "neutral")
        #     self.ROTATION = data.get("ROTATION", 0)
        #     self.DAMAGE = data.get("DAMAGE", 0)
        #     self.WIRED = data.get("WIRED", False)

        self.load()
        self.rotate()

    # ---------- reset ----------

    def load(self):
        data = allfractions.frakcje.get(self.fraction, {}).get(self.name, {})
        for key, value in data.items():
            attr_name = key.name if isinstance(key, Enum) else str(key)
            if attr_name.isidentifier():
                setattr(self, attr_name, deepcopy(value))

    def reset(self):
        self.ROTATION = 0
        self.DAMAGE = 0
        self.WIRED = False

        self.load()

    # --------- HQ ----------

    def is_HQ(self):
        return self.name == "sztab"

    # ---------- wire ----------

    def is_wired(self):
        return self.WIRED
    
    def wire(self):
        self.WIRED = True

    def unwire(self):
        self.WIRED = False

    def can_wire(self):
        return len(self.WIRE) > 0


    # --------- rotation ----------

    def rotate(self, direction = None):
        self.load()

        if direction is not None:
            self.ROTATION = (self.ROTATION + direction) % 6

        for attack_type, attack_list in self.ATTACKS.items():
            self.ATTACKS[attack_type] = [
                [(direction + self.ROTATION) % 6, power]
                for direction, power in attack_list
            ]
        
        for boost_type, boost_list in self.BOOSTS.items():
            self.BOOSTS[boost_type] = [
                (direction + self.ROTATION) % 6
                for direction in boost_list
            ]

        self.ARMOR = [(direction + self.ROTATION) % 6 for direction in self.ARMOR]
        self.WIRE = [(direction + self.ROTATION) % 6 for direction in self.WIRE]

    # --------- hp and armor ----------

    def take_damage(self, direction = None, damage = 1, blockable=False):
        # direction -> from where the attack is coming, 0-5

        if direction is not None:
            direction = (direction + 3) % 6

            if (blockable and self.ARMOR and direction in self.ARMOR):
                damage -= 1
            
        self.DAMAGE += max(damage, 0)

    # --------- attacks and boosts ----------

    # boosty bierzesz token.BOOSTS -> dict | None

    def get_wire(self):
        if self.WIRED:
            return []
        return self.WIRE

    def get_boosts(self):
        if self.WIRED:
            return {}
        return self.BOOSTS

    def get_attacks(self, which_initiative):      
        if which_initiative not in self.INITIATIVE or self.WIRED:
            return {}
        return self.ATTACKS
        
    def get_ability(self) -> Ability:
        return Ability.NO_ABILITY
    
    def to_dict(self) -> dict:
        data = {
            "name": self.name,
            "fraction": self.fraction,
            "ROTATION": self.ROTATION,
            "DAMAGE": self.DAMAGE,
            "WIRED": self.WIRED,
            "ability_used" : self.ability_used
        }
        return data
    
    @classmethod
    def from_dict(cls, data : dict) -> BoardToken:
        return Serializator.from_dict_dataclass(cls, data)