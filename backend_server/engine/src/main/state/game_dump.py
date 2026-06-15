from main.state.serialization import Serializator
from dataclasses import dataclass, field

@dataclass
class GameDump:
    state : dict
    undo : list = field(default_factory=list)

    @classmethod
    def from_dict(cls, data) -> "GameDump":
        return Serializator.from_dict_dataclass(cls, data)
    
    def to_dict(self) -> dict:
        return Serializator.to_dict_dataclass(self)