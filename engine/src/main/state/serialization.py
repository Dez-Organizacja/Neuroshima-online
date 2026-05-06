from typing import get_origin, get_args
from dataclasses import fields, MISSING
from collections import deque
from main.state.player_state import PlayerState

def convert_value(value, target_type, key = None):
    # print(f"convert value: {value} to {target_type}")
    origin = get_origin(target_type) # typ tego co chcemy dostać

    if hasattr(target_type, "from_dict") and isinstance(value, dict):
        if target_type is PlayerState and key is not None:
            return PlayerState.from_dict(key, value)
        return target_type.from_dict(value)

    if hasattr(target_type, "from_list") and isinstance(value, list):
        return target_type.from_list(value)

    if origin is dict and isinstance(value, dict):
        key_type, value_type = get_args(target_type)
        return {
            k : convert_value(v, value_type, key=k)
            for k, v in value.items()
        }

    if origin is tuple:
        return tuple(value)

    return value
    
def from_dict_dataclass(cls, data: dict):
    values = {}

    for f in fields(cls):
        if f.name in data:
            value = data[f.name]
            values[f.name] = convert_value(value, f.type)
        else:
            if f.default is not MISSING or f.default_factory is not MISSING:
                continue
            raise ValueError(f"Missing required field: {f.name}")

    return cls(**values)

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
    if(isinstance(obj, (list, deque))):
        return [auto_to_dict(v) for v in obj]
    
    return obj

def to_dict_dataclass(obj):
    return{
        f.name : auto_to_dict(getattr(obj, f.value))
        for f in fields(obj)
    }