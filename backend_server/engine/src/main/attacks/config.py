from dataclasses import dataclass
from enum import Enum

class AttackType(Enum):
    MELEE = "melee"
    SHOOT = "shoot"
    GAUSS = "gauss"

@dataclass
class AttackConfig:
    attack_type : AttackType
    direction : int
    power : int = 1

@dataclass
class AttackSpec:
    attack_type : AttackType
    directions : list[int]
    power : int = 1    
