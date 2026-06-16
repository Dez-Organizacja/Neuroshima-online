from dataclasses import dataclass, field
from main.tokens.data import TokenRelation, Ability
from main.tokens.config import BoardTokenConfig
from main.attacks.config import AttackType

@dataclass
class TokenCoreState:
    rotation            : int = 0
    damage              : int = 0
    wounds              : list[int] = field(default_factory=list)
    wired               : bool = False

@dataclass
class TokenModifiers:
    attack_boosts : dict[AttackType, int] = field(default_factory=dict)
    from_boost_ability : Ability | None = None

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
    used_from_boost_ability : bool = False
    used_battle_ability : bool = False

@dataclass
class BoardTokenState:
    core: TokenCoreState = field(default_factory=TokenCoreState)
    modifiers: TokenModifiers = field(default_factory=TokenModifiers)
    relations: TokenRelations = field(default_factory=TokenRelations)
    execution : TokenExecutionState = field(default_factory=TokenExecutionState)

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

    def reset_abitility(self):
        self.execution = TokenExecutionState()


    def reset_boosts(self, config : BoardTokenConfig):
        # self.modifiers = TokenModifiers()
        # self.relations = TokenRelations()
        self.reset_modifiers()
        self.reset_initiatives(config.initiative)
        self.reset_relations(config.boost_target)
        

    def reset_modifiers(self):
        self.modifiers.attack_boosts.clear()
        self.modifiers.is_blocked_to_0 = False
        self.modifiers.initiative_boosts = 0
        self.modifiers.num_of_new = 0
        self.modifiers.from_boost_ability = None
    
    def reset_initiatives(self, initiatives : list[int]):
        self.modifiers.initiatives = initiatives
        self.modifiers.is_used = [False for _ in initiatives]
        self.modifiers.is_basic = [True for _ in initiatives]

    def reset_relations(self, relation : TokenRelation):
        self.relations.real_boost_target = relation

    def add_attack_boost(self, attack_type : AttackType, cnt : int):
        boosts = self.modifiers.attack_boosts
        boosts[attack_type] = boosts.get(attack_type, 0) + cnt
        # self.state.modifiers.attack_boosts[attack_type] += cnt