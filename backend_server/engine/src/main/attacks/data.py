from dataclasses import dataclass
from enum import Enum

class AttackType(Enum):
    MELEE = "melee"
    SHOOT = "shoot"
    GAUSS = "gauss"

@dataclass
class TargetedIntent:
    target_pos : tuple[int, int]
    power : int = 1
    blockable : bool = False
    from_direction : int | None = None
    destroy : bool = False

@dataclass
class DirectedIntent:
    attaker_pos : tuple[int, int]
    direction : int
    attack_type : AttackType
    power : int = 1

AttackIntent = TargetedIntent | DirectedIntent

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
