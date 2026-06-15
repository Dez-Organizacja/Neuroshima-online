from main.state.game_state import GameState

class UndoSystem:
    def __init__(self, history : list[dict] | None = None):
        self.stack = history or []

    def clear_undo_stack(self):
        self.stack.clear()

    def create_undo_snapshot(self, state : GameState) -> None:
        print("creating undo snapshot")
        snapshot : dict = state.to_dict()
        self.stack.append(snapshot)

    def undo(self) -> GameState:
        if not self.stack:
            raise ValueError("no snapshots to undo")
        # print("Undoing")
        snapshot = self.stack.pop()
        # print(snapshot)
        return GameState.from_dict(snapshot)


    def can_undo(self) -> bool:
        return len(self.stack) > 0 #bo jest tu stan aktualny
    
    @classmethod
    def from_dict(cls, data : list) -> "UndoSystem":
        return cls(data)

    def to_list(self) -> list:
        print("serializing undo stack")
        print(f"stack : {len(self.stack)}")
        return self.stack