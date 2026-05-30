from dataclasses import dataclass, field
from copy import deepcopy
from enum import Enum

import main.frakcje.wszystkie_frakcje as allfractions
from main.tokens.data import Ability
from main.tokens.Clever_iniciative import CleverIniciative
from main.tokens.abstract_token import Token as AbstractToken
from main.tokens.data import TokenKey, TokenStats, TokenType, TokenRelation
from main.utils.variable import Attack, Boost
from main.state.serialization import Serializator

@dataclass
class BoardToken(AbstractToken):
    # name: str | dict = "default"
    type: TokenType = field(default=TokenType.BOARD, init=False)

    rotation: int = 0
    damage: int = 0
    wired: bool = False
    hp: int = 0
    armor: list[int] = field(default_factory=list)
    unit_count: int | None = None
    attacks: dict = field(default_factory=dict)
    wire_dirs: list[int] = field(default_factory=list)
    boosts: dict = field(default_factory=dict)

    real_boost_target: TokenRelation | None = None
    boost_target: TokenRelation | None = None

    iniciative: list[int] = field(default_factory=list)
    clever_iniciative: CleverIniciative | None = None

    meele_boosts: int = 0
    shoot_boosts: int = 0

    BOOST_TO_ATTACK = {
        Attack.MELEE: "MEELE_BOOSTS",
        Attack.SHOOT: "SHOOT_BOOSTS"
    }

    _LOAD_ATTR_MAP = {
        "ROTATION": "rotation",
        "DAMAGE": "damage",
        "WIRED": "wired",
        "HP": "hp",
        "ARMOR": "armor",
        "UNIT_COUNT": "unit_count",
        "ATTACKS": "attacks",
        "WIRE": "wire_dirs",
        "BOOSTS": "boosts",
        "BOOST_TARGET": "boost_target",
        "INITIATIVE": "iniciative",
        "REAL_BOOST_TARGET": "real_boost_target",
        "MEELE_BOOSTS": "meele_boosts",
        "SHOOT_BOOSTS": "shoot_boosts",
    }

    # chwilowo zadane np w trakcie bitwy
    wounds : list[int] = field(default_factory=list)

    def __post_init__(self):
        self.load()
        self.rotate()
        self.clever_iniciative = CleverIniciative(self.iniciative)
        self.real_boost_target = self.boost_target

    # ---------- reset ----------

    def load(self):
        # print(f"loading token {self.name}")
        data = allfractions.frakcje.get(self.faction, {}).get(self.name, {})
        for key, value in data.items():
            attr_name = key.name if isinstance(key, Enum) else str(key)
            # print(f"attr_name {attr_name}")
            if attr_name.isidentifier():
                setattr(self, self._LOAD_ATTR_MAP.get(attr_name, attr_name.lower()), deepcopy(value))
        # print("load finished")

    def reset(self):
        self.rotation = 0
        self.damage = 0
        self.wired = False

        self.load()

    # --------- HQ ----------

    def is_HQ(self):
        return self.name == "sztab"

    # --------- healer ----------

    @property
    def is_healer(self) -> bool:
        return Boost.HEAL in self.boosts.keys()
    
    @property
    def needs_heal(self) -> bool:
        return len(self.wounds) > 0

    def get_heal_direction(self) -> list[int]:
        return self.boosts.get(Boost.HEAL, [])

    # ---------- wire ----------

    def is_wired(self):
        return self.wired
    
    def wire(self):
        self.wired = True

    def unwire(self):
        self.wired = False

    def can_wire(self):
        return len(self.wire_dirs) > 0

    def get_wire(self):
        if self.wired:
            return []
        return self.wire_dirs

    # --------- rotation ----------

    def rotate(self, direction = None):
        self.load()

        if direction is not None:
            self.rotation = (self.rotation + direction) % 6

        for attack_type, attack_list in self.attacks.items():
            self.attacks[attack_type] = [
                [(direction + self.rotation) % 6, power]
                for direction, power in attack_list
            ]
        
        for boost_type, boost_list in self.boosts.items():
            self.boosts[boost_type] = [
                (direction + self.rotation) % 6
                for direction in boost_list
            ]

        self.armor = [(direction + self.rotation) % 6 for direction in self.armor]
        self.wire_dirs = [(direction + self.rotation) % 6 for direction in self.wire_dirs]

    # --------- hp and armor ----------

    def take_damage(self, direction = None, damage = 1, blockable=False):
        # direction -> from where the attack is coming, 0-5

        if direction is not None:
            direction = (direction + 3) % 6

            if (blockable and self.armor and direction in self.armor):
                damage -= 1
            
        self.damage += max(damage, 0)

    # --------- attacks and boosts ----------

    # boosty bierzesz token.BOOSTS -> dict | None

    def get_boosts(self):
        if self.wired:
            return {}
        return self.boosts

    def get_attacks(self, which_initiative) -> dict:      
        if self.clever_iniciative.activate(which_initiative) or self.wired:
            return {}
        return self.attacks
    
    # --------- save and load ----------

    def to_dict(self) -> dict:
        data = {
            "name": self.name,
            "faction": self.faction,
            "ROTATION": self.rotation,
            "DAMAGE": self.damage,
            "WIRED": self.wired,
            "ability_used" : self.ability_used
        }
        return data
    
    def to_dict_battle(self) -> dict:
        data = {
            "name": self.name,
            "fraction": self.fraction,
            "ROTATION": self.rotation,
            "DAMAGE": self.damage,
            "WIRED": self.wired,
            "ability_used" : self.ability_used,
            "clever_iniciative": self.clever_iniciative.export_iniciative() if self.clever_iniciative else None
        }
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> "BoardToken":
        if "faction" in data and "faction" not in data:
            data = {
                **data,
                "faction": data["faction"]
            }
        return Serializator.from_dict_dataclass(cls, data)

    @property
    def INITIATIVE(self):
        return self.iniciative

    @INITIATIVE.setter
    def INITIATIVE(self, value):
        self.iniciative = value

    @property
    def WIRE(self):
        return self.wire_dirs

    @WIRE.setter
    def WIRE(self, value):
        self.wire_dirs = value

    @property
    def ROTATION(self):
        return self.rotation

    @ROTATION.setter
    def ROTATION(self, value):
        self.rotation = value

    @property
    def DAMAGE(self):
        return self.damage

    @DAMAGE.setter
    def DAMAGE(self, value):
        self.damage = value

    @property
    def WIRED(self):
        return self.wired

    @WIRED.setter
    def WIRED(self, value):
        self.wired = value

    @property
    def ARMOR(self):
        return self.armor

    @ARMOR.setter
    def ARMOR(self, value):
        self.armor = value

    @property
    def ATTACKS(self):
        return self.attacks

    @ATTACKS.setter
    def ATTACKS(self, value):
        self.attacks = value

    @property
    def BOOSTS(self):
        return self.boosts

    @BOOSTS.setter
    def BOOSTS(self, value):
        self.boosts = value

    @property
    def BOOST_TARGET(self):
        return self.boost_target

    @BOOST_TARGET.setter
    def BOOST_TARGET(self, value):
        self.boost_target = value

    @property
    def MEELE_BOOSTS(self):
        return self.meele_boosts

    @MEELE_BOOSTS.setter
    def MEELE_BOOSTS(self, value):
        self.meele_boosts = value

    @property
    def SHOOT_BOOSTS(self):
        return self.shoot_boosts

    @SHOOT_BOOSTS.setter
    def SHOOT_BOOSTS(self, value):
        self.shoot_boosts = value

    @property
    def REAL_BOOST_TARGET(self):
        return self.real_boost_target

    @REAL_BOOST_TARGET.setter
    def REAL_BOOST_TARGET(self, value):
        self.real_boost_target = value

    @property
    def HP(self):
        return self.hp

    @HP.setter
    def HP(self, value):
        self.hp = value

    @property
    def CLEVER_INICIATIVE(self):
        return self.clever_iniciative

    @CLEVER_INICIATIVE.setter
    def CLEVER_INICIATIVE(self, value):
        self.clever_iniciative = value
