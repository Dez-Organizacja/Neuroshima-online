from dataclasses import dataclass, field
from abc import ABC
from enum import Enum
from main.board.data import Hex

class AnimationType(Enum):
    WOUND="wound"
    ATTACK="attack"
    WEAKEN="weaken"
    DESTROY="destroy"
    SET_WIRE="set_wire"


@dataclass
class Animation(ABC):
    type : AnimationType = field(default=None, init=False)

@dataclass
class WoundAnimation(Animation):
    target : Hex
    wounds : int
    type : AnimationType = field(default=AnimationType.WOUND, init=False)

@dataclass
class DestroyAnimation(Animation):
    target : Hex
    type : AnimationType = field(default=AnimationType.DESTROY, init=False)

@dataclass
class AttackAnimation(Animation):
    attacker : Hex
    target : Hex
    type : AnimationType = field(default=AnimationType.ATTACK, init=False)

@dataclass
class WeakenAnimation(Animation):
    target : Hex
    damage : int
    type : AnimationType = field(default=AnimationType.WEAKEN, init=False)

@dataclass
class SetWireAnimation(Animation):
    target: Hex
    wired: bool
    type: AnimationType = field(default=AnimationType.SET_WIRE, init=False)