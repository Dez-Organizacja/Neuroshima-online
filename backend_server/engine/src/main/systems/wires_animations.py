from collections.abc import Mapping
from dataclasses import dataclass, field

from main.board.board import Board
from main.board.data import Hex
from main.events.animations import Animation

@dataclass
class SetWireAnimation(Animation):
    pos: Hex
    wired: bool
    type: str = field(default="set_wire", init=False)


class WiresAnimationSystem:
    @staticmethod
    def snapshot(board: Board) -> dict[Hex, bool]:
        return {
            pos: token.wired
            for pos in board.ALL_HEXES
            if (token := board.get_token(pos)) is not None
        }

    @classmethod
    def get_wire_animations(
        cls,
        before: Mapping[Hex, bool],
        after: Mapping[Hex, bool],
    ) -> list[Animation]:

        result: list[Animation] = []

        for pos in sorted(set(before) | set(after)):
            before_wired = before.get(pos, False)
            after_wired = after.get(pos, False)

            if before_wired == after_wired:
                continue

            result.append(SetWireAnimation(pos=pos, wired=after_wired))

        return result


class WireAnimationTracker:
    def __init__(self, board: Board):
        self.before = WiresAnimationSystem.snapshot(board)

    def collect(self, board: Board) -> list[Animation]:
        after = WiresAnimationSystem.snapshot(board)
        animations = WiresAnimationSystem.get_wire_animations(
            before=self.before,
            after=after,
        )
        self.before = after
        return animations
