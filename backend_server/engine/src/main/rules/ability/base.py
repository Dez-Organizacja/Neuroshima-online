from abc import ABC, abstractmethod
from main.state.context import ActionContext

class AbilityRules(ABC):
    @staticmethod
    def get_sources(ctx : ActionContext):
        return []
    
    @staticmethod
    def get_targets(ctx : ActionContext):
        return []

    @staticmethod
    def get_destinations(ctx : ActionContext):
        return []
    
    @staticmethod
    def can_use(ctx : ActionContext, pos):
        return False