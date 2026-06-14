from abc import ABC
from dataclasses import dataclass
from main.attacks.targeting.data import TargetingType

@dataclass
class AttackProperties(ABC):
    targeting_type : TargetingType
    blockable : bool = False