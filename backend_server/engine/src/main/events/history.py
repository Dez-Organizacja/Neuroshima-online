from dataclasses import dataclass

from main.events.data import Effect
from main.state.context import ActionContext
from main.state.game_state import GameState

@dataclass
class ClearUndoStackEffect(Effect):
    def apply(self, ctx : ActionContext):
        ctx.undo_system.clear_undo_stack()

@dataclass
class CreateSnapshotEffect(Effect):
    def apply(self, ctx : ActionContext):
        ctx.undo_system.create_undo_snapshot(ctx.state)

@dataclass
class UndoEffect(Effect):
    # def __init__(self):
        # print("INITED UNDO EFFECT")

    def apply(self, ctx: ActionContext):
        # print("appling UNDO EFFECT")
        ctx.state = ctx.undo_system.undo()
        # snapshot = ctx.state.pop_latest_undo_snapshot(self.decision_faction)
        # restored_state = GameState.from_dict(snapshot)
        # ctx.state.__dict__.clear()
        # ctx.state.__dict__.update(restored_state.__dict__)
