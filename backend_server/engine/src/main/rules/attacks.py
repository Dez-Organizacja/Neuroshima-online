from main.attacks.data import AttackType
from main.attacks.targeting.data import TargetingType

ATTACK_TARGETING_RULES: dict[AttackType, TargetingType] = {
    AttackType.MELEE: TargetingType.ADJACENT_DIRECTION,
    AttackType.SHOOT: TargetingType.FIRST_IN_LINE,
    AttackType.GAUSS: TargetingType.ALL_IN_LINE,
}

def get_targeting(attack_type: AttackType) -> TargetingType:
    return ATTACK_TARGETING_RULES[attack_type]