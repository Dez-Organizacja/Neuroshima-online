from main.input.data import Bottom
from dataclasses import dataclass
from main.state.serialization import Serializator

@dataclass
class AvailableStructure:
    hand : dict[str, list[bool]]
    board : dict[tuple[int, int], bool]
    bottoms : dict[Bottom, bool]

    def to_dict(self):
        return Serializator.to_dict_dataclass(self)