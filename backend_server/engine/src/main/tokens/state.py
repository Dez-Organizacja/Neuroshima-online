from dataclasses import dataclass, field
from main.tokens.data import TokenRelation

@dataclass
class TokenCoreState:
    rotation            : int = 0
    damage              : int = 0
    wounds              : list[int] = field(default_factory=list)
    wired               : bool = False

@dataclass
class TokenModifiers:
    melee_boosts: int = 0
    shoot_boosts: int = 0

    initiatives: list[int] = field(default_factory=list)
    is_used: list[bool] = field(default_factory=list)
    is_basic: list[bool] = field(default_factory=list)
    num_of_old: int = 0
    
    is_blocked_to_0: bool = False
    initiative_boosts: int = 0
    num_of_new: int = 0

@dataclass
class TokenRelations:
    real_boost_target: TokenRelation | None = None

@dataclass
class TokenExecutionState:
    # clever_initiative: CleverInitiative | None = None
    used_ability : bool = False
    used_battle_ability : bool = False

@dataclass
class BoardTokenState:
    core: TokenCoreState = field(default_factory=TokenCoreState)
    modifiers: TokenModifiers = field(default_factory=TokenModifiers)
    relations: TokenRelations = field(default_factory=TokenRelations)
    exection : TokenExecutionState = field(default_factory=TokenExecutionState)

    # --------- wire ----------
    @property
    def wired(self):
        return self.core.wired
    
    def set_wired(self, value):
        self.core.wired = value

    # --------- rotation ----------
    @property
    def rotation(self):
        return self.core.rotation

    def set_rotation(self, value):
        self.core.rotation = value

    # --------- damage ----------
    @property
    def damage(self):
        return self.core.damage
    
    @property
    def wounds(self):
        return self.core.wounds

    def get_damage(self, cnt : int):
        self.core.damage += cnt

    # --------- initiative ----------
    @property
    def clever_initiative(self):
        return self.modifiers

    # --------- reset ----------
    def reset(self):
        self.core.wired = False
        self.modifiers = TokenModifiers()
        self.relations = TokenRelations()
