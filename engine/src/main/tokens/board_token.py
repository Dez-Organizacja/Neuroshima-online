from copy import deepcopy
from enum import Enum

from main.utils.variable import Attack, Boost
from main.tokens.abstract_token import Token
from main.tokens.data import TokenKey, TokenStats, TokenType
from main.tokens.properties import Properties


class BoardToken(Token):
    DEFAULT = {
        TokenKey.NAME: "default",
        TokenKey.FRACTION: "neutral",
        TokenKey.ROTATION: 0,
        TokenKey.DAMAGE: 0,
    }

    TYPE = TokenType.BOARD

    def __init__(self, data=None):
        merged = deepcopy(self.DEFAULT)

        if data is not None:
            merged.update(deepcopy(data))

        super().__init__(merged[TokenKey.NAME], merged[TokenKey.FRACTION], TokenType.BOARD)

        self.rotation = merged[TokenKey.ROTATION]
        self.fraction = merged[TokenKey.FRACTION]
        self.damage = merged[TokenKey.DAMAGE]
        self.name = merged[TokenKey.NAME]

        self.properties = Properties(self.name, self.fraction)

        # print("mam na imie:", name)
        print(merged)

        self.wired = False

        self.boost_to_attack = {
            Boost.MELEE: Attack.MELEE,
            Boost.SHOOT: Attack.SHOOT,
        }

    def get_ability(self):
        return super().get_ability()

    # ---------------- properties ----------------

    def get_property(self, key: Enum, default=None):
        return getattr(self.properties, key.name, default)

    def set_property(self, key: Enum, value) -> None:
        setattr(self.properties, key.name, value)

    def has_property(self, key: Enum) -> bool:
        return hasattr(self.properties, key.name)

    def __getitem__(self, key: Enum):
        return self.get_property(key)

    # ---------------- basic data ----------------

    @property
    def name_pl(self):
        return self.name

    @property
    def fraction_pl(self):
        return self.fraction
        
    def to_json(self):
        return {
            Token.FRACTION: self.fraction,
            Token.NAME: self.name,
            Token.ROTATION: self.rotation,
            Token.DAMAGE: self.damage,
            Token.WIRED: self.wired,
        }

    # ---------------- wire ----------------

    def wire(self) -> None:
        self.wired = True

    def unwire(self) -> None:
        self.wired = False

    def is_wired(self) -> bool:
        return self.wired

    def can_wire(self) -> bool:
        return self.has_property(TokenStats.SIEC)

    # ---------------- boosts / modules ----------------

    def is_booster(self) -> bool:
        return self.has_property(TokenStats.BOOSTS)

    def get_boosts(self):
        return self.get_property(TokenStats.BOOSTS, {})

    def steal_boost(self) -> None:
        if self.is_booster():
            self.set_property(TokenStats.BOOST_TARGET, "enemy")

    # ---------------- stats ----------------

    def reset_properties(self) -> None:
        self.properties = Properties(self.name, self.fraction)

    def rotate(self, rotation: int) -> None:
        self.rotation = rotation

    def take_damage(self, damage: int) -> None:
        self.damage += max(0, damage)

    def receive_attack(self, damage: int, direction: int, blockable=False) -> None:
        relative_direction = (direction - self.rotation + 6) % 6

        armor = self.get_property(TokenStats.ARMOR, [])

        if blockable and relative_direction in armor:
            damage -= 1

        self.take_damage(damage)

    def is_alive(self) -> bool:
        hp = self.get_property(TokenStats.HP, 0)
        return hp > self.damage

    def get_stat(self, stat_key: TokenStats, default=None):
        return self.get_property(stat_key, default)

    def can_activate(self, initiative: int) -> bool:
        initiatives = self.get_stat(TokenStats.INITIATIVE, [])

        if initiatives is None:
            return False

        if isinstance(initiatives, (list, tuple, set)):
            return initiative in initiatives

        return initiative == initiatives

    def get_attacks(self, initiative: int) -> dict:
        if not self.can_activate(initiative):
            return {}

        attacks = self.get_stat(TokenStats.ATTACKS, {})

        rotated_attacks = {}

        for attack_type, attack_list in attacks.items():
            rotated_attacks[attack_type] = [
                [
                    (direction + self.rotation) % 6,
                    power,
                ]
                for direction, power in attack_list
            ]

        return rotated_attacks