from dataclasses import dataclass, field
from enum import Enum
from main.input.data import ActionType
from main.tokens.data import Ability, BattleAbility
from main.input.data import Button
from typing import TypeVar

Hex = tuple[int, int]
    
class WorkflowName(Enum):
    MOVE = "move"
    PUSH = "push"
    ROTATE = "rotate"
    BOMB = "bomb"
    GRENADE = "grenade"
    SNIPER = "sniper"
    BATTLE = "battle"
    TURN = "turn"
    BOARD = "board"
    HAND = "hand"
    PLACE = "place"
    START_BATTLE = "start_battle"
    GAME = "game"
    HEAL = "heal"
    HEADQUARTER_TURN = "headquarter_turn"
    HEADQUARTER_PLACE = "headquarter_place"
    INITIATIVE = "initiative"
    EXPLOSION = "explosion"

ABILITY_WORKFLOW_REGISTRY = {
    Ability.MOVE : WorkflowName.MOVE,
    Ability.BOMB : WorkflowName.BOMB,
    Ability.GRENADE : WorkflowName.GRENADE,
    Ability.SNIPER : WorkflowName.SNIPER,
    Ability.PUSH : WorkflowName.PUSH,
    Ability.BATTLE : WorkflowName.START_BATTLE,
}
BATTLE_ABILITY_WORKFLOW_REGISTRY = {
    BattleAbility.EXPLOSIN : WorkflowName.EXPLOSION   
}
    
@dataclass
class WorkflowData:
    slot        : int | None = None
    unit_pos    : Hex | None = None
    target_pos  : Hex | None = None
    destination : Hex | None = None
    rotation    : int | None = None
    type        : ActionType | None = None
    button      : Button | None = None
    decision    : bool | None = None

    # @classmethod
    # def from_dict(cls, data):
    #     return from_dict_dataclass(cls, data) 
    
    # def to_dict(self):
    #     return to_dict_dataclass(self)
    
    def set_unit_pos(self, value):
        self.unit_pos = value
    
    def set_target_pos(self, value):
        self.target_pos = value
    
    def set_destination(self, value):
        self.destination = value

    def set_slot(self, value):
        self.slot = value

    def set_type(self, value):
        self.type = value

    def set_rotation(self, value):
        self.rotation = value

    def set_decision(self, value):
        self.decision = value


@dataclass
class WorkflowConfig:
    faction : str = ""
    factions : list[str] = field(default_factory=list)
    hand_limit : int = 3
    pos : tuple[int, int] | None = None
    initiative : int | None = None

@dataclass
class WorkflowInstance:
    name : WorkflowName
    current_step_index : int | None = None
    config : WorkflowConfig = field(default_factory=WorkflowConfig)
