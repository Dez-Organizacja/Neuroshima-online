from dataclasses import dataclass, field
from collections import deque
from main.state.player_state import PlayerState
from main.board.board import Board
from main.events.data import Event
from main.attacks.data import AttackIntent
from main.workflows.data import WorkflowData, WorkflowInstance, WorkflowName, UndoSnapshot
from main.state.serialization import Serializator
from main.utils.variable import Phase
from main.state.last_clicked_hex import LastClickedHex

def print_obj(obj, deepth):
    base_s = "\n" + "   " * deepth
    pre_s = "\n" + "   " * (deepth - 1)
    # print("PRINTING: ", obj, "deepth: ", deepth)
    if(isinstance(obj, dict)):
        if(deepth > 0):
            print(pre_s + "--->", end='')
        for k, v in obj.items():
            print(base_s, k, end='', sep='')
            print_obj(v, deepth + 1)
        
        if(deepth > 0):
            print(pre_s + "#####",end='')
        return True
    
    if(isinstance(obj, list)):
        if(deepth > 0):
            print(pre_s + "||||", end='')
        for v in obj:
            status = print_obj(v, deepth + 1)
            print(',', end=('\n' if status else ''))
        
        if(deepth > 0):
            print(pre_s + "////",end='')
        
        return True

    
    
    print(" ", obj, end='')
    return False

@dataclass
class GameState:
    # --------- factions ----------
    factions            : list[str]
    turn_faction        : str = ""
    active_faction      : str = ""

    # --------- tokens ----------
    players             : dict[str, PlayerState] = field(default_factory=dict)
    board               : Board = field(default_factory=Board)
    
    # --------- events ----------
    events_queue        : deque[Event] = field(default_factory=deque)
    pending_attacks     : list[AttackIntent] = field(default_factory=list)
    pending_workflows   : list[WorkflowInstance] = field(default_factory=list)

    # --------- workflows ----------
    workflow_data       : WorkflowData = field(default_factory=WorkflowData)
    workflow_stack      : list[WorkflowInstance] = field(default_factory=list)
    
    # --------- others ----------
    undo_stack          : list[UndoSnapshot] = field(default_factory=list)
    phase               : Phase = Phase.GAME
    last_clicked_hex    : LastClickedHex = field(default_factory=LastClickedHex)
    
    def __post_init__(self):
        for faction in self.factions:
            if not faction in self.players:
                self.add_player(faction)

    @classmethod
    def from_dict(cls, data) -> GameState:
        data = dict(data)
        if data.get("last_clicked_hex") is None:
            data.pop("last_clicked_hex", None)
        return Serializator.from_dict_dataclass(cls, data)
    
    def to_dict(self):
        return Serializator.to_dict_dataclass(self)
    
    def print_game_state(self):
        print_obj(self.to_dict(), 0)

    def add_player(self, faction):
        self.players[faction] = PlayerState()

    def create_undo_snapshot(self, workflow_name : WorkflowName, owner_faction : str) -> None:
        if not owner_faction:
            return

        snapshot = self.to_dict()
        self.undo_stack.append(
            UndoSnapshot(
                workflow_name=workflow_name,
                owner_faction=owner_faction,
                snapshot=snapshot,
            )
        )

    def clear_undo_stack(self, decision_faction : str | None) -> None:
        if not decision_faction:
            return

        if any(snapshot.owner_faction != decision_faction for snapshot in self.undo_stack):
            self.undo_stack.clear()

    def pop_latest_undo_snapshot(self, decision_faction : str | None) -> dict:
        if not self.undo_stack:
            raise ValueError("brak akcji do cofniecia")

        snapshot = self.undo_stack[-1]
        if decision_faction and snapshot.owner_faction != decision_faction:
            raise ValueError("nie mozesz cofnac akcji innego gracza")

        self.undo_stack.pop()
        return snapshot.snapshot

    def can_undo(self, decision_faction : str | None) -> bool:
        if not self.undo_stack:
            return False

        snapshot = self.undo_stack[-1]
        return decision_faction is None or snapshot.owner_faction == decision_faction
