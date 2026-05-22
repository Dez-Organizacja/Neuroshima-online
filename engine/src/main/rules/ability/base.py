from abc import ABC, abstractmethod
from main.state.contex import ActionContext
from main.rules.ability.movement import MoveRules, PushRules
from main.workflows.data import Ability

class AbilityRules(ABC):
    @staticmethod
    @abstractmethod
    def get_sources(ctx : ActionContext):
        return []
    
    @staticmethod
    @abstractmethod
    def get_targets(ctx : ActionContext):
        return []

    @staticmethod
    @abstractmethod
    def get_destinations(ctx : ActionContext):
        return []
    
    @staticmethod
    @abstractmethod
    def can_use(ctx : ActionContext, pos):
        return False
    

class AbilityRulesFactory:
    REGISTRY = {
        Ability.MOVE : MoveRules,
        Ability.PUSH : PushRules
    }

    @classmethod
    def get(cls, name : Ability) -> AbilityRules:
        obj = cls.REGISTRY.get(name)
        if not obj:
            raise ValueError("no {name} ability rules")
        return obj