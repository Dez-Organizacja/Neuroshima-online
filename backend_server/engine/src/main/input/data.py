from dataclasses import dataclass, field
from abc import ABC
from enum import Enum
from main.state.serialization import Serializator

try:
    from enum import StrEnum
except ImportError:  # pragma: no cover - Python < 3.11
    class StrEnum(str, Enum):
        pass

class ActionType(StrEnum):
    BOARD = "board"
    HAND = "hand"
    ROTATE = "rotate"
    BUTTON = "button"

class Button(Enum):
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
class ButtonAction(UserAction):
    name : Button
    type : ActionType = field(default=ActionType.BUTTON, init=False)
    
@dataclass
class HandAction(UserAction):
    slot : int
    type : ActionType = field(default=ActionType.HAND, init=False)

class UserActionFactory(ABC):
    USER_ACTIONS={
        ActionType.ROTATE : RotationAction,
        ActionType.BOARD : BoardAction,
        ActionType.BUTTON : ButtonAction,
        ActionType.HAND : HandAction
    }
    TYPE_KEY = "type"
    @classmethod
    def create(cls, data : dict) -> UserAction:
        action_type = data.pop(cls.TYPE_KEY)
        return Serializator.from_dict_dataclass(
            cls.USER_ACTIONS[action_type], 
            data
        )
