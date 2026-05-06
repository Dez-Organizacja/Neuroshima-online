from dataclasses import dataclass
from main.state.serialization import from_dict_dataclass, to_dict_dataclass
from enum import Enum

Hex = tuple[int, int]

class WorkflowSource(Enum):
    HAND = "hand"
    BOARD = "board"

    @classmethod
    def from_dict(cls, value):
        return cls(value)
    
class WorkflowName(Enum):
    MOVE = "move"
    PUSH = "Push"
    ROTATE = "rotate"
    BOMB = "bomb"
    GRENADE = "grenade"
    SNIPER = "sniper"
    BATTLE = "battle"
    CHOOSING_ACTION = "choosing_action"


@dataclass
class WorkflowData:
    unit_pos : Hex | None = None
    target_pos : Hex | None = None
    destination : Hex | None = None
    source : WorkflowSource | None = None
    current_step_index : int = 0

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