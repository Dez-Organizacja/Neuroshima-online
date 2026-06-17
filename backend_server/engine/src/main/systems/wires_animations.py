from collections.abc import Mapping
from dataclasses import dataclass, field

from main.board.board import Board
from main.board.data import Hex
from main.events.animations import Animation

@dataclass
class SetWireAnimation(Animation):
    target: Hex
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
        ordered_logs=None,
    ) -> list[Animation]:

        result: list[Animation] = []
        changed = {
            pos: after.get(pos, False)
            for pos in set(before) | set(after)
            if before.get(pos, False) != after.get(pos, False)
        }

        for animation in ordered_logs or []:
            pos = animation.target
            wired = changed.get(pos)

            if wired is None or wired != animation.wired:
                continue

            result.append(SetWireAnimation(target=pos, wired=wired))
            del changed[pos]

        for pos in sorted(changed):
            result.append(SetWireAnimation(target=pos, wired=changed[pos]))

        return result


class WireAnimationTracker:
    def __init__(self, board: Board):
        self.before = WiresAnimationSystem.snapshot(board)

    def collect(self, board: Board, ordered_logs=None) -> list[Animation]:
        after = WiresAnimationSystem.snapshot(board)
        animations = WiresAnimationSystem.get_wire_animations(
            before=self.before,
            after=after,
            ordered_logs=ordered_logs,
        )
        self.before = after
        return animations
