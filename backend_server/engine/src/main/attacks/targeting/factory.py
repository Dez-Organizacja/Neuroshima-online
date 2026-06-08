from main.attacks.targeting.base import TargetingStrategy
from main.attacks.data import AttackType

class TargetingFactory:
    _TARGETING : dict[AttackType, type[TargetingStrategy]] = {}
    
    @classmethod
    def register(cls, attack_type : AttackType):
        def wrapper(strategy_cls):
            cls._TARGETING[attack_type] = strategy_cls
            return strategy_cls
        return wrapper

    @classmethod
    def create(cls, name : AttackType) -> TargetingStrategy:
        return cls._TARGETING[name]