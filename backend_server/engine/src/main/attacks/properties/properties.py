from dataclasses import dataclass
from main.attacks.targeting.data import TargetingType
from main.attacks.data import AttackType
from main.attacks.properties.data import AttackProperties
from main.attacks.properties.factory import AttackPropertiesFactory

@AttackPropertiesFactory.register(AttackType.MELEE)
@dataclass
class MeleeProperties(AttackProperties):
    targeting_type : TargetingType = TargetingType.ADJACENT

@AttackPropertiesFactory.register(AttackType.SHOOT)
@dataclass
class ShootProperties(AttackProperties):
    targeting_type : TargetingType = TargetingType.FIRST_IN_LINE
    blockable : bool = True

@AttackPropertiesFactory.register(AttackType.GAUSS)
@dataclass
class GaussProperties(AttackProperties):
    targeting_type : TargetingType = TargetingType.ALL_IN_LINE
