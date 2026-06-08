from dataclasses import dataclass, field
from collections import deque
from main.state.player_state import PlayerState
from main.board.board import Board
from main.events.data import Event
from main.attacks.data import AttackIntent
from main.workflows.data import WorkflowData, WorkflowInstance
from main.state.serialization import Serializator

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
    events_queue          : deque[Event] = field(default_factory=deque)
    pending_attacks       : list[AttackIntent] = field(default_factory=list)

    # --------- workflows ----------
    workflow_data       : WorkflowData = field(default_factory=WorkflowData)
    workflow_stack      : list[WorkflowInstance] = field(default_factory=list)

    def __post_init__(self):
        for faction in self.factions:
            if not faction in self.players:
                self.add_player(faction)

    @classmethod
    def from_dict(cls, data):
        return Serializator.from_dict_dataclass(cls, data)
    
    def to_dict(self):
        return Serializator.to_dict_dataclass(self)
    
    def print_game_state(self):
        print_obj(self.to_dict(), 0)

    def add_player(self, faction):
        self.players[faction] = PlayerState()