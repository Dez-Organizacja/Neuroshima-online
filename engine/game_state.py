from dataclasses import dataclass, fields, field, MISSING
from typing import get_origin, get_args
from variable import *
from player_state import PlayerState
from plansza import Board

def convert_value(value, target_type, key = None):
    # print(f"convert value: {value} to {target_type}")
    origin = get_origin(target_type) # typ tego co chcemy dostać

    if hasattr(target_type, "from_dict") and isinstance(value, dict):
        if target_type is PlayerState and key is not None:
            return PlayerState.from_dict(key, value)
        return target_type.from_dict(value)
    
    if origin is dict and isinstance(value, dict):
        key_type, value_type = get_args(target_type)
        return {
            k : convert_value(v, value_type, key=k)
            for k, v in value.items()
        }
    
    return value

def auto_to_dict(obj):
    if(hasattr(obj, "to_dict")):
        return obj.to_dict()
    if(hasattr(obj, "to_list")):
        return obj.to_list()
    if(isinstance(obj, dict)):
        return{
            k : auto_to_dict(v)
            for k, v in obj.items()
        }
    if(isinstance(obj, list)):
        return [auto_to_dict(v) for v in obj]
    
    return obj

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
    phase : str
    fractions : list[str]
    state : str = State.NO_SELECTION
    selected : dict = field(default_factory=dict)
    active_action : dict = field(default_factory=dict)
    current_fraction : str = ""
    next_turns : list[dict] = field(default_factory=list)
    players : dict[str, PlayerState] = field(default_factory=dict)
    board : Board = field(default_factory=Board)

    @classmethod
    def from_dict(cls, data):
        values = {}
        for f in fields(cls):
            if(f.name in data):
                value = data.get(f.name)
                values[f.name] = convert_value(value, f.type)

            else:
                if f.default is not MISSING or f.default_factory is not MISSING:
                    continue
                raise ValueError(f"Missing required field: {f.name}")
            
        return cls(**values)
    
    def to_dict(self):
        return {
            f.name : auto_to_dict(getattr(self, f.name))
            for f in fields(self)
        }

    def print_game_state(self):
        print_obj(self.to_dict(), 0)


    @property
    def current_player(self):
        return self.players[self.current_fraction]