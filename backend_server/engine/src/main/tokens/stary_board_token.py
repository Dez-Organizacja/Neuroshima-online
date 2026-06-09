from dataclasses import dataclass, field
from copy import deepcopy
from enum import Enum

import main.frakcje.wszystkie_frakcje as allfractions
from main.tokens.data import Ability
from main.tokens.clever_initiative import CleverInitiative
from main.tokens.base import Token
from main.tokens.data import TokenKey, TokenType, TokenRelation
from main.utils.variable import Attack, Boost
from main.state.serialization import Serializator
from main.tokens.config import BoardTokenConfig
from main.tokens.state import BoardTokenState

@dataclass
class BoardToken(Token):
    name: str | dict = "default"
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
    clever_initiative: CleverInitiative | None = None

    meele_boosts: int = 0

    # chwilowo zadane np w trakcie bitwy
    wounds : list[int] = field(default_factory=list)

    def __post_init__(self):
        clever_initiative_data = self.clever_initiative
        # self.load()
        self.rotate()
        
        self.clever_initiative = CleverInitiative(self.initiative)
        if clever_initiative_data is not None:
            if isinstance(clever_initiative_data, CleverInitiative):
                self.clever_initiative.import_state(clever_initiative_data.export_state())
            else:
                self.clever_initiative.import_state(clever_initiative_data)
        self.real_boost_target = self.boost_target

    # ---------- reset ----------

    def load(self):
        print(f"loading token {self.name}")
        data = allfractions.frakcje.get(self.faction, {}).get(self.name, {})
        for key, value in data.items():
            attr_name = key.name if isinstance(key, Enum) else str(key)
            if attr_name.isidentifier():
                setattr(self, attr_name.lower(), deepcopy(value))

        self.rotation = 0
        self.damage = 0
        self.wired = False

        self.load()

    def reset(self):
        self.wired = 0
        self.rotation = 0
        self.load()
        # self.state.reset()

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

    def get_heal_directions(self) -> list[int]:
        return self.boosts.get(Boost.HEAL, [])
    
    def pop_highest_wound(self):
        self.wounds.sort()
        return self.wounds.pop(-1)

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

    def take_wounds(self, damage):
        if damage > 0:
            self.wounds.append(damage)

    def apply_wounds(self):
        self.damage += sum(self.wounds)
        self.wounds.clear()

    def reduce_damage(self, damage : int, direction : int) -> int:
        # direction -> from where the attack is coming, 0-5
        direction = (direction + 3) % 6
        if direction in self.armor:
            damage = max(damage - 1, 0)

        return damage

    def take_damage(self, direction = None, damage = 1, blockable=False):
        if direction is not None and blockable:
            damage = self.reduce_damage(damage, direction)
            
        self.take_wounds(damage)

    @property
    def is_alive(self):
        return self.hp > self.damage

    # --------- attacks and boosts ----------

    # boosty bierzesz token.BOOSTS -> dict | None

    def can_activate(self, initiative):
        return self.clever_initiative.can_activate(initiative)

    def mark_activated(self, initiative : int):
        self.clever_initiative.activate(initiative)

    def get_boosts(self):
        if self.wired:
            return {}
        return self.boosts

    def get_attacks(self, which_initiative) -> dict:      
        if self.clever_initiative.activate(which_initiative) or self.wired:
            return {}
        return self.attacks
    
    # --------- save and load ----------

    def to_dict(self) -> dict:
        data = {
            "name": self.name,
            "faction": self.faction,
            "hp": self.hp,
            "rotation": self.rotation,
            "damage": self.damage,
            "wounds": self.wounds,
            "wired": self.wired,
            "abilities" : Serializator.to_dict_dataclass(self.abilities),
        }
        return data
    
    def to_dict_battle(self) -> dict:
        data = self.to_dict()
        data["clever_iniciative"] = self.clever_initiative.export_state() if self.clever_initiative else None

        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> "BoardToken":
        normalized = dict(data)
        clever_initiative_data = normalized.pop("clever_initiative", None)
        if clever_initiative_data is None:
            clever_initiative_data = normalized.pop("clever_iniciative", None)

        token = Serializator.from_dict_dataclass(cls, normalized)
        if clever_initiative_data is not None and token.clever_initiative is not None:
            token.clever_initiative.import_state(clever_initiative_data)
        return token
