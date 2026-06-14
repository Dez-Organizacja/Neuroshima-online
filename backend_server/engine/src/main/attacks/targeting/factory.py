from main.attacks.targeting.base import TargetingStrategy
from main.attacks.targeting.data import TargetingType

class TargetingFactory:
    _TARGETING : dict[TargetingType, type[TargetingStrategy]] = {}
    
    @classmethod
    def register(cls, attack_type : TargetingType):
        def wrapper(strategy_cls):
            cls._TARGETING[attack_type] = strategy_cls
            return strategy_cls
        return wrapper

    @classmethod
    def create(cls, name : TargetingType) -> TargetingStrategy:
        return cls._TARGETING[name]