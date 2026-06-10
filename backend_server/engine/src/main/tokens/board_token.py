from dataclasses import dataclass, field

from main.tokens.base import Token
from main.state.serialization import Serializator
from main.tokens.clever_initiative import CleverInitiative
from main.tokens.config import BoardTokenConfig, BoostInstance, Boost
from main.tokens.state import BoardTokenState
from copy import deepcopy
from main.state.serialization import Serializator
from main.attacks.data import AttackConfig
from main.tokens.data import TokenView

@dataclass
class BoardToken(Token):
    state : BoardTokenState = field(default_factory=BoardTokenState)

    def reset(self):
        self.state.reset()

    

    # --------- boosts ----------
    @property
    def boosts(self) -> dict[Boost, BoostInstance]:
        return self.config.boosts

    def has_boost(self, boost : Boost) -> bool:
        return boost in self.boosts

    def get_boost_directions(self, boost : Boost) -> list[int]:
        b = self.boosts.get(boost)
        return self.rotate_list(b.directions) if b else []

    def get_boosts(self):
        if self.wired:
            return {}
        return self.boosts
    # --------- healer ----------

    @property
    def is_healer(self) -> bool:
        return self.has_boost(Boost.HEAL)
    
    @property
    def needs_heal(self) -> bool:
        return len(self.wounds) > 0

    def get_heal_directions(self) -> list[int]:
        return self.get_boost_directions(Boost.HEAL)
    
    def pop_highest_wound(self) -> int:
        max_w = max(self.state.wounds)
        self.state.wounds.remove(max_w)
        return max_w

    # ---------- wire ----------
    @property
    def wired(self) -> bool:
        return self.state.wired
    
    @property
    def wires(self) -> list[int]:
        return self.config.wire
    
    def set_wire(self, value : bool = True) -> None:
        return self.state.set_wired(value)

    def can_wire(self) -> bool:
        return len(self.wires) > 0

    def get_wire_directions(self) -> list:
        return self.rotate_list(self.wires)

    # --------- rotation ----------

    @property
    def rotation(self) -> int:
        return self.state.rotation

    def set_rotation(self, rotation):
        self.state.set_rotation(rotation)
    
    def get_real_direction(self, int) -> int:
        return (int + self.rotation) % 6

    def rotate_list(self, arr : list[int]) -> list[int]:
        return [
            self.get_real_direction(direction)
            for direction in arr
        ]
    # --------- hp and armor ----------
    @property
    def wounds(self) -> list[int]:
        return self.state.wounds

    def add_wounds(self, wounds : int):
        self.state.core.wounds.append(wounds)

    def claer_wounds(self):
        self.state.core.wounds = []

    def add_damage(self, damage : int):
        self.state.core.damage += damage

    def get_armor(self):
        return self.rotate_list(self.config.armor)

    @property
    def is_alive(self) -> bool:
        return self.config.hp > self.state.damage

    # --------- initiative ----------
    @property
    def clever_initiative(self):
        return self.state.clever_initiative

    # def can_activate(self, initiative):
    #     return not self.wired and CleverInitiative.can_activate(self, initiative)

    def mark_activated(self, initiative : int):
        return CleverInitiative.mark_activated(self, initiative)

    # --------- attacks ----------

    @property
    def attacks(self):
        return self.config.attacks

    def get_attacks(self) -> list[AttackConfig]:
        attacks = deepcopy(self.attacks)
        for attack in attacks:
            attack.direction = self.get_real_direction(attack.direction)
        return attacks
    
    # --------- attacks ----------
    @property
    def ability_used(self):
        return self.state.exection.used_ability
    
    @ability_used.setter
    def ability_used(self, value):
        self.state.exection.used_ability = value

    # --------- save and load ----------

    def to_dict(self) -> dict:
        return Serializator.to_dict_dataclass(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "BoardToken":
        return Serializator.from_dict_dataclass(cls, data)

    def get_view(self) -> TokenView:
        return TokenView(
            faction= self.faction,
            name= self.name,
            rotation= self.rotation,
            ability_used= self.ability_used,
            damage= self.state.damage + sum(self.wounds),
            wired= self.wired,
        )
