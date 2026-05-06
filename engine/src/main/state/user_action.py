from dataclasses import dataclass
from abc import ABC
from enum import Enum
from main.state.serialization import from_dict_dataclass

class Type(Enum):
    BOARD = "board"
    HAND = "hand"
    ROTATE = "rotate"
    BOTTOM = "bottom"

@dataclass
class UserAction(ABC):
    type : str
    def get_type(self):
        return self.type

@dataclass
class RotationAction(UserAction):
    rotation : int
    def __post_init__(self):
        self.type = Type.ROTATE

    def get_rotation(self):
        return self.rotation
    
    
@dataclass
class BoardAction(UserAction):
    pos : tuple[int, int]
    def __post_init__(self):
        self.type = Type.BOARD

    def get_pos(self):
        return self.pos

@dataclass
class BottomAction(UserAction):
    name : str | None = None
    def __post_init__(self):
        self.type = Type.BOTTOM

    def get_name(self):
        return self.name

@dataclass
class HandAction(UserAction):
    slot : int | None = None
    def __post_init__(self):
        self.type = Type.HAND

    def get_slot(self):
        return self.name

class UserActionFactory(ABC):
    USER_ACTIONS={
        Type.ROTATE : RotationAction,
        Type.BOARD : BoardAction,
        Type.BOTTOM : BottomAction,
        Type.HAND : HandAction
    }
    TYPE_KEY = "type"
    @classmethod
    def create(cls, data : dict):
        action_type = data[cls.TYPE_KEY]
        return cls.USER_ACTIONS[action_type]()