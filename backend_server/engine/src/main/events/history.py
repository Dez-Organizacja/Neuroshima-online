from dataclasses import dataclass

from main.events.data import Effect
from main.state.contex import ActionContext
from main.state.game_state import GameState


@dataclass
class RestoreUndoSnapshotEffect(Effect):
    decision_faction: str | None = None

    def apply(self, ctx: ActionContext):
        snapshot = ctx.state.pop_latest_undo_snapshot(self.decision_faction)
        restored_state = GameState.from_dict(snapshot)
        ctx.state.__dict__.clear()
        ctx.state.__dict__.update(restored_state.__dict__)
