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
    faction : str
    mode : UIMode = UIMode.DEFAULT
    message : str = ""
   
    def to_dict(self):
        data = Serializator.to_dict_dataclass(self)
        data["faction"] = data.pop("faction")
        return data

@dataclass
class StepViewData:
    available_actions : AvailableStructure
    ui_state : StepUIState
    
    def to_dict(self) -> dict:
        return {
            "availableActions": Serializator.auto_to_dict(self.available_actions),
            "uiState": self.ui_state.to_dict()
        }