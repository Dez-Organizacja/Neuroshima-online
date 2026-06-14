from dataclasses import dataclass

@dataclass
class LastClickedHex:
    source: str | None = None
    pos: tuple[int, int] | None = None
    slot: int | None = None

    def reset(self) -> None:
        self.source = None
        self.pos = None
        self.slot = None

    def set_board(self, pos: tuple[int, int]) -> None:
        self.source = "board"
        self.pos = pos
        self.slot = None

    def set_hand(self, slot: int) -> None:
        self.source = "hand"
        self.slot = slot
        self.pos = None
