from dataclasses import dataclass, field
from abc import ABC
from enum import Enum

class ActionType(Enum):
    BOARD = "board"
    HAND = "hand"
    ROTATE = "rotate"
    BOTTOM = "bottom"

class Bottom(Enum):
    END_TURN = "end_turn"
    DISCARD = "discard"
    USE = "use"
    CANCEL = "cancel"
    YES = "yes"
    NO = "no"

@dataclass
class UserAction(ABC):
    type : str = field(init=False)

@dataclass
class RotationAction(UserAction):
    rotation : int
    type : ActionType = field(default=ActionType.ROTATE, init=False)
    
@dataclass
class BoardAction(UserAction):
    pos : tuple[int, int]
    type : ActionType = field(default=ActionType.BOARD, init=False)

@dataclass
class BottomAction(UserAction):
    name : Bottom
    type : ActionType = field(default=ActionType.BOTTOM, init=False)
    
@dataclass
class HandAction(UserAction):
    slot : int
    type : ActionType = field(default=ActionType.HAND, init=False)

class UserActionFactory(ABC):
    USER_ACTIONS={
        ActionType.ROTATE : RotationAction,
        ActionType.BOARD : BoardAction,
        ActionType.BOTTOM : BottomAction,
        ActionType.HAND : HandAction
    }
    TYPE_KEY = "type"
    @classmethod
    def create(cls, data : dict):
        action_type = data.pop(cls.TYPE_KEY)
        return cls.USER_ACTIONS[action_type](**data)