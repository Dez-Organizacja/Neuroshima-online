from dataclasses import dataclass, field
from main.attacks.properties.data import AttackProperties
from main.events.data import Effect
from main.events.animations import Animation

@dataclass
class TargetedIntent:
    target_pos : tuple[int, int]
    attacker_pos : tuple[int, int] | None = None
    power : int = 1
    blockable : bool = False
    from_direction : int | None = None
    destroy : bool = False

@dataclass
class DirectedIntent:
    attacker_pos : tuple[int, int]
    direction : int
    properties : AttackProperties
    power : int = 1

AttackIntent = TargetedIntent | DirectedIntent

@dataclass
class AttackResult:
    result      : list[Effect] = field(default_factory=list)
    animations  : list[Animation] = field(default_factory=list)

@dataclass
class TargetResoltion:
    target_pos : tuple[int, int]
    effects : list[Effect] = field(default_factory=list)
    hit : bool = True

@dataclass
class AttackLog:
    resolved_targets : list[TargetResoltion] = field(default_factory=list)
    attacker_pos : tuple[int, int] | None = None