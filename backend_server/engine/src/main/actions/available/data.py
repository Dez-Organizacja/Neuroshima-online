from main.input.data import Button
from dataclasses import dataclass, field
from main.state.serialization import Serializator
from main.tokens.hand import Hand

@dataclass
class AvailableStructure:
    hand : list[bool] = field(default_factory=list)
    board : list[tuple[int, int]] = field(default_factory=list)
    buttons : list[Button] = field(default_factory=list)

    def __post_init__(self):
        self.hand = [False] * Hand.MAX_LIMIT

    def to_dict(self):
        return Serializator.to_dict_dataclass(self)