from dataclasses import fields, MISSING, is_dataclass
from typing import get_origin, get_args
from collections import deque
from enum import Enum

class Serializator:
    @staticmethod
    def convert_value(value, target_type, key=None):

        origin = get_origin(target_type)
        # print(f"convert vaule {value} to {target_type} ")

        # ---------- enum ----------
        if isinstance(target_type, type) and issubclass(target_type, Enum):
            return target_type(value)

        # ---------- custom from_dict ----------
        if hasattr(target_type, "from_dict") and isinstance(value, dict):
            return target_type.from_dict(value)

        # ---------- custom from_list ----------
        if hasattr(target_type, "from_list") and isinstance(value, list):
            return target_type.from_list(value)
        
        # ---------- dataclass ----------
        if (
            isinstance(target_type, type)
            and is_dataclass(target_type)
            and isinstance(value, dict)
        ):
            return Serializator.from_dict_dataclass(target_type, value)


        # ---------- dict ----------
        if origin is dict and isinstance(value, dict):
            key_type, value_type = get_args(target_type)

            result = {}
            for k, v in value.items():

                # enum key handling
                if isinstance(key_type, type) and issubclass(key_type, Enum):
                    k = key_type(k)

                result[k] = Serializator.convert_value(v, value_type)

            return result

        # ---------- list ----------
        if origin is list:
            item_type = get_args(target_type)[0]

            return [
                Serializator.convert_value(v, item_type)
                for v in value
            ]

        # ---------- deque ----------
        if origin is deque:
            item_type = get_args(target_type)[0]

            return deque(
                Serializator.convert_value(v, item_type)
                for v in value
            )

        # ---------- tuple ----------
        if origin is tuple:
            item_types = get_args(target_type)

            return tuple(
                Serializator.convert_value(v, t)
                for v, t in zip(value, item_types)
            )

        return value

    @staticmethod
    def from_dict_dataclass(cls, data: dict):
        values = {}

        for f in fields(cls):

            if f.name in data:
                value = data[f.name]
                values[f.name] = Serializator.convert_value(value, f.type)

            else:
                if f.default is not MISSING or f.default_factory is not MISSING:
                    continue

                raise ValueError(f"Missing required field: {f.name}")

        return cls(**values)


    @staticmethod
    def auto_to_dict(obj):
        # ---------- custom serializer (optional escape hatch) ----------
        if hasattr(obj, "to_dict") and callable(obj.to_dict):
            return obj.to_dict()

        if hasattr(obj, "to_list") and callable(obj.to_list):
            return obj.to_list()

        # ---------- enum ----------
        if isinstance(obj, Enum):
            return obj.value

        # ---------- dataclass ----------
        if is_dataclass(obj):
            return {
                f.name: Serializator.auto_to_dict(getattr(obj, f.name))
                for f in fields(obj)
            }

        # ---------- dict ----------
        if isinstance(obj, dict):
            return {
                Serializator.auto_to_dict(k) : Serializator.auto_to_dict(v)
                for k, v in obj.items()
            }

        # ---------- list / deque ----------
        if isinstance(obj, (list, deque)):
            return [Serializator.auto_to_dict(v) for v in obj]

        # ---------- tuple ----------
        if isinstance(obj, tuple):
            return [Serializator.auto_to_dict(v) for v in obj]


        # ---------- primitive ----------
        return obj

    @staticmethod
    def to_dict_dataclass(obj):
        return{
            f.name : Serializator.auto_to_dict(getattr(obj, f.name))
            for f in fields(obj)
        }