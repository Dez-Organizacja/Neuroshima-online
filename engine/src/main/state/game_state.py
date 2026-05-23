from dataclasses import dataclass, field
from main.utils.variable import *
from main.state.player_state import PlayerState
from main.board.board import Board
from main.events.data import FlowEvent
from collections import deque
from main.workflows.data import WorkflowData, WorkflowInstance
from main.state.serialization import from_dict_dataclass, to_dict_dataclass

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
    fractions           : list[str]
    current_fraction    : str = ""
    players             : dict[str, PlayerState] = field(default_factory=dict)
    board               : Board = field(default_factory=Board)
    flow_queue          : deque[FlowEvent] = field(default_factory=deque)
    workflow_data       : WorkflowData = field(default_factory=WorkflowData)
    workflow_stack      : deque[WorkflowInstance] = field(default_factory=deque)

    @classmethod
    def from_dict(cls, data):
        return from_dict_dataclass(cls, data)
    
    def to_dict(self):
        return to_dict_dataclass(self)
    
    def print_game_state(self):
        print_obj(self.to_dict(), 0)

    def add_player(self, fraction):
        player = PlayerState(fraction)
        player.new_game()
        self.players[fraction] = player