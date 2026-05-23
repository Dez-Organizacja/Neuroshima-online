from main.input.data import Bottom
from dataclasses import dataclass
from main.state.serialization import to_dict_dataclass

@dataclass
class AvailableStructure:
    hand : dict[str, list[bool]]
    board : dict[tuple[int, int], bool]
    bottoms : dict[Bottom, bool]

    def to_dict(self):
        return to_dict_dataclass(self)