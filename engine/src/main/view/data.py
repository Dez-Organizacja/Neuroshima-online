from dataclasses import dataclass
from enum import Enum
from main.state.serialization import to_dict_dataclass
from main.actions.available.data import AvailableStructure

class UIMode(Enum):
    DEFAULT = "default"
    ROTATION = "rotation"
    DECISION = "decision"

@dataclass
class StepUIState:
    fraction : str
    mode : UIMode = UIMode.DEFAULT
    message : str = ""

    def to_dict(self) -> dict:
        return to_dict_dataclass(self)
    
@dataclass
class StepViewData:
    available_actions : AvailableStructure
    ui_state : StepUIState

    def to_dict(self) -> dict:
        to_dict_dataclass(self)