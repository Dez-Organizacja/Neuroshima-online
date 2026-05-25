from dataclasses import dataclass
from enum import Enum
from main.actions.available.data import AvailableStructure
from main.state.serialization import Serializator

class UIMode(Enum):
    DEFAULT = "default"
    ROTATION = "rotation"
    DECISION = "decision"

@dataclass
class StepUIState:
    fraction : str
    mode : UIMode = UIMode.DEFAULT
    message : str = ""
   
    def to_dict(self):
        Serializator.to_dict_dataclass(self)

@dataclass
class StepViewData:
    available_actions : AvailableStructure
    ui_state : StepUIState
    
    def to_dict(self):
        Serializator.to_dict_dataclass(self)