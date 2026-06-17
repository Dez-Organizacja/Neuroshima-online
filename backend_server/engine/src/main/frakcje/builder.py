from main.tokens.data import TokenType, Boost, Ability, TokenRelation, BattleAbility
from main.tokens.config import TokenConfig, BoardTokenConfig, BoostInstance
from main.attacks.config import AttackConfig, AttackType, AttackSpec

class TokenConfigBuilder:
    def __init__(self, config : TokenConfig):
        self.config = config

    def ability(self, name : Ability):
        self.config.abilities.ability = name
        return self
    
    def battle_ability(self, name : BattleAbility):
        self.config.abilities.battle_ability = name
        return self

    def build(self) -> TokenConfig:
        return self.config

class BoardTokenConfigBuilder(TokenConfigBuilder):
    def __init__(self, base : TokenConfig):
        self.config = BoardTokenConfig.from_base(base)

    @staticmethod
    def compile_attacks(spec : AttackSpec) -> list[AttackConfig]:
        result = []
        for d in spec.directions:
            result.append(
                AttackConfig(
                    attack_type=spec.attack_type,
                    direction=d,
                    power=spec.power,
                )
            )
        return result

    def attacks(self, *specs : list[AttackSpec]):
        for spec in specs:
            self.config.attacks.extend(self.compile_attacks(spec))
        return self
    
    def initiatives(self, initiatives : list[int]):
        self.config.initiative = initiatives
        return self

    def boosts(
            self, 
            types : list[Boost], 
            directions : list[int] = [], 
            target : TokenRelation = TokenRelation.OWN,
        ):
        for t in types:
            self.config.boosts[t] = BoostInstance(directions)
        self.config.boost_target = target
        return self
    
    def hp(self, hp : int):
        self.config.hp = hp
        return self

    def directions_of(self, armor : list[int] = None, wire : list[int] = None):
        self.config.armor = armor or []
        self.config.wire = wire or []
        return self

def token(name : str, faction : str, unit_count : int, type : TokenType):
    config = TokenConfig(
        faction=faction,
        name = name,
        type = type,
        unit_count=unit_count
    )
    if type == TokenType.BOARD:
        return BoardTokenConfigBuilder(config)
    if type == TokenType.INSTANT:
        return TokenConfigBuilder(config)
    
    raise ValueError(f"invalid token type {type}")

def melee(directions : list[int], power : int = 1):
    return AttackSpec(AttackType.MELEE, directions, power)

def shoot(directions : list[int], power : int = 1):
    return AttackSpec(AttackType.SHOOT, directions, power)

def gauss(directions : list[int], power : int = 1):
    return AttackSpec(AttackType.GAUSS, directions, power)
