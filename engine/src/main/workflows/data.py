from dataclasses import dataclass
from main.state.serialization import from_dict_dataclass, to_dict_dataclass
from enum import Enum
from main.state.user_action import Type as ActionType
from main.tokens.data import Ability

Hex = tuple[int, int]
    
class WorkflowName(Enum):
    MOVE = "move"
    PUSH = "Push"
    ROTATE = "rotate"
    BOMB = "bomb"
    GRENADE = "grenade"
    SNIPER = "sniper"
    BATTLE = "battle"
    TURN = "turn"
    BOARD = "board"
    HAND = "hand"

ABILITY_WORKFLOW_REGISTRY = {
    Ability.MOVE : WorkflowName.MOVE,
    Ability.BOMB : WorkflowName.BOMB,
    Ability.GRENADE : WorkflowName.GRENADE,
    Ability.SNIPER : WorkflowName.SNIPER,
    Ability.PUSH : WorkflowName.PUSH,
    Ability.BITWA : WorkflowName.BITWA,
}
    
@dataclass
class WorkflowData:
    type        : ActionType | None = None
    slot        : int | None = None
    unit_pos    : Hex | None = None
    target_pos  : Hex | None = None
    destination : Hex | None = None

    @classmethod
    def from_dict(cls, data):
        return from_dict_dataclass(cls, data) 
    
    def to_dict(self):
        return to_dict_dataclass(self)
    
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

@dataclass
class WorkflowInstance:
    name : WorkflowName
    current_step_index : int = 0