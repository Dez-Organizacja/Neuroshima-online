from abc import ABC, abstractmethod
from main.state.contex import ActionContext

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