from main.input.data import Bottom
from dataclasses import dataclass, field
from main.state.serialization import Serializator

@dataclass
class AvailableStructure:
    hand : list[bool] = field(default_factory=list)
    board : list[tuple[int, int]] = field(default_factory=list)
    buttons : list[Bottom] = field(default_factory=list)

    def __post_init__(self):
        self.hand = [False] * 3

    def to_dict(self):
        return Serializator.to_dict_dataclass(self)