from dataclasses import dataclass, field
from copy import deepcopy
from enum import Enum

import main.frakcje.wszystkie_frakcje as allfractions
from main.tokens.data import Ability
from main.tokens.Clever_iniciative import CleverIniciative
from main.tokens.abstract_token import Token as AbstractToken
from main.tokens.data import TokenKey, TokenType, TokenRelation
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
    wire: list[int] = field(default_factory=list)
    boosts: dict = field(default_factory=dict)

    real_boost_target: TokenRelation | None = None
    boost_target: TokenRelation | None = None

    initiative: list[int] = field(default_factory=list)
    clever_iniciative: CleverIniciative | None = None

    meele_boosts: int = 0
    shoot_boosts: int = 0

    # chwilowo zadane np w trakcie bitwy
    wounds : list[int] = field(default_factory=list)

    def __post_init__(self):
        self.load()
        self.rotate()
        self.clever_iniciative = CleverIniciative(self.initiative)
        self.real_boost_target = self.boost_target

    # ---------- reset ----------

    def load(self):
        # print(f"loading token {self.name}")
        data = allfractions.frakcje.get(self.faction, {}).get(self.name, {})
        for key, value in data.items():
            attr_name = key.name if isinstance(key, Enum) else str(key)
            if attr_name.isidentifier():
                setattr(self, attr_name.lower(), deepcopy(value))

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
    
    def set_wire(self):
        self.wired = True

    def unwire(self):
        self.wired = False

    def can_wire(self):
        return len(self.wire) > 0

    def get_wire(self):
        if self.wired:
            return []
        return self.wire

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
        self.wire = [(direction + self.rotation) % 6 for direction in self.wire]

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
            "ability_used" : self.ability_used,
            "clever_iniciative": self.clever_iniciative.export_state() if self.clever_iniciative else None,
        }
        return data
    
    def to_dict_battle(self) -> dict:
        return self.to_dict()
    
    @classmethod
    def from_dict(cls, data: dict) -> "BoardToken":
        data = cls._normalize_dict(data)
        clever_iniciative_data = data.pop("clever_iniciative", None)
        token = Serializator.from_dict_dataclass(cls, data)
        if clever_iniciative_data is not None and token.clever_iniciative is not None:
            token.clever_iniciative.import_state(clever_iniciative_data)
        return token

    @staticmethod
    def _normalize_dict(data: dict) -> dict:
        normalized = dict(data)

        if "fraction" in normalized and "faction" not in normalized:
            normalized["faction"] = normalized["fraction"]

        if "clever_initiative" in normalized and "clever_iniciative" not in normalized:
            normalized["clever_iniciative"] = normalized["clever_initiative"]

        legacy_keys = {
            "ROTATION": "rotation",
            "DAMAGE": "damage",
            "WIRED": "wired",
        }
        for legacy_key, field_name in legacy_keys.items():
            if legacy_key in normalized and field_name not in normalized:
                normalized[field_name] = normalized[legacy_key]

        return normalized
